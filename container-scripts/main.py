import logging
import sys

from constants import USE_OPEN_STARBOUND, WORKSHOP_COLLECTION_IDS, WORKSHOP_ITEM_IDS
from utils.open_starbound import update_open_starbound
from utils.starbound import start_server, switch_starbound_distribution
from utils.steam.auth import check_login, login
from utils.steam.update import ensure_starbound_packed_pak, update_starbound
from utils.steam.workshop import download_workshop_items

log = logging.getLogger(__name__)


def main(should_login: bool = False) -> None:
    if should_login:
        login()
    else:
        # Check if the user is logged in
        check_login()

        if USE_OPEN_STARBOUND:
            log.info("Using OpenStarbound server.")

            # Switch to Open Starbound distribution
            switch_starbound_distribution(target_distribution="open")
            update_open_starbound()

            # Download the packed.pak file from Steam
            ensure_starbound_packed_pak()
        else:
            log.info("Using Steam Starbound server.")

            # Switch to Steam Starbound distribution
            switch_starbound_distribution(target_distribution="steam")

            # Check if the user is logged in
            check_login()

            # Download or update Starbound server
            update_starbound()

        # Download or update workshop items
        if WORKSHOP_COLLECTION_IDS or WORKSHOP_ITEM_IDS:
            download_workshop_items()

        # Start the Starbound server
        start_server()


if __name__ == "__main__":
    should_login = len(sys.argv) > 1 and sys.argv[1] == "login"

    logging.basicConfig(level=logging.INFO)

    main(should_login=should_login)
