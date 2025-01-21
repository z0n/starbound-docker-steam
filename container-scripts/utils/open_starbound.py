import logging
import os
import shutil
import sys
import tarfile
import zipfile

import requests
from constants import (
    OPEN_STARBOUND_SERVER_ASSET_NAME,
    OPEN_STARBOUND_VERSION_FILE,
    STARBOUND_INSTALL_DIR,
)
from utils.github import download_latest_release_asset, get_latest_release_tag

log = logging.getLogger(__name__)


def _open_starbound_needs_update() -> bool:
    if not os.path.isfile(OPEN_STARBOUND_VERSION_FILE):
        log.info(f"Version file not found in {OPEN_STARBOUND_VERSION_FILE}.")
        return True
    try:
        remote_version = get_latest_release_tag()
        local_version = None
        with open(OPEN_STARBOUND_VERSION_FILE, "r") as f:
            local_version = f.read().strip()
        if remote_version != local_version:
            log.info(
                f"New OpenStarbound update available: {remote_version} - Current version: {local_version}"
            )
        else:
            log.info("No new OpenStarbound update available.")
        return remote_version != local_version
    except (requests.RequestException, KeyError, ValueError, OSError) as e:
        log.error(f"Error checking for OpenStarbound updates: {e}", exc_info=True)
        return False


def update_open_starbound() -> None:
    already_installed = (
        os.path.isdir(STARBOUND_INSTALL_DIR)
        and os.listdir(STARBOUND_INSTALL_DIR)
        and os.path.isfile(os.path.join(STARBOUND_INSTALL_DIR, "assets/opensb.pak"))
    )
    needs_update = _open_starbound_needs_update() if already_installed else True
    if not already_installed:
        log.info(f"OpenStarbound not found in {STARBOUND_INSTALL_DIR}. Downloading...")
    elif needs_update:
        log.info(f"Updating OpenStarbound in {STARBOUND_INSTALL_DIR}...")
    else:
        log.info(f"OpenStarbound is up to date in {STARBOUND_INSTALL_DIR}.")
        return

    try:
        tmp_dir = "/tmp/openstarbound_download"
        target_file_path = os.path.join(tmp_dir, OPEN_STARBOUND_SERVER_ASSET_NAME)
        # Clean up any previous downloads
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)
        downloaded_tag_name = download_latest_release_asset(
            target_file_path=target_file_path
        )
        zip_path = os.path.join(tmp_dir, OPEN_STARBOUND_SERVER_ASSET_NAME)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)

        tar_path = os.path.join(tmp_dir, "server.tar")
        with tarfile.open(tar_path, "r") as tar_ref:
            for member in tar_ref.getmembers():
                log.info(f"Original member name: {member.name}...")
                if member.name.startswith("server_distribution/"):
                    member.name = member.name.replace("server_distribution/", "", 1)
                log.info(f"Extracting member: {member.name}...")
                tar_ref.extract(member, STARBOUND_INSTALL_DIR)

        with open(OPEN_STARBOUND_VERSION_FILE, "w") as version_file:
            version_file.write(downloaded_tag_name + "\n")

        shutil.rmtree(tmp_dir)

        log.info(
            f"OpenStarbound release {downloaded_tag_name} downloaded and extracted successfully."
        )
    except (
        requests.RequestException,
        KeyError,
        ValueError,
        OSError,
        zipfile.BadZipFile,
        tarfile.TarError,
    ) as e:
        log.error(
            f"Error downloading or extracting OpenStarbound release: {e}", exc_info=True
        )
        sys.exit(1)
