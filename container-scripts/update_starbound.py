import logging
import os
import subprocess
import sys

from check_update import starbound_needs_update

log = logging.getLogger(__name__)


def update_starbound(install_dir: str, steam_user: str, app_id: str):
    already_installed = os.path.isdir(install_dir)
    needs_update = starbound_needs_update(install_dir=install_dir, app_id=app_id)
    if not already_installed:
        log.info(f"Starbound not found in {install_dir}. Downloading...")
    elif needs_update:
        log.info(f"Updating Starbound in {install_dir}...")
    else:
        log.info(f"Starbound is up to date in {install_dir}.")
        return

    steamcmd_command = [
        "steamcmd",
        "+force_install_dir",
        install_dir,
        "+login",
        steam_user,
        "+app_update",
        app_id,
        "validate",
        "+quit",
    ]

    result = subprocess.run(steamcmd_command)
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
