# A Starbound Docker container with Steam workshop support

## Setup

Everything can be configured using the docker-compose.yml file.  

### Environment variables
| Variable                  | Usage                                                                                                                                                                                                    |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `STEAM_USER`              | Your Steam username (must own Starbound)                                                                                                                                                                 |
| `WORKSHOP_COLLECTION_IDS` | One or more Steam Workshop collection IDs, separated by space                                                                                                                                            |
| `WORKSHOP_ITEM_IDS`       | One or more Steam Workshop item IDs, separated by space                                                                                                                                                  |
| `CLEANUP_ORPHANS`         | If set to `true`, this will remove symlinks to workshop items which are no longer used, e.g. because it was removed from a collection or the item ID is no longer provided in the environment variables. |

### First time setup

#### Preparation
Update the environment variables in the docker-compose.yml file. At least the `STEAM_USER` is required. Remove the others if you don't need them.  
Configure the volume folders and make sure both folders can be written by the user in the container.  
The user in the container is using UID/GID 1001.

#### Logging into Steam
When running the container for the first time, you'll need to log into Steam. Your credentials will then be cached and used again later.

In the directory with the docker-compose.yml file, run `docker compose run starbound-server login`. If you're using podman, you can run `podman compose run starbound-server login` instead. 
This will trigger the login flow where you can enter your credentials into SteamCMD.  
You should now find some files in the folder of your steam volume. If not, check your folder permissions.

### Running the container
You should now be able to run the container in "normal" mode.  
For docker, run `docker compose up -d starbound-server`.  
For podman, you can run `podman compose up -d starbound-server` or use the included `starbound-server.container` quadlet file.  
If everything went fine, the server should start.

#### Updating
Currently, there is no auto-update mechanism included. One solution would be to restart the container at fixed times as everything (Starbound and Workshop items) are updated when the container starts.
