#!/usr/bin/env bash

steamcmd +set_var @NoPromptForPassword 0 +set_var @ShutdownOnFailedCommand 0 +login $STEAM_USER +quit

if [ $? -ne 0 ]; then
  echo "Failed to login to Steam. Exiting..."
  exit 1
else
  echo "Login successful, you can now start the container without the \"login\" command."
fi
