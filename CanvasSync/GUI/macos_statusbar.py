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
import configparser
import os.path
import datetime
import keyring
import pymsgbox


class config_file:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            open(self.filepath, 'a').close()
        self.config = configparser.ConfigParser()
        self.config.read(filepath)

    def read(self, section, parameter):
        if not self.config.has_option(section, parameter):
            return None
        else:
            return self.config[section][parameter]

    def write(self, section, parameter, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, parameter, value)
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)


from tkinter import *

def pop_up():
    app = Tk()
    app.title("CanvasSync Password")
    label = Label(app, text="Please enter the CanvasSync Password:")
    label.grid()
    pwd = StringVar()
    e1 = Entry(app, width=40, textvariable=pwd)
    btn = Button(app, text="Ok", command=app.destroy)
    btn.grid(row=2)
    e1.grid(row=1)

    app.mainloop()
    return pwd.get()

def savepassword():
    response = str(pop_up())
    keyring.set_password('CanvasSync', 'xkcd', response)


def changeSchedule(ToNew):
    """
    This function changes the scheduler settings file so that the selected interval in the settings file is saved there.
    Arguments:
        ToNew (str): The interval changed to/the new interval.
    """
    config.write('Settings', 'interval', ToNew)


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
    sys.path.insert(0, path)
    # Actual syncing
    import canvas
    settings = canvas.Settings()
    password = keyring.get_password('CanvasSync', 'xkcd')
    canvas.do_sync(settings, password)
    rumps.notification("Canvas Sync", "Finished Synchronisation", "The Manual Canvas-Sync-task was finished.")
    config.write('Last run', 'time', str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")))


@clicked("Preferences")
def sayhi(_):
    # Will be added later on
    rumps.alert("Not yet available! In next version...")


hourly = MenuItem('hourly', callback=adjust_interval)
every6 = MenuItem('every 6 hours', callback=adjust_interval)
daily = MenuItem('daily', callback=adjust_interval)
no_sync = MenuItem('Do not sync', callback=adjust_interval)

if __name__ == "__main__":
    if keyring.get_password('CanvasSync', 'xkcd') is None:
        savepassword()

    config = config_file(str(pathlib.Path(__file__).parent.parent) + "/scheduler/scheduler.ini")
    interval = config.read('Settings', 'interval')

    # Do not appear in Mac Dock
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSBackgroundOnly"] = "1"

    # Set Statusbar Properties
    app = App('Canvas Sync', icon='canvas_logo.png')
    app.menu = [("Sync now"), ("Automatic sync", [hourly, every6, daily, None, no_sync]), "Preferences"]
    path = str(pathlib.Path(__file__).parent.parent) + '/scheduler/scheduler.py'

    # Run Scheduler as independent subprocess
    #subprocess.run(["python", path])
    from subprocess import Popen, PIPE
    p = subprocess.Popen([sys.executable, path],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    # Get Current Sync-Setting from file and select the selected in Statusbar
    if not interval == None:
        app.menu["Automatic sync"][interval].state = 1

    # Run Statusbar
    app.run()
