import logging
import os
import sys

from download_workshop_items import download_workshop_items
from login import check_login, login
from start_server import start_server
from update_starbound import update_starbound

log = logging.getLogger(__name__)


def _get_env_var(var_name: str, fallback: str | None = None) -> str:
    var = os.getenv(var_name, fallback)
    if not var:
        log.error(f"{var_name} environment variable is not set. Exiting...")
        sys.exit(1)
    return var


def main(steam_user: str, should_login: bool = False) -> None:
    if should_login:
        login(steam_user=steam_user)
    else:
        # Required environment variables
        starbound_app_id = _get_env_var("STARBOUND_APP_ID")
        starbound_install_dir = _get_env_var("STARBOUND_INSTALL_DIR")
        starbound_mods_dir = _get_env_var("STARBOUND_MODS_DIR")

        # Optional environment variables
        cleanup = _get_env_var("CLEANUP", "false").lower() == "true"
        workshop_collections = _get_env_var("WORKSHOP_COLLECTION_IDS", "").split()
        workshop_items = _get_env_var("WORKSHOP_ITEM_IDS", "").split()

        # Check if the user is logged in
        check_login(steam_user=steam_user)

        # Download or update Starbound server
        update_starbound(
            install_dir=starbound_install_dir,
            steam_user=steam_user,
            app_id=starbound_app_id,
        )

        # Download or update workshop items
        download_workshop_items(
            steam_user=steam_user,
            starbound_app_id=starbound_app_id,
            starbound_mods_dir=starbound_mods_dir,
            workshop_collection_ids=workshop_collections,
            workshop_item_ids=workshop_items,
            cleanup=cleanup,
        )

        # Start the Starbound server
        start_server(starbound_install_dir=starbound_install_dir)


if __name__ == "__main__":
    steam_user = _get_env_var("STEAM_USER")
    if not steam_user:
        log.error("STEAM_USER environment variable is not set. Exiting...")
        sys.exit(1)
    should_login = len(sys.argv) > 1 and sys.argv[1] == "login"

    logging.basicConfig(level=logging.INFO)

    main(steam_user=steam_user, should_login=should_login)
