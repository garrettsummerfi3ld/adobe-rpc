import win32gui
import win32process
import psutil
import json
import ntpath
import logging

with open('meta.json') as f:
    # Parses metadata for associated applications
    logging.debug("Loading 'meta.json'")
    data = json.load(f)

def get_process_info():
    # Retrieves pid of listed Adobe Application
    logging.debug("Getting process information...")
    for element in data:
        # Finds process name for Adobe applications
        process_name = element['processNameWin']
        logging.debug("Loading Process names for Windows...")
        for process in psutil.process_iter():
            # Finds pid through iteration
            process_info = process.as_dict(attrs=['pid', 'name'])
            logging.debug("Found proc '%s' at pid '%s'" % (process_info['name'],process_info['pid']))
            if process_info['name'].lower() in process_name:
                # If the process name is listed in the 'meta.json', set process_info to element and return the element
                element['pid'] = process_info['pid']
                logging.debug("Found Adobe process '%s' at pid '%s'" % (process_info['name'],process_info['pid']))
                return element

def get_title(pid):
    # Processes title of application from pid
    logging.debug("Getting title for the application...")

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    window_title = win32gui.GetWindowText(hwnds[-1])
    logging.debug("Title of application: " + window_title)
    return window_title

def get_status(app_info, title):
    # Status of application
    if app_info['largeText'].lower() in title.lower() and app_info['splitBy'] != " - ":
        # Idle detection
        logging.debug("Returning to Discord that you are detected as idle...")
        return "{}: IDLE".format(app_info['smallText'])
    else:
        # Project detection
        logging.debug("Not idling! Finding project...")
        title_seperated = title.split(app_info['splitBy'])
        if app_info['splitBy'] == " - ":
            try:
                title_basename = ntpath.basename(
                    title_seperated[app_info['splitIndex']])
                logging.debug("Returning the title of the project")
                return "{}: {}".format(app_info['smallText'], title_basename)
            except:
                logging.error("Something bad happened, did you not select a project?")
                return "{}: {}".format("IDLE", "Waiting for a project")
        else:
            return "{}: {}".format(app_info['smallText'], title_seperated[app_info['splitIndex']])
