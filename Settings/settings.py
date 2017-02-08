#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
settings.py, Class

The Settings object implements the functionality of setting the initial-launch settings and later loading these settings
These settings include:

1) A path to with synchronization will occur. The path must be pointing to a valid folder and contain a sub folder name.
   The sub folder is generated and stores all synchronized courses.
2) The domain of the Canvas web server.
3) An authentication token used to authenticate with the Canvas API. The token is generated on the Canvas web server
   after authentication under "Settings".

The Settings object will prompt the user for these settings through the set_settings method and write them to a hidden
file in the users home directory. The file is encrypted using a user-specified password. This password must be specified
whenever CanvasSync is launched. Encryption is implemented via the PyCrypto AES-256 encryption module. The password
is stored locally in a hashed format using the bcrypt module. At runtime, the hashed password is used to validate
the user input password.
"""

# Inbuilt modules
import os
import sys
import readline
import glob

# Third party modules
import requests

# CanvasSync modules
from CanvasSync.Settings.encrypt import encrypt, decrypt
from CanvasSync.Statics.ANSI import Colors
from CanvasSync.Statics import static_functions


class Settings(object):
    def __init__(self):
        self.sync_path_ = "Not set"
        self.domain_ = "Not set"
        self.token_ = "Not set"

        # Get the path pointing to the settings file.
        self.settings_path = os.path.abspath(os.path.expanduser("~") + "/.CanvasSync.settings")

    def settings_file_exists(self):
        """ Returns a boolean representing if the settings file has already been created on this machine """
        return os.path.exists(self.settings_path)

    def is_loaded(self):
        return self.sync_path_ != "Not set" and self.domain_ != "Not set" and self.token_ != "Not set"

    def load_settings(self):
        """ Loads the current settings from the settings file and sets the attributes of the Settings object """
        encrypted_message = open(self.settings_path, "rb").read()
        self.sync_path_, self.domain_, self.token_ = decrypt(encrypted_message).split("#SPLIT#")

        if not self.validate_token(self.token_):
            print "\n[ERROR] The authentication token has been reset, you must generate a new on the canvas webpage and reset\n" \
                  "the CanvasSync settings using the -s or --setup command line arguments"
            sys.exit()

    def set_settings(self):
        """
        Prompt the user for settings and write the information to a hidden file in the users home directory.
        """

        # Clear the console and print guidance
        static_functions.clear_console()
        print Colors.UNDERLINE + "\nPlease specify the following settings to use CanvasSync:\n" + Colors.ENDC
        self.print_settings(clear=False)

        # Prompt user for settings
        self.ask_for_sync_path()
        self.ask_for_domain()
        self.ask_for_token()

        # Write password encrypted settings to hidden file in home directory
        with open(self.settings_path, "w") as out_file:
            settings = self.sync_path_ + "#SPLIT#" + self.domain_ + "#SPLIT#" + self.token_
            out_file.write(encrypt(settings))

        # Print the finalized settings and prompt the user to start the sync (continuing)
        self.print_settings()
        raw_input("\nReady to sync, hit enter to start.")

    def ask_for_sync_path(self):
        """
        Prompt the user for a path to a folder that will be used to synchronize the Canvas page into
        The path should point into a directory along with a sub-folder name of a folder not already existing.
        This folder wll be created using the os module.
        """

        # Enable auto-completion of path and cursor movement using the readline and glob modules
        def path_completer(text, state):
            if "~" in text:
                text = text.replace("~", os.path.expanduser("~"))

            paths = glob.glob("%s*" % text)
            paths.append(False)

            return os.path.abspath(paths[state]) + '/'

        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(path_completer)

        found = False
        # Keep asking until a valid path has been entered by the user
        while not found:
            sync_path = raw_input("\nEnter a relative or absolute path to sync to (~/Desktop/Canvas etc.):\n$ ")

            # Expand tilde if present in the sync_path
            if "~" in sync_path:
                sync_path = sync_path.replace("~", os.path.expanduser("~"))
            sync_path = os.path.abspath(sync_path)

            # Check if the path already exists
            if os.path.exists(sync_path):
                print "\n[ERROR] The supplied path is a folder. A sub folder name must also be specified."
            elif not os.path.exists(os.path.split(sync_path)[0]):
                print "\n[ERROR] Base path '%s' does not exist." % os.path.split(sync_path)[0]
            else:
                found = True

        self.sync_path_ = sync_path

        # Disable path auto-completer
        readline.parse_and_bind('set disable-completion on')
        self.print_settings()

    def ask_for_domain(self):
        """
        Prompt the user for a Canvas domain.

        To ensure that the API calls are made on an encrypted SSL connection the initial 'https://' is pre-specified.
        To ensure that the user input is 1) a valid URL and 2) a URL representing a Canvas web server request is used
        to fetch a resources on the Canvas page. If the GET requests fails the URL was not valid. If the server returns
        a 404 unauthenticated error the domain is very likely to be a Canvas server, if anything else is returned the
        URL points to a correct URL that is not a Canvas server.
        """
        found = False

        # Keep asking until a valid domain has been entered by the user
        while not found:
            domain = "https://" + raw_input("\nEnter the Canvas domain of your institution:\n$ https://")
            found = self.validate_domain(domain)

        self.domain_ = domain
        self.print_settings()

    def ask_for_token(self):
        """
        Prompt the user for an authentication token.

        The token must be generated on the Canvas web page when login in under the "Settings" menu.
        To ensure that the entered token is valid, a request GET call is made on a resource that requires authentication
        on the server. If the server responds with the resource the token is valid.
        """
        found = False

        # Keep asking until a valid authentication token has been entered by the user
        while not found:
            token = raw_input("\nEnter authentication token (see help for details):\n$ ")
            found = self.validate_token(token)

        self.token_ = token
        self.print_settings()

    def validate_domain(self, domain):
        try:
            response = requests.get(domain + "/api/v1/courses", timeout=5).content
            if response == "{\"status\":\"unauthenticated\",\"errors\":[{\"message\":\"user authorisation required\"}]}":
                # If this response, the server exists and understands the API call but complains that the call was
                # not authenticated - the URL represents a Canvas server
                return True
            else:
                print "\n[ERROR] Not a valid Canvas web server. Wrong domain?"
                return False
        except Exception:
            print "\n[ERROR] Invalid domain."
            return False

    def validate_token(self, token):
        response = requests.get(self.domain_ + "/api/v1/courses", headers={'Authorization': "Bearer %s" % token}).content

        if "Invalid access token" in response:
            print "The server did not accept the authentication token."
            return False
        else:
            return True

    def print_settings(self, clear=True):
        """ Print the settings currently in memory. Clear the console first if specified by the 'clear' parameter """
        if clear:
            static_functions.clear_console()

        print Colors.BOLD + "[*] Sync path:             " + Colors.ENDC + Colors.BLUE + self.sync_path_ + Colors.ENDC
        print Colors.BOLD + "[*] Canvas domain:         " + Colors.ENDC + Colors.BLUE + self.domain_ + Colors.ENDC
        print Colors.BOLD + "[*] Authentication token:  " + Colors.ENDC + Colors.BLUE + self.token_ + Colors.ENDC
