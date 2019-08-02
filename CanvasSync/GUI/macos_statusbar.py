"""
This script is the actual MacOS Statusbar for CanvasSync.
Execute this script to run the CanvasSync Statusbar.
Run startup_installer.py to add the CanvasSync Statsubar to the system StartUp.
"""
from rumps import *
import pathlib
import sys
import subprocess
import AppKit

def changeSchedule(ToNew):
    """
    This function changes the scheduler settings file so that the selected interval in the settings file is saved there.
    Arguments:
        ToNew (str): The interval changed to/the new interval.
    """
    path = str(pathlib.Path(__file__).parent.parent) + "/scheduler/scheduler.settings"
    with open(path, 'a') as file:
        file.write('\ninterval=' + ToNew)

def adjust_interval(self):
    # Change tick-mark in Statusbar on change
    app.menu["Automatic sync"]['hourly'].state = 0
    app.menu["Automatic sync"]['every 6 hours'].state = 0
    app.menu["Automatic sync"]['daily'].state = 0
    app.menu["Automatic sync"]['Do not sync'].state = 0
    self.state = 1
    # Save setting in Scheduler-Settings-File
    if self.title == 'hourly':
        changeSchedule('hourly')
    elif self.title == 'every 6 hours':
        changeSchedule('every 6 hours')
    elif self.title == 'daily':
        changeSchedule('daily')
    elif self.title == 'Do not sync':
        changeSchedule('Do not sync')


@clicked("Sync now")
def prefs(_):
    # Manual Sync now
    rumps.notification("Canvas Sync", "Syncing...", "The Canvas sync was started manually.")
    # Add folder of canvas module to search directory
    path = str(pathlib.Path(__file__).parent.parent.parent) + "/bin/"
    sys.path.insert(0,path)
    # Actual syncing
    import canvas
    settings = canvas.Settings()
    password = 'NotSafePassword'   # Later store password somewhere safe and make it adjustable
    canvas.do_sync(settings, password)
    rumps.notification("Canvas Sync", "Finished Synchronisation", "The Manual Canvas-Sync-task was finished.")


@clicked("Preferences")
def sayhi(_):
    # Will be added later on
    rumps.alert("Not yet available! In next version...")



hourly = MenuItem('hourly', callback=adjust_interval)
every6 = MenuItem('every 6 hours', callback=adjust_interval)
daily = MenuItem('daily', callback=adjust_interval)
no_sync = MenuItem('Do not sync', callback=adjust_interval)


if __name__ == "__main__":
    # Do not appear in Mac Dock
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSBackgroundOnly"] = "1"

    # Set Statusbar Properties
    app = App('Canvas Sync', icon='canvas_logo.png')
    app.menu = [("Sync now"),("Automatic sync",[hourly,every6,daily,None,no_sync]),"Preferences"]
    path = str(pathlib.Path(__file__).parent.parent) + '/scheduler/scheduler.py'

    # Run Scheduler as independent subprocess
    subprocess.Popen(["python", path])

    # Get Current Sync-Setting from file and select the selected in Statusbar
    with open(str(pathlib.Path(__file__).parent.parent) + "/scheduler/scheduler.settings") as f:
        contents = f.readlines()
        for content in contents:
            line = str(content).split("=")
            if line[0] == "interval":
                interval = line[1]
    app.menu["Automatic sync"][interval].state = 1

    # Run Statusbar
    app.run()



