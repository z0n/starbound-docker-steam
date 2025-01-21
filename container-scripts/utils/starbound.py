import logging
import os
import shutil
from typing import Literal

from constants import STARBOUND_INSTALL_DIR
from utils.shell import run_command

log = logging.getLogger(__name__)


def check_starbound_distribution() -> Literal["none", "open", "steam"]:
    if not os.path.isdir(STARBOUND_INSTALL_DIR):
        return "none"
    if os.path.isfile(os.path.join(STARBOUND_INSTALL_DIR, "assets/opensb.pak")):
        return "open"
    if os.path.isfile(os.path.join(STARBOUND_INSTALL_DIR, "linux/libsteam_api.so")):
        return "steam"
    return "none"


def switch_starbound_distribution(
    target_distribution: Literal["open", "steam"],
) -> None:
    current_distribution = check_starbound_distribution()
    if current_distribution == target_distribution:
        log.debug(f"Starbound is already set to {target_distribution} distribution.")
        return
    if current_distribution == "none":
        log.info("Starbound not found. Skipping distribution switch.")
        return
    for item in os.listdir(STARBOUND_INSTALL_DIR):
        if item not in ("mods", "steamapps", "storage"):
            path = os.path.join(STARBOUND_INSTALL_DIR, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    log.info(
        f'Switched Starbound distribution from "{current_distribution}" to "{target_distribution}".'
    )


def start_server():
    start_server_command = [
        os.path.join(STARBOUND_INSTALL_DIR, "linux", "starbound_server")
    ]

    os.chdir(os.path.join(STARBOUND_INSTALL_DIR, "linux"))
    run_command(command=start_server_command)
