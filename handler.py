import sys
import logging

def get_rpc_update():
    # Grabs data from applications
    logging.debug("Checking OS...")
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        # Windows data retrieval
        try:
            logging.debug("Importing Windows specific modules...")
            from api.windows import get_title, get_process_info, get_status

            app_info = get_process_info()

            if app_info != None:
                # Information to publically show to Discord
                app_title = get_title(app_info['pid'])
                app_state = get_status(app_info, app_title)

                # Dictionary setup to return application info
                rpc_update = {'state': app_state,
                            'small_image': app_info['smallImageKey'],
                            'large_image': app_info['largeImageKey'],
                            'large_text': app_info['largeText'],
                            'small_text': app_info['smallText'],
                            'details': app_info['largeText']}

                # Returns data from processing the application data
                return rpc_update

            # If 'get_process_info()' doesn't find a proper 'processName' element, stop application
            elif app_info == None:
                logging.error("Unable to find process")

        except ImportError:
            logging.error(
                "Required dependency is not found! Did install all dependencies? Check with the README")
            raise SystemExit(1)
        except TypeError:
            logging.error("No Adobe Applications running!")

    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        # macOS data retrieval
        try:
            logging.debug("Importing macOS specific modules...")
            from api.macos import get_title, get_process_info, get_status

            app_info = get_process_info()
            if app_info != None:
                # Information to publically show to Discord
                app_title = get_title(app_info['pid'])
                app_state = get_status(app_info, app_title)

                # Dictionary setup to return application info
                rpc_update = {'state': app_state,
                            'small_image': app_info['smallImageKey'],
                            'large_image': app_info['largeImageKey'],
                            'large_text': app_info['largeText'],
                            'small_text': app_info['smallText'],
                            'details': app_info['largeText']}

                # Returns data from processing the application data
                return rpc_update

            # If 'get_process_info()' doesn't find a proper 'processName' element, stop application
            elif app_info == None:
                logging.error("Unable to find process")

        except ImportError:
            logging.error(
                "Required dependency is not found! Did install all dependencies? Check with the README")
            raise SystemExit(1)
        except TypeError:
            logging.error("No Adobe Applications running!")

    else:
        logging.error("Unknown operating system! Exiting...")
        logging.error("If you believe this is an error. Submit a bug report.")
        raise SystemExit(0)

def exception_handler(exception, future):
    logging.exception("Something bad happened. Printing stacktrace...")