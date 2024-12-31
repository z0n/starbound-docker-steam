#!/usr/bin/env bash

set -e

if [ -z "$STEAM_USER" ]; then
  echo "STEAM_USER is not set. Exiting."
  exit 1
fi

if [ "$1" == "login" ]; then
  ./login.sh
  exit $?
fi

# Check if we're logged in
./check_login.sh

# Update/Download Starbound server
./update_starbound.sh

# Download workshop items
./download_workshop_items.sh

# Start Starbound server
./start_server.sh
