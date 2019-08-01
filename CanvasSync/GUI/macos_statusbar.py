from rumps import *
import pathlib
import sys
import os


def adjust_interval(self):
    app.menu["Automatic sync"]['hourly'].state = 0
    app.menu["Automatic sync"]['every 6 hours'].state = 0
    app.menu["Automatic sync"]['daily'].state = 0
    app.menu["Automatic sync"]['Do not sync'].state = 0
    self.state = 1
    #pass

hourly = MenuItem('hourly', callback=adjust_interval)
every6 = MenuItem('every 6 hours', callback=adjust_interval)
daily = MenuItem('daily', callback=adjust_interval)
no_sync = MenuItem('Do not sync', callback=adjust_interval)


@clicked("Sync now")
def prefs(_):
    rumps.notification("Canvas Sync", "Syncing...", "The Canvas sync was started manually.")
    sys.path.insert(pathlib.Path(__file__).parent.parent + "/bin/")
    import canvas
    canvas.run_canvas_sync('-S')
    #print("run")

@clicked("Preferences")
def sayhi(_):
    rumps.alert("Not yet available! In next version...")


if __name__ == "__main__":
    app = App('Canvas Sync', icon='canvas_logo.png')
    app.menu = [("Sync now"),("Automatic sync",[hourly,every6,daily,None,no_sync]),"Preferences"]
    app.run()

