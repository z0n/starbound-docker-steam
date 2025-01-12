import logging
import os
import re
import subprocess

import requests
from check_update import workshop_mod_needs_update

log = logging.getLogger(__name__)


def _fetch_workshop_ids_from_collection(collection_id: str):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={collection_id}"
    response = requests.get(url)
    pattern = r'id="sharedfile_(\d+)" class="collectionItem"'
    return re.findall(pattern, response.text)


def _download_workshop_items(
    steam_user: str, starbound_app_id: str, workshop_ids: list[str]
):
    steamcmd_cmd = ["steamcmd", "+login", steam_user]
    for id in workshop_ids:
        if not workshop_mod_needs_update(id, f"workshop/{id}.pak"):
            continue
        steamcmd_cmd += ["+workshop_download_item", starbound_app_id, id]
    steamcmd_cmd.append("+quit")
    subprocess.run(steamcmd_cmd, check=True)


def _create_symlinks(
    downloaded_ids: set[str], starbound_app_id: str, starbound_mods_dir: str
):
    home_dir = os.path.expanduser("~")
    for item_id in downloaded_ids:
        path_to_pak = None
        content_dir = os.path.join(
            home_dir,
            "Steam/steamapps/workshop/content",
            str(starbound_app_id),
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
            link_path = os.path.join(starbound_mods_dir, f"{item_id}.pak")
            if not os.path.islink(link_path):
                os.symlink(path_to_pak, link_path)


def _cleanup_orphans(downloaded_ids: set[str], starbound_mods_dir: str):
    for filename in os.listdir(starbound_mods_dir):
        if filename.endswith(".pak"):
            link_path = os.path.join(starbound_mods_dir, filename)
            if os.path.islink(link_path):
                wid = filename.rsplit(".pak", 1)[0]
                if wid not in downloaded_ids:
                    os.remove(link_path)


def download_workshop_items(
    steam_user: str,
    starbound_app_id: str,
    starbound_mods_dir: str,
    workshop_collection_ids: list[str] = [],
    workshop_item_ids: list[str] = [],
    cleanup: bool = False,
):
    downloaded_ids: set[str] = set()
    for collection_id in workshop_collection_ids:
        if collection_id.isdigit():
            for item_id in _fetch_workshop_ids_from_collection(
                collection_id=collection_id
            ):
                downloaded_ids.add(item_id)
        else:
            log.warning(f"Skipping invalid collection ID: {collection_id}")

    for item_id in workshop_item_ids:
        if item_id.isdigit():
            downloaded_ids.add(item_id)
        else:
            log.warning(f"Skipping invalid item ID: {item_id}")

    if downloaded_ids:
        _download_workshop_items(steam_user, starbound_app_id, list(downloaded_ids))
        _create_symlinks(downloaded_ids, starbound_app_id, starbound_mods_dir)

    if cleanup:
        _cleanup_orphans(downloaded_ids, starbound_mods_dir)
