from rumps import *
import pathlib
import sys
import subprocess
import datetime, time

def changeScheduel(ToNew):
    path = str(pathlib.Path(__file__).parent.parent) + "/scheduler/scheduler.settings"
    with open(path, 'a') as file:
        file.write('\ninterval=' + ToNew)

def adjust_interval(self):
    app.menu["Automatic sync"]['hourly'].state = 0
    app.menu["Automatic sync"]['every 6 hours'].state = 0
    app.menu["Automatic sync"]['daily'].state = 0
    app.menu["Automatic sync"]['Do not sync'].state = 0
    self.state = 1
    if self.title == 'hourly':
        changeScheduel('hourly')
    elif self.title == 'every 6 hours':
        changeScheduel('every 6 hours')
    elif self.title == 'daily':
        changeScheduel('daily')
    elif self.title == 'Do not sync':
        changeScheduel('Do not sync')
    #pass

hourly = MenuItem('hourly', callback=adjust_interval)
every6 = MenuItem('every 6 hours', callback=adjust_interval)
daily = MenuItem('daily', callback=adjust_interval)
no_sync = MenuItem('Do not sync', callback=adjust_interval)


@clicked("Sync now")
def prefs(_):
    rumps.notification("Canvas Sync", "Syncing...", "The Canvas sync was started manually.")
    path = str(pathlib.Path(__file__).parent.parent.parent) + "/bin/"
    #print(str(path))
    sys.path.insert(0,path)
    import canvas
    settings = canvas.Settings()
    password = True #Later store password somewhere safe
    canvas.do_sync(settings, 'testPassword')
    rumps.notification("Canvas Sync", "Finished Synchronisation", "The Manual Canvas-Sync-task was finished.")

@clicked("Preferences")
def sayhi(_):
    rumps.alert("Not yet available! In next version...")


if __name__ == "__main__":
    app = App('Canvas Sync', icon='canvas_logo.png')
    app.menu = [("Sync now"),("Automatic sync",[hourly,every6,daily,None,no_sync]),"Preferences"]
    path = str(pathlib.Path(__file__).parent.parent) + '/scheduler/scheduler.py'
    #print(path)
    subprocess.Popen(["python", path])
    with open(str(pathlib.Path(__file__).parent.parent) + "/scheduler/scheduler.settings") as f:
        contents = f.readlines()
        for content in contents:
            line = str(content).split("=")
            if line[0] == "interval":
                interval = line[1]
    app.menu["Automatic sync"][interval].state = 1
    app.run()



