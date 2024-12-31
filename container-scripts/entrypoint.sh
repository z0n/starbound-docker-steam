#!/usr/bin/env bash

set -e

# Update/Download Starbound server
./update_starbound.sh

# Download workshop items
./download_workshop_items.sh

# Start Starbound server
./start_server.sh
