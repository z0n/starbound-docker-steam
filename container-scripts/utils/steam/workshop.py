import logging
import os
import re

import requests
from constants import (
    CLEANUP_ORPHANS,
    STARBOUND_APP_ID,
    STARBOUND_MODS_DIR,
    STEAM_USER,
    WORKSHOP_COLLECTION_IDS,
    WORKSHOP_ITEM_IDS,
)
from utils.shell import run_command

log = logging.getLogger(__name__)


def _workshop_mod_needs_update(workshop_mod_id: str) -> bool:
    home_dir = os.path.expanduser("~")
    steam_workshop_dir = os.path.join(
        home_dir, "Steam/steamapps/workshop/content", STARBOUND_APP_ID
    )
    mod_dir = os.path.join(steam_workshop_dir, workshop_mod_id)
    if not os.path.isdir(mod_dir):
        log.info(f"Mod {workshop_mod_id} not found in {mod_dir}.")
        return True
    try:
        response = requests.post(
            "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={"itemcount": "1", "publishedfileids[0]": workshop_mod_id},
        )
        response.raise_for_status()
        data = response.json()
        if (
            "response" not in data
            or "publishedfiledetails" not in data["response"]
            or not data["response"]["publishedfiledetails"]
            or "time_updated" not in data["response"]["publishedfiledetails"][0]
        ):
            log.error(
                f"Invalid Steam API response while checking for workshop mod {workshop_mod_id} update."
            )
            return False
        remote_timestamp = data["response"]["publishedfiledetails"][0]["time_updated"]
        local_timestamp = os.path.getmtime(mod_dir)
        if remote_timestamp > local_timestamp:
            log.info(f"Update for mod {workshop_mod_id} available.")
        else:
            log.info(f"Workshop mod {workshop_mod_id} is up to date.")
        return remote_timestamp > local_timestamp
    except (requests.RequestException, KeyError, ValueError, OSError) as e:
        log.error(
            f"Error while checking for workshop mod {workshop_mod_id} update: {e}",
            exc_info=True,
        )
        return False


def _fetch_workshop_ids_from_collection(collection_id: str):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={collection_id}"
    response = requests.get(url)
    pattern = r'id="sharedfile_(\d+)" class="collectionItem"'
    return re.findall(pattern, response.text)


def _download_workshop_items(workshop_ids: list[str]):
    steamcmd_cmd = ["steamcmd", "+login", STEAM_USER]
    for id in workshop_ids:
        if not _workshop_mod_needs_update(workshop_mod_id=id):
            continue
        steamcmd_cmd += ["+workshop_download_item", STARBOUND_APP_ID, id]
    steamcmd_cmd.append("+quit")
    run_command(steamcmd_cmd)


def _create_symlinks(downloaded_ids: set[str]):
    home_dir = os.path.expanduser("~")
    for item_id in downloaded_ids:
        path_to_pak = None
        content_dir = os.path.join(
            home_dir,
            "Steam/steamapps/workshop/content",
            str(STARBOUND_APP_ID),
            str(item_id),
        )
        for root, _, files in os.walk(content_dir):
            for f in files:
                if f.endswith(".pak"):
                    path_to_pak = os.path.join(root, f)
                    break
            if path_to_pak:
                break
        if path_to_pak:
            link_path = os.path.join(STARBOUND_MODS_DIR, f"{item_id}.pak")
            if not os.path.islink(link_path):
                os.symlink(path_to_pak, link_path)


def _cleanup_orphans(downloaded_ids: set[str]):
    for filename in os.listdir(STARBOUND_MODS_DIR):
        if filename.endswith(".pak"):
            link_path = os.path.join(STARBOUND_MODS_DIR, filename)
            if os.path.islink(link_path):
                wid = filename.rsplit(".pak", 1)[0]
                if wid not in downloaded_ids:
                    os.remove(link_path)


def download_workshop_items():
    downloaded_ids: set[str] = set()
    for collection_id in WORKSHOP_COLLECTION_IDS:
        if collection_id.isdigit():
            for item_id in _fetch_workshop_ids_from_collection(
                collection_id=collection_id
            ):
                downloaded_ids.add(item_id)
        else:
            log.warning(f"Skipping invalid collection ID: {collection_id}")

    for item_id in WORKSHOP_ITEM_IDS:
        if item_id.isdigit():
            downloaded_ids.add(item_id)
        else:
            log.warning(f"Skipping invalid item ID: {item_id}")

    if downloaded_ids:
        _download_workshop_items(workshop_ids=list(downloaded_ids))
        _create_symlinks(downloaded_ids=downloaded_ids)

    if CLEANUP_ORPHANS:
        _cleanup_orphans(downloaded_ids=downloaded_ids)
