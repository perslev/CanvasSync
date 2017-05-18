#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017

--------------------------------------------

CanvasSync.py, main module

Implements the main module of CanvasSync. This module initiates the top-level Synchronizer object with the
settings specified in the settings file. If no settings file can be found, the user is promoted to supply the
information.

The main module may take input from the command line and will act accordingly. Without command line arguments,
CanvasSync enter a main menu where the user is guided to either set settings, show previously set settings, show help,
quit of start the synchronization process.

The module takes the arguments -h or --help that will show a help screen and quit.
The module takes the arguments -i or --info that will show the currently logged settings from the settings file.
The module takes the arguments -s or --setup that will force CanvasSync to prompt the user for settings.

"""

# TODO
# - Make a more transparent and robust setup process, at the moment some hacks are used for CanvasSync to be stable in all
#   scenarious (to be able to handle events such as deleted settings files and/or password files etc.) - It works
#   but surely can be more elegant

# Future imports
from __future__ import print_function

# Inbuilt modules
import getopt
import os
import sys

# If python 2.7, use raw_input(), otherwise use input()
from six.moves import input

# CanvasSync modules
from CanvasSync.CanvasEntities.synchronizer import Synchronizer
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Settings.settings import Settings
from CanvasSync.Statics import static_functions
from CanvasSync.Statics.instructure_api import InstructureApi
from CanvasSync import usage

try:
    import requests
    import bcrypt
    import Crypto
except ImportError:
    print(u"\n [ERROR] Missing dependencies.\n"
          u"         Please install requests, py-bcrypt and pycrypto (alternatively use PIP to install CanvasSync)'")


def run_canvas_sync():
    """ Main CanvasSync function, reads arguments from the command line and initializes the program """

    # Get command line arguments (C-style)
    try:
        opts, args = getopt.getopt(sys.argv[1:], u"hsi", [u"help", u"setup", u"info"])
    except getopt.GetoptError as err:
        # print help information and exit
        print(err)
        usage.help()

    # Parse the command line arguments and act accordingly
    setup = False
    show_info = False
    if len(opts) != 0:
        for o, a in opts:
            if o in (u"-h", u"--help"):
                # Show help
                usage.help()

            elif o in (u"-s", u"--setup"):
                # Force re-setup
                setup = True

            elif o in (u"-i", u"--info"):
                # Show current settings
                show_info = True

            else:
                # Unknown option
                assert False, u"Unknown option specified, please refer to the --help section."

    # Initialize Settings object. This object will parse the settings file or generate a new one if one does not exist.
    settings = Settings()

    # If the settings file does not exist or the user promoted to re-setup, start prompting user for settings info.
    if setup:
        settings.set_settings()

    # If -i or --info was specified, show the current settings and EXIT
    if show_info:
        settings.show(quit=True)

    # If here, CanvasSync was launched without parameters, show main screen
    main_menu(settings)


def main_menu(settings):
    """ Main menu function, calss the settings.show_main_screen function and handles user response """
    to_do = settings.show_main_screen(settings.settings_file_exists())

    # Act according to the users input to the main menu function
    if to_do == u"quit":
        sys.exit()
    elif to_do == u"set_settings":
        settings.set_settings()
        main_menu(settings)
    elif to_do == u"show_settings":
        settings.show(quit=False)
        main_menu(settings)
    elif to_do == u"show_help":
        usage.help()
    else:
        # Initialize the Instructure Api object used to make API calls to the Canvas server
        valid_token = settings.load_settings()
        if not valid_token:
            settings.print_auth_token_reset_error()
            sys.exit()

        # Initialize the API object
        api = InstructureApi(settings)

        # Start Synchronizer with the current settings
        synchronizer = Synchronizer(settings=settings, api=api)
        synchronizer.sync()

        # If here, sync was completed, show prompt
        print(ANSI.format(u"\n\n[*] Sync complete", formatting=u"bold"))


# If main module
if __name__ == u"__main__":

    if os.name == u"nt":
        # Warn Windows users
        static_functions.clear_console()
        input(u"\n[OBS] You are running CanvasSync on a Windows operating system.\n"
                  u"      The application is not developed for Windows machines and may be\n"
                  u"      unstable. Some pretty output formatting and tab-autocompletion\n"
                  u"      is not supported... :-(\n"
                  u"\n    Anyway, hit enter to start.")

    try:
        run_canvas_sync()
    except KeyboardInterrupt:
        print(ANSI.format(u"\n\n[*] Synchronization interrupted", formatting=u"red"))
        sys.exit()
