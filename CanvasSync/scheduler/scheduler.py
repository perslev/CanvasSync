"""
This Script is the Scheduler for the automatic Canvas Sync. It constanly runs and checks every full hour if it needs to sync.
It checks it every hour because the user could have changed the settings inbetween the last and the current run.
"""
import datetime, time
import pathlib
import sys
import configparser
import os.path
import keyring
import platform
#import pymsgbox

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


def runSync():
    print('sync')
    if keyring.get_password('CanvasSync', 'xkcd') == None:
        raise Exception("Error: Password for CanvasSync not saved in Keychain")
    settings = canvas.Settings()
    password = keyring.get_password('CanvasSync', 'xkcd')
    canvas.do_sync(settings, password)
    config.write('Last run', 'time', str(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")))


if __name__ == '__main__':
    # Import Canvas Module
    path = str(pathlib.Path(__file__).parent.parent.parent) + "/bin/"
    sys.path.insert(0, path)
    # Set workind dir for windows
    # ToDo: Check if still works with MacOS
    if platform.system() == 'Windows':
        os.chdir(path)
    import canvas

    # The Check if has to sync
    dailysync = False
    while True:
        # read Config
        config = config_file(str(pathlib.Path(__file__).parent) + "/scheduler.ini")
        interval = config.read('Settings', 'interval')
        print('interval ' + str(interval))
        last_sync = config.read('Last run', 'time')
        if last_sync == None:
            last_sync = '01.01.2000 01:01:01'
        last_sync = datetime.datetime.strptime(last_sync, "%d.%m.%Y %H:%M:%S")
        print('last sync ' + str(last_sync.strftime("%d.%m.%Y %H:%M:%S")))
        current_time = datetime.datetime.now()
        print('current time ' + str(current_time.strftime("%d.%m.%Y %H:%M:%S")))
        if interval == 'daily':
            next_sync = last_sync + datetime.timedelta(days=1)
        elif interval == 'Do not sync':
            #do nothing
            next_sync = last_sync + datetime.timedelta(hours=1)
            pass
        elif interval == 'hourly':
            next_sync = last_sync + datetime.timedelta(hours=1)
        elif interval == 'every 6 hours':
            next_sync = last_sync + datetime.timedelta(hours=6)
        else:
            next_sync = last_sync + datetime.timedelta(minutes=10)
        if next_sync < current_time and interval != 'Do not sync':
            runSync()
        else:
            print('next sync ' + str(next_sync.strftime("%d.%m.%Y %H:%M:%S")))
            # Calc time till next full hour and wait till then
            waitseconds = (next_sync - current_time).total_seconds()
            if waitseconds > 3600:
                waitseconds = 3600
            print('waiting ' + str(waitseconds) + ' seconds')
            time.sleep(waitseconds)