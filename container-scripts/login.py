import logging
import subprocess
import sys

log = logging.getLogger(__name__)


def login(steam_user: str) -> None:
    command = [
        "steamcmd",
        "+set_var",
        "@NoPromptForPassword",
        "0",
        "+set_var",
        "@ShutdownOnFailedCommand",
        "0",
        "+login",
        steam_user,
        "+quit",
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        log.error("Steam login failed, exiting...")
        sys.exit(1)
    else:
        log.info(
            "Steam login successful, you can now run the container without the 'login' command."
        )
        sys.exit(0)


def check_login(steam_user: str) -> None:
    command = [
        "steamcmd",
        "+set_var",
        "@NoPromptForPassword",
        "1",
        "+set_var",
        "@ShutdownOnFailedCommand",
        "1",
        "+login",
        steam_user,
        "+quit",
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        log.error("Steam login failed, run the container with the 'login' command.")
        sys.exit(1)
    else:
        log.info("Steam login successful.")
