from AppKit import NSWorkspace
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import applescript
import psutil
import json
import logging

with open('meta.json') as f:
    # Parses metadata for associated applications
    logging.debug("Loading 'meta.json'")
    data = json.load(f)

def get_process_info():
    # Process information of application
    logging.debug("Getting process information...")
    for element in data:
        # Finds process name for Adobe applications
        process_name = element['processNameMac']
        for process in psutil.process_iter():
            # Finds pid through iteration
            process_info = process.as_dict(attrs=['pid', 'name'])
            if process_info['name'].lower() in process_name:
                element['pid'] = process_info['pid']
                logging.debug("Process returns with info: " +
                            str(process_info))
                return element

def get_title(pid):
    # Processes title of application from PID
    logging.debug("Getting title for the application...")
    curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    curr_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
    curr_app_name = curr_app.localizedName()
    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in windowList:
        pid = window['kCGWindowOwnerPID']
        windowNumber = window['kCGWindowNumber']
        ownerName = window['kCGWindowOwnerName']
        geometry = window['kCGWindowBounds']
        windowTitle = window.get('kCGWindowName', u'Unknown')
        if curr_pid == pid:
            logging.debug("Title of application: " +  windowTitle.encode('ascii','ignore'))
            return windowTitle

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
            title_basename = ntpath.basename(
                title_seperated[app_info['splitIndex']])
            logging.debug("Returning the title of the project")
            return "{}: {}".format(app_info['smallText'], title_basename)
        else:
            return "{}: {}".format(app_info['smallText'], title_seperated[app_info['splitIndex']])
