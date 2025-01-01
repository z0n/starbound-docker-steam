#!/usr/bin/env bash

declare -A downloaded_mods
steamcmd_command="steamcmd +login $STEAM_USER"

# https://stackoverflow.com/a/3352015 🤯
trim() {
  local var="$*"
  (($#)) || read -r var
  # remove leading whitespace characters
  var="${var#"${var%%[![:space:]]*}"}"
  # remove trailing whitespace characters
  var="${var%"${var##*[![:space:]]}"}"
  printf '%s' "$var"
}

download_workshop_item() {
  local workshop_item=$1
  modname="$(curl -s https://steamcommunity.com/sharedfiles/filedetails/?id="$workshop_item" | grep "<title>" | sed -e 's/<[^>]*>//g' | sed -e 's/Steam Workshop:://' | trim)"
  modname_clean=$(echo "$modname" | dos2unix)
  printf "Preparing to download %s - %s \n" "$workshop_item" "$modname_clean"
  steamcmd_command+=" +workshop_download_item $STARBOUND_APP_ID $workshop_item"
  downloaded_mods[$workshop_item]=1
}

if [ -n "$WORKSHOP_COLLECTION_IDS" ]; then
  for collection_id in $WORKSHOP_COLLECTION_IDS; do
    mapfile -t WORKSHOP_IDS < <(curl -s https://steamcommunity.com/sharedfiles/filedetails/?id="${collection_id}" | grep -oP 'id="sharedfile_\K\d+(?=" class="collectionItem")')
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

# Execute the steamcmd command to download all items at once
steamcmd_command+=" +quit"
echo "Downloading workshop items..."
eval $steamcmd_command

# Create symbolic links for downloaded mods
for workshop_item in "${!downloaded_mods[@]}"; do
  if [ ! -L "$STARBOUND_MODS_DIR/$workshop_item" ]; then
    ln -s "$HOME/Steam/steamapps/workshop/content/$STARBOUND_APP_ID/$workshop_item/" "$STARBOUND_MODS_DIR/$workshop_item"
  fi
done
