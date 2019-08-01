import datetime, time
import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent) + "/bin/"
sys.path.insert(0, path)
import canvas

def runSync():
    settings = canvas.Settings()
    password = True #Later store password somewhere safe
    canvas.do_sync(settings, 'testPassword')


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
        waitseconds = (60 - t.second) + (60 - t.minute - 1) * 60
        print(str(waitseconds))
        time.sleep(waitseconds)