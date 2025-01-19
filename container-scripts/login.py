import logging
import sys

from run_shell_command import run_shell_command

log = logging.getLogger(__name__)


def login(steam_user: str) -> None:
    steamcmd_command = [
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

    result = run_shell_command(command=steamcmd_command, allowInput=True)
    if result.returncode != 0:
        log.error("Steam login failed, exiting...")
        sys.exit(1)
    else:
        log.info(
            "Steam login successful, you can now run the container without the 'login' command."
        )
        sys.exit(0)


def check_login(steam_user: str) -> None:
    steamcmd_command = [
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

    result = run_shell_command(command=steamcmd_command)

    if result.returncode != 0:
        log.error("Steam login failed, run the container with the 'login' command.")
        sys.exit(1)
    else:
        log.info("Steam login successful.")
