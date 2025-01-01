#!/usr/bin/env bash

declare -A downloaded_mods
steamcmd_command="steamcmd +login $STEAM_USER"

download_workshop_item() {
  local workshop_item=$1
  printf "Preparing to download %s \n" "$workshop_item"
  steamcmd_command+=" +workshop_download_item $STARBOUND_APP_ID $workshop_item"
  downloaded_mods[$workshop_item]=1
}

if [ -n "$WORKSHOP_COLLECTION_IDS" ]; then
  for collection_id in $WORKSHOP_COLLECTION_IDS; do
    if [[ "$collection_id" =~ ^[0-9]+$ ]]; then
      mapfile -t WORKSHOP_IDS < <(curl -s https://steamcommunity.com/sharedfiles/filedetails/?id="${collection_id}" | grep -oP 'id="sharedfile_\K\d+(?=" class="collectionItem")')
      for workshop_item in "${WORKSHOP_IDS[@]}"; do
        if [ -z "${downloaded_mods[$workshop_item]}" ]; then
          download_workshop_item "$workshop_item"
        fi
      done
    else
      echo "Skipping invalid collection ID: $collection_id"
    fi
  done
fi

if [ -n "$WORKSHOP_ITEM_IDS" ]; then
  for workshop_item in $WORKSHOP_ITEM_IDS; do
    if [[ "$workshop_item" =~ ^[0-9]+$ ]]; then
      if [ -z "${downloaded_mods[$workshop_item]}" ]; then
        download_workshop_item "$workshop_item"
      fi
    else
      echo "Skipping invalid workshop item ID: $workshop_item"
    fi
  done
fi

# Execute the steamcmd command to download all items at once
steamcmd_command+=" +quit"
echo "Downloading workshop items..."
eval $steamcmd_command

# Create symbolic links for downloaded mods
for workshop_item in "${!downloaded_mods[@]}"; do
  pak_file=$(find "$HOME/Steam/steamapps/workshop/content/$STARBOUND_APP_ID/$workshop_item/" -name "*.pak" -print -quit)
  if [ -n "$pak_file" ] && [ ! -L "$STARBOUND_MODS_DIR/$workshop_item.pak" ]; then
    ln -s "$pak_file" "$STARBOUND_MODS_DIR/$workshop_item.pak"
  fi
done

# Remove symlinks for items which are no longer in the downloaded mods
if [ "$CLEANUP_ORPHANS" = "true" ]; then
  for symlink in "$STARBOUND_MODS_DIR"/*.pak; do
    if [ -L "$symlink" ]; then
      workshop_item=$(basename "$symlink" .pak)
      if [ -z "${downloaded_mods[$workshop_item]}" ]; then
        echo "Removing orphaned symlink for $workshop_item"
        rm "$symlink"
      fi
    fi
  done
fi
