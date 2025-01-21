import logging
import sys

from constants import STEAM_USER
from utils.shell import run_command

log = logging.getLogger(__name__)


def login() -> None:
    steamcmd_command = [
        "steamcmd",
        "+set_var",
        "@NoPromptForPassword",
        "0",
        "+set_var",
        "@ShutdownOnFailedCommand",
        "0",
        "+login",
        STEAM_USER,
        "+quit",
    ]

    result = run_command(command=steamcmd_command, allowInput=True)
    if result.returncode != 0:
        log.error("Steam login failed, exiting...")
        sys.exit(1)
    else:
        log.info(
            "Steam login successful, you can now run the container without the 'login' command."
        )
        sys.exit(0)


def check_login() -> None:
    steamcmd_command = [
        "steamcmd",
        "+set_var",
        "@NoPromptForPassword",
        "1",
        "+set_var",
        "@ShutdownOnFailedCommand",
        "1",
        "+login",
        STEAM_USER,
        "+quit",
    ]

    result = run_command(command=steamcmd_command)

    if result.returncode != 0:
        log.error("Steam login failed, run the container with the 'login' command.")
        sys.exit(1)
    else:
        log.info("Steam login successful.")
