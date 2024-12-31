#!/usr/bin/env bash

declare -A downloaded_mods

download_workshop_item() {
  local workshop_item=$1
  modname="$(curl -s https://steamcommunity.com/sharedfiles/filedetails/?id="$workshop_item" | grep "<title>" | sed -e 's/<[^>]*>//g' | cut -d ' ' -f 4-)"
  modname_clean=$(echo "$modname" | dos2unix)
  counter=1
  printf "Downloading %s - %s \n" "$workshop_item" "$modname_clean"
  until steamcmd +workshop_download_item "$STARBOUND_APP_ID" "$workshop_item" validate +quit; do
    printf "Error Downloading %s - %s. Will try again \n" "$workshop_item" "$modname_clean"
    counter++
    if ((counter > 4)); then
      printf "Failed to download %s - %s \n" "$workshop_item" "$modname_clean"
      exit 1
    fi
  done
  if [ ! -L "$STARBOUND_MODS_DIR/$workshop_item" ]; then
    ln -s "$HOME/.steam/steamapps/workshop/content/$STARBOUND_APP_ID/$workshop_item/" "$STARBOUND_MODS_DIR/$workshop_item"
  fi
  downloaded_mods[$workshop_item]=1
}

if [ -n "$WORKSHOP_COLLECTION_IDS" ]; then
  for collection_id in $WORKSHOP_COLLECTION_IDS; do
    mapfile -t WORKSHOP_IDS < <(curl -s https://steamcommunity.com/sharedfiles/filedetails/?id="${collection_id}" | grep "https://steamcommunity.com/sharedfiles/filedetails/?id=" | grep -Eoi '<a [^>]+>' | tail -n +2 | grep -Eo 'href="[^\"]+"' | awk -F'"' '{ print $2 }' | awk -F'=' '{ print $2 }')
    for workshop_item in "${WORKSHOP_IDS[@]}"; do
      if [ -z "${downloaded_mods[$workshop_item]}" ]; then
        download_workshop_item "$workshop_item"
      fi
    done
  done
fi

if [ -n "$WORKSHOP_ITEM_IDS" ]; then
  for workshop_item in $WORKSHOP_ITEM_IDS; do
    if [ -z "${downloaded_mods[$workshop_item]}" ]; then
      download_workshop_item "$workshop_item"
    fi
  done
fi
