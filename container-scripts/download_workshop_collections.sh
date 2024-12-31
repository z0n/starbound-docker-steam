#!/usr/bin/env bash

declare -A downloaded_mods

download_workshop_item() {
  local workshop_item=$1
  modname="$(curl -s https://steamcommunity.com/sharedfiles/filedetails/?id="$workshop_item" | grep "<title>" | sed -e 's/<[^>]*>//g' | cut -d ' ' -f 4-)"
  modname_clean=$(echo "$modname" | dos2unix)
  counter=1
  printf "Downloading %s \n" "$modname_clean"
  until steamcmd +workshop_download_item 107410 "$workshop_item" validate +quit; do
    printf "Error Downloading %s. Will try again \n" "$modname_clean"
    counter++
    if ((counter > 4)); then
      exit 1
    fi
  done
  if [ ! -L "$STARBOUND_MODS_DIR/@$modname_clean" ]; then
    ln -s "$HOME/.steam/steamapps/workshop/content/107410/$workshop_item/" "$STARBOUND_MODS_DIR/@$modname_clean"
  fi
  downloaded_mods[$workshop_item]=1
}

if [ -n "$WSCOLLECTIONID" ]; then
  for collection_id in $WSCOLLECTIONID; do
    mapfile -t WS_IDS < <(curl -s https://steamcommunity.com/sharedfiles/filedetails/?id="${collection_id}" | grep "https://steamcommunity.com/sharedfiles/filedetails/?id=" | grep -Eoi '<a [^>]+>' | tail -n +2 | grep -Eo 'href="[^\"]+"' | awk -F'"' '{ print $2 }' | awk -F'=' '{ print $2 }')
    for workshop_item in "${WS_IDS[@]}"; do
      if [ -z "${downloaded_mods[$workshop_item]}" ]; then
        download_workshop_item "$workshop_item"
      fi
    done
  done
fi

if [ -n "$WSITEMIDS" ]; then
  for workshop_item in $WSITEMIDS; do
    if [ -z "${downloaded_mods[$workshop_item]}" ]; then
      download_workshop_item "$workshop_item"
    fi
  done
fi
