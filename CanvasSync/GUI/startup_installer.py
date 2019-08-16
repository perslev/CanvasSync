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

def AddWinTaskScheduler(wkdir, command, enabled):
    import datetime
    import win32com.client

    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    # Create trigger
    #end_time = datetime.datetime.now()
    TASK_TRIGGER_TIME = 9
    trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
    #trigger.EndBoundary = end_time.isoformat()
    trigger.ExecutionTimeLimit = "PT5M"
    trigger.Id = "LogonTriggerId"
    import win32api
    user = win32api.GetUserName()
    trigger.UserId = user
    trigger.ExecutionTimeLimit = "P0M2DT0H0M"
    trigger.enabled = enabled

    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = 'DO NOTHING'
    action.Path = 'cmd.exe'
    action.Arguments = '/c "' + str(command) + '"'
    action.WorkingDirectory = str(wkdir)

    # Set parameters
    task_def.RegistrationInfo.Description = 'Run CanvasSync at System Startup'
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.Settings.Hidden = True

    # Register task
    # If task already exists, it will be updated
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        'CanvasSync',  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE)



def ActivateStartUpStatusbar():
    # ToDo: In Windows subpress feedback e.g. when asking if run this package that is not in PATH.
    if platform.system() == 'Windows':
        path = str(pathlib.Path(__file__).parent)
        AddWinTaskScheduler(path, r'python .\windows_systemtray.py -y', True)

    else: #MacOS
        CreateStartupFile()
        load_command = "launchctl load " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
        os.system(load_command)

def DeactivateStartUpStatusbar():
    if platform.system() == 'Windows':
        path = str(pathlib.Path(__file__).parent)
        AddWinTaskScheduler(path, r'python .\windows_systemtray.py -y', False)
    else:  # MacOS
        unload_command = "launchctl unload " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
        stop_command = "launchctl stop " + str(os.path.expanduser('~')) + "/Library/LaunchAgents/com.CanvasSync.Statusbar.plist"
        os.system(unload_command)
        os.system(stop_command)


# If main module
if __name__ == u"__main__":
    ActivateStartUpStatusbar()
