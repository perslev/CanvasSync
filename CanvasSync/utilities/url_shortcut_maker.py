"""
CanvasSync by Mathias Perslev
February 2017

--------------------------------------------

url_shortcut_maker.py, module

A collection of functions that creates URL shortcuts based on the machine operating system
"""

import sys
import os


def _make_mac_url_shortcut(url, path):
    url_content = u"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>URL</key>
<string>%s</string>
</dict>
</plist>""" % url

    if not os.path.exists(path + u".webloc"):
        with open(path + u".webloc", u"w") as out_file:
            out_file.write(url_content)


def _make_linux_url_shortcut(url, path):
    name = os.path.split(url)[-1]
    url_content =u"""[Desktop Entry]
Encoding=UTF-8
Name=%s
Type=Link
URL=%s
Icon=text-html""" % (name, url)

    if not os.path.exists(path + u".desktop"):
        with open(path + u".desktop", u"w") as out_file:
            out_file.write(url_content)


def _make_windows_url_shortcut(url, path):
    url_content = u"""[InternetShortcut]
URL=%s""" % url

    if not os.path.exists(path + u".URL"):
        with open(path + u".URL", u"w") as out_file:
            out_file.write(url_content)


def make_url_shortcut(url, path):

    system = sys.platform.lower()

    if system == u"darwin":
        _make_mac_url_shortcut(url, path)
    elif u"linux" in system:
        _make_linux_url_shortcut(url, path)
    else:
        _make_windows_url_shortcut(url, path)
