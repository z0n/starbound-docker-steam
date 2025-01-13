import logging
import os
import sys

from check_update import starbound_needs_update
from run_shell_command import run_shell_command

log = logging.getLogger(__name__)


def update_starbound(install_dir: str, steam_user: str, app_id: str):
    already_installed = (
        os.path.isdir(install_dir)
        and os.listdir(install_dir)
        and os.path.isfile(os.path.join(install_dir, "linux/starbound_server"))
    )
    needs_update = (
        starbound_needs_update(install_dir=install_dir, app_id=app_id)
        if already_installed
        else True
    )
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

    result = run_shell_command(steamcmd_command)
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
