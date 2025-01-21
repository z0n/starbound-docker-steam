import logging

import requests
from constants import OPEN_STARBOUND_GITHUB_REPO_NAME, OPEN_STARBOUND_SERVER_ASSET_NAME

log = logging.getLogger(__name__)


def get_latest_release_tag() -> str:
    response = requests.get(
        f"https://api.github.com/repos/{OPEN_STARBOUND_GITHUB_REPO_NAME}/releases/latest",
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    response.raise_for_status()
    data = response.json()
    return data.get("tag_name")


def download_latest_release_asset(target_file_path: str) -> str:
    response = requests.get(
        f"https://api.github.com/repos/{OPEN_STARBOUND_GITHUB_REPO_NAME}/releases/latest",
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    response.raise_for_status()
    data = response.json()
    tag_name = data.get("tag_name")
    assets = data.get("assets", [])
    for asset in assets:
        if asset.get("name") == OPEN_STARBOUND_SERVER_ASSET_NAME:
            zip_url = asset.get("browser_download_url")
            break
    else:
        raise ValueError(
            f"{OPEN_STARBOUND_SERVER_ASSET_NAME} asset not found in the release."
        )
    log.info(
        f"Downloading {OPEN_STARBOUND_SERVER_ASSET_NAME} {tag_name} from {OPEN_STARBOUND_GITHUB_REPO_NAME}..."
    )
    zip_response = requests.get(zip_url)
    zip_response.raise_for_status()
    with open(target_file_path, "wb") as f:
        f.write(zip_response.content)
    return tag_name
