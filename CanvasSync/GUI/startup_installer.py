"""
This script is to add/remove the CanvasSync Statusbar in MacOS to the LaunchAgent so that is automatically starts at startup.
Run this file or the function ActivateStartUpStatusbar() to add it to startup.
Run the function DeactivateStartUpStatusbar() to remove it from startup.
"""

import pathlib
import os
import sys
import platform

def CreateStartupFile():
    with open(str(pathlib.Path(__file__).parent) + '/startup_template.plist', 'r') as file:
        script = str(file.read())

    script = script.replace('[@replaceCanvasPath]', str(pathlib.Path(__file__).parent))
    script = script.replace('[@replacePythonPath]', str(sys.executable))

    path_s = str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
    with open(path_s, 'w') as file:
        file.write(script)

def ActivateStartUpStatusbar():
    # ToDo: Somehow Batch Script to run at StartUp does not work.
    if platform.system() == 'Windows':
        path = str(pathlib.Path(__file__).parent) + '\windows_systemtray.py'
        startup_path = os.path.expanduser('~') + '\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\CanvasSync.bat'
        with open(startup_path, 'w+') as file:
            file.write(str('python "' + path + '"'))
    else: #MacOS
        CreateStartupFile()
        load_command = "launchctl load " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
        os.system(load_command)

def DeactivateStartUpStatusbar():
    if platform.system() == 'Windows':
        startup_path = os.path.expanduser('~') + '\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\CanvasSync.bat'
        os.remove(startup_path)
    else:  # MacOS
        unload_command = "launchctl unload " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
        stop_command = "launchctl stop " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
        os.system(unload_command)
        os.system(stop_command)


# If main module
if __name__ == u"__main__":
    ActivateStartUpStatusbar()
