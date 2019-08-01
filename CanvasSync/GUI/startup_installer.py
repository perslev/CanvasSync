import pathlib
import os

script = """"<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>my.python.script.name</string>
            <key>ProgramArguments</key>
            <array>
                <string>""" + str(pathlib.Path(__file__).parent) + """</string>
                <string>""" + str(pathlib.Path(__file__).parent) + "/macos_statusbar.py" + """</string>
            </array>
            <key>StandardErrorPath</key>
            <string>/var/log/python_script.error</string>
            <key>KeepAlive</key>
            <true/>
        </dict>
        </plist>"""




path = str(os.path.expanduser('~')) + "/Library/LaunchAgents/CanvasSyncStartUp.plist"
with open(path, 'w') as file:
    file.write(script)