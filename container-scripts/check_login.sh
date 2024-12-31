#!/usr/bin/env bash

steamcmd +set_var @NoPromptForPassword 1 +set_var @ShutdownOnFailedCommand 1 +login $STEAM_USER +quit
exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo "Login successful."
else
  echo "Login failed. Please run the container with the \"login\" command to login."
fi
