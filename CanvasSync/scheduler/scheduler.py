"""
This Script is the Scheduler for the automatic Canvas Sync. It constanly runs and checks every full hour if it needs to sync.
It checks it every hour because the user could have changed the settings inbetween the last and the current run.

ToDo:
- Password must be 'NotSafePassword' to work.
- At the moment when 'daily' is selected CanvasSync syncs at StartUp not just once daily.
"""
import datetime, time
import pathlib
import sys

# Import Canvas Module
path = str(pathlib.Path(__file__).parent.parent.parent) + "/bin/"
sys.path.insert(0, path)
import canvas


def runSync():
    settings = canvas.Settings()
    password = 'NotSafePassword'   # Later store password somewhere safe and make it adjustable
    canvas.do_sync(settings, password)


# The Check if has to sync
dailysync = False
while True:
    # read Config
    with open(str(pathlib.Path(__file__).parent) + "/scheduler.settings") as f:
        contents = f.readlines()
        for content in contents:
            line = str(content).split("=")
            if line[0] == "interval":
                interval = line[1]
    t = datetime.datetime.now()
    print(t)
    if interval == 'daily' and dailysync == False:
        runSync()
        dailysync = True
    elif interval == 'Do not sync':
        #do nothing
        pass
    if t.minute == 0 and t.second < 3:
        if interval == 'hourly':
            runSync()
        elif interval == 'every 6 hours' and t.hour % 6 == 0:
            runSync()
    else:
        # Calc time till next full hour and wait till then
        waitseconds = (60 - t.second) + (60 - t.minute - 1) * 60
        print(str(waitseconds))
        time.sleep(waitseconds)