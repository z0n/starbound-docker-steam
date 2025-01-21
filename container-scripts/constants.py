import logging
import os
import sys

log = logging.getLogger(__name__)


def _get_env_var(var_name: str, fallback: str | None = None) -> str:
    var = os.getenv(var_name, fallback)
    if var is None:
        log.error(f"{var_name} environment variable is not set. Exiting...")
        sys.exit(1)
    return var


STEAM_USER = _get_env_var("STEAM_USER")
STARBOUND_INSTALL_DIR = _get_env_var("STARBOUND_INSTALL_DIR")
STARBOUND_MODS_DIR = _get_env_var("STARBOUND_MODS_DIR")
STARBOUND_APP_ID = _get_env_var("STARBOUND_APP_ID")
STARBOUND_PACKED_FILE_PATH = _get_env_var("STARBOUND_PACKED_FILE_PATH")
OPEN_STARBOUND_VERSION_FILE = _get_env_var("OPEN_STARBOUND_VERSION_FILE")
OPEN_STARBOUND_GITHUB_REPO_NAME = _get_env_var("OPEN_STARBOUND_GITHUB_REPO_NAME")
OPEN_STARBOUND_SERVER_ASSET_NAME = _get_env_var("OPEN_STARBOUND_SERVER_ASSET_NAME")
WORKSHOP_COLLECTION_IDS = _get_env_var("WORKSHOP_COLLECTION_IDS", "").split()
WORKSHOP_ITEM_IDS = _get_env_var("WORKSHOP_ITEM_IDS", "").split()
USE_OPEN_STARBOUND = _get_env_var("USE_OPEN_STARBOUND", "false").lower() == "true"
CLEANUP_ORPHANS = _get_env_var("CLEANUP_ORPHANS", "false").lower() == "true"
