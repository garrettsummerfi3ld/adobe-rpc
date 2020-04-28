from pypresence import Presence
import logging
import handler
import time
from pypresence.exceptions import InvalidID

# Client Setup
client_id = "482150417455775755"
rich_presence = Presence(client_id)

# Logging config
logging.basicConfig(level=logging.DEBUG, format=('%(asctime)s - %(levelname)s - ' +
                                                 '%(funcName)s - %(message)s'),
                    datefmt='%d-%m-%y %H:%M:%S')

def connect_loop(retries=0):
    # Attempts to find Discord
    logging.info("Connecting rich presence...")
    if retries < 10:
        # Retry limit of 10 attempts
        try:
            logging.info("Conneting to RPC...")
            rich_presence.connect()
            update_loop()
        except KeyError:
            logging.error(
                "Unable to connect to Discord! Is your Client ID correct?")
            raise SystemExit(1)
        except SystemExit:
            logging.error(
                "Something has seriously gone wrong, and to prevent any issues, this application is terminating. Look through logs and submit a bug report on GitHub for support.")
            exit()
        except:
            logging.error("Error connecting to Discord! Retrying...")
            retries += 1
            time.sleep(1)
            connect_loop(retries)
    else:
        logging.exception(
            "Failed to connect to Discord! Printing stacktrace and exiting...")
        raise SystemExit(1)


def update_loop():
    # Updates Discord of current activity
    start_time = int(time.time())
    # Sets startup time for the application
    try:
        while True:
            # Creates rpc_data dictionary to parse data to handle
            rpc_data = handler.get_rpc_update()
            # 'handler.py' data is imported into here
            rich_presence.update(state=rpc_data['state'],
                                 small_image=rpc_data['small_image'],
                                 large_image=rpc_data['large_image'],
                                 large_text=rpc_data['large_text'],
                                 small_text=rpc_data['small_text'],
                                 details=rpc_data['details'],
                                 start=start_time)
            logging.info("Updated Discord RPC Data:")
            logging.info("Large Text: " + str(rpc_data['large_text']))
            logging.info("Small Text: " + str(rpc_data['small_text']))
            logging.info("State: " + str(rpc_data['state']))
            logging.debug("Raw input into Discord RPC: " + str(rpc_data))

            time.sleep(10)
    except InvalidID:
        # When script has a bad Client ID
        logging.error(
            "Unable to connect to Discord! Is your Client ID correct?")
        raise SystemExit(1)
    except:
        # When either Discord or a supported Adobe product is not detected...
        # Clear rpc_data
        rich_presence.clear()
        logging.exception(
            "Not detecting Adobe applications! Are you sure your running a compatible application?")
        # Update Discord
        time.sleep(1)
        update_loop()

if __name__ == "__main__":
    # Main instance
    try:
        logging.info("Started Adobe RPC!")
        connect_loop()
    except:
        rich_presence.close()
        logging.info("Stopped Adobe RPC!")
