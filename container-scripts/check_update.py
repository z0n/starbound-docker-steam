import logging
import os

import requests

log = logging.getLogger(__name__)


def starbound_needs_update(install_dir: str, app_id: str) -> bool:
    try:
        response = requests.get(
            "https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/",
            params={"appid": app_id, "count": 1, "format": "json"},
        )
        response.raise_for_status()
        data = response.json()
        if (
            "appnews" not in data
            or "newsitems" not in data["appnews"]
            or not data["appnews"]["newsitems"]
            or "date" not in data["appnews"]["newsitems"][0]
        ):
            log.error("Invalid Steam API response while checking for Starbound update.")
            return False
        remote_timestamp = data["appnews"]["newsitems"][0]["date"]
        local_timestamp = os.path.getmtime(install_dir)
        if remote_timestamp > local_timestamp:
            log.info("New Starbound update available.")
        else:
            log.info("No new Starbound update available.")
        return remote_timestamp > local_timestamp
    except (requests.RequestException, KeyError, ValueError, OSError) as e:
        log.error(f"Error checking for Starbound updates: {e}")
        return False


def workshop_mod_needs_update(workshop_mod_id: str, app_id: str) -> bool:
    home_dir = os.path.expanduser("~")
    steam_workshop_dir = os.path.join(
        home_dir, "Steam/steamapps/workshop/content", app_id
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
            f"Error while checking for workshop mod {workshop_mod_id} update: {e}"
        )
        return False
