#!/usr/bin/env bash

# Function to update or download Starbound server
update_starbound() {
  steamcmd +force_install_dir "$STARBOUND_INSTALL_DIR" +login $STEAM_USER +app_update "$STARBOUND_APP_ID" validate +quit
  if [ $? -ne 0 ]; then
    echo "Failed to update or download Starbound server."
    exit 1
  fi
}

# Check if Starbound is already installed
if [ ! -d "$INSTALL_DIR" ]; then
  echo "Starbound not found in $STARBOUND_INSTALL_DIR. Downloading..."
  mkdir -p "$STARBOUND_INSTALL_DIR"
  update_starbound
else
  echo "Updating Starbound in $STARBOUND_INSTALL_DIR..."
  update_starbound
fi

echo "Starbound server update/download complete."
