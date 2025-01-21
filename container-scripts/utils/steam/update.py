import logging
import os
import shutil
import sys

import requests
from constants import (
    STARBOUND_APP_ID,
    STARBOUND_INSTALL_DIR,
    STARBOUND_PACKED_FILE_PATH,
    STEAM_USER,
)
from utils.shell import run_command

log = logging.getLogger(__name__)


def _starbound_needs_update() -> bool:
    try:
        response = requests.get(
            "https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/",
            params={"appid": STARBOUND_APP_ID, "count": 1, "format": "json"},
        )
        response.raise_for_status()
        data = response.json()
        if (
            "appnews" not in data
            or "newsitems" not in data["appnews"]
            or not data["appnews"]["newsitems"]
            or "date" not in data["appnews"]["newsitems"][0]
        ):
            log.error("Invalid Steam API response while checking for Starbound update.")
            return False
        remote_timestamp = data["appnews"]["newsitems"][0]["date"]
        local_timestamp = os.path.getmtime(STARBOUND_INSTALL_DIR)
        if remote_timestamp > local_timestamp:
            log.info("New Starbound update available.")
        else:
            log.info("No new Starbound update available.")
        return remote_timestamp > local_timestamp
    except (requests.RequestException, KeyError, ValueError, OSError) as e:
        log.error(f"Error checking for Starbound updates: {e}", exc_info=True)
        return False


def update_starbound() -> None:
    already_installed = (
        os.path.isdir(STARBOUND_INSTALL_DIR)
        and os.listdir(STARBOUND_INSTALL_DIR)
        and os.path.isfile(
            os.path.join(STARBOUND_INSTALL_DIR, "linux/starbound_server")
        )
    )
    needs_update = _starbound_needs_update() if already_installed else True
    if not already_installed:
        log.info(f"Starbound not found in {STARBOUND_INSTALL_DIR}. Downloading...")
    elif needs_update:
        log.info(f"Updating Starbound in {STARBOUND_INSTALL_DIR}...")
    else:
        log.info(f"Starbound is up to date in {STARBOUND_INSTALL_DIR}.")
        return

    steamcmd_command = [
        "steamcmd",
        "+force_install_dir",
        STARBOUND_INSTALL_DIR,
        "+login",
        STEAM_USER,
        "+app_update",
        STARBOUND_APP_ID,
        "validate",
        "+quit",
    ]

    result = run_command(steamcmd_command)
    if result.returncode != 0:
        if not already_installed:
            log.error("Failed to download Starbound server, exiting...")
        else:
            log.error("Failed to update Starbound server, exiting...")
        sys.exit(1)
    else:
        if not already_installed:
            log.info("Starbound server downloaded successfully.")
        else:
            log.info("Starbound server updated successfully.")


def ensure_starbound_packed_pak() -> None:
    starbound_assets_dir = os.path.join(STARBOUND_INSTALL_DIR, "assets")
    if not os.path.isdir(starbound_assets_dir):
        log.error("Starbound not found in {install_dir}.")
        sys.exit(1)

    starbound_packed_pak = os.path.join(starbound_assets_dir, "packed.pak")
    if os.path.isfile(starbound_packed_pak):
        log.debug("Starbound packed.pak already exists, nothing to do.")
        return

    log.info("Downloading Starbound packed.pak...")

    starbound_tmp_install_dir = "/tmp/starbound"

    steamcmd_command = [
        "steamcmd",
        "+force_install_dir",
        starbound_tmp_install_dir,
        "+login",
        STEAM_USER,
        "+app_update",
        STARBOUND_APP_ID,
        "validate",
        # download_depot never finishes :(
        # "+download_depot",
        # STARBOUND_APP_ID,
        # STARBOUND_DEPOT_ID,
        "+quit",
    ]

    result = run_command(steamcmd_command)
    if result.returncode != 0:
        log.error("Failed to download Starbound packed.pak, exiting...")
        sys.exit(1)
    else:
        log.info("Starbound packed.pak downloaded successfully.")

    starbound_tmp_packed_pak = os.path.join(
        starbound_tmp_install_dir, STARBOUND_PACKED_FILE_PATH
    )
    shutil.move(starbound_tmp_packed_pak, starbound_packed_pak)

    shutil.rmtree(starbound_tmp_install_dir)
    log.info("Starbound packed.pak moved to assets directory.")
