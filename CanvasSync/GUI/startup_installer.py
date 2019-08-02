"""
This script is to add/remove the CanvasSync Statusbar in MacOS to the LaunchAgent so that is automatically starts at startup.
Run this file or the function ActivateStartUpStatusbar() to add it to startup.
Run the function DeactivateStartUpStatusbar() to remove it from startup.
"""

import pathlib
import os
import sys

def CreateStartupFile():
    with open(str(pathlib.Path(__file__).parent) + '/startup_template.plist', 'r') as file:
        script = str(file.read())

    script = script.replace('[@replaceCanvasPath]', str(pathlib.Path(__file__).parent))
    script = script.replace('[@replacePythonPath]', str(sys.executable))

    path_s = str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
    with open(path_s, 'w') as file:
        file.write(script)

def ActivateStartUpStatusbar():
    CreateStartupFile()
    load_command = "launchctl load " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
    os.system(load_command)

def DeactivateStartUpStatusbar():
    unload_command = "launchctl unload " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
    stop_command = "launchctl stop " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
    os.system(unload_command)
    os.system(stop_command)


# If main module
if __name__ == u"__main__":
    ActivateStartUpStatusbar()
