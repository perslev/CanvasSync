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
   The sub folder is generated and stores all synchronized courses_to_sync.
2) The domain of the Canvas web server.
3) An authentication token used to authenticate with the Canvas API. The token is generated on the Canvas web server
   after authentication under "Settings".

The Settings object will prompt the user for these settings through the set_settings method and write them to a hidden
file in the users home directory. The file is encrypted using a user-specified password. This password must be specified
whenever CanvasSync is launched. Encryption is implemented via the PyCrypto AES-256 encryption module. The password
is stored locally in a hashed format using the bcrypt module. At runtime, the hashed password is used to validate
the user input password.
"""

# TODO
# - Clean things
# - Implement ANKI.fomrat method instead of accessing the ANKI attributes directly
# - Make it possible reuse settings, so that you do not have to re-specify all settings to change a single one


# Inbuilt modules
import os
import sys

# CanvasSync modules
from CanvasSync.Settings.cryptography import encrypt, decrypt
from CanvasSync.Settings import user_prompter
from CanvasSync.Statics.instructure_api import InstructureApi
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Statics import static_functions


class Settings(object):
    def __init__(self):
        self.sync_path = "Not set"
        self.domain = "Not set"
        self.token = "Not set"
        self.courses_to_sync = ["Not set"]
        self.modules_settings = {"Files": True, "HTML pages": True, "External URLs": True}
        self.sync_assignments = True
        self.download_linked = True
        self.avoid_duplicates = True

        # Get the path pointing to the settings file.
        self.settings_path = os.path.abspath(os.path.expanduser("~") + "/.CanvasSync.settings")

        # Initialize user prompt class, used to get information from the user via the terminal
        self.api = InstructureApi(self)

    def settings_file_exists(self):
        """ Returns a boolean representing if the settings file has already been created on this machine """
        return os.path.exists(self.settings_path)

    def is_loaded(self):
        return self.sync_path != "Not set" and self.domain != "Not set" and self.token != "Not set" and self.courses_to_sync[0] != "Not set"

    def load_settings(self):
        """ Loads the current settings from the settings file and sets the attributes of the Settings object """
        encrypted_message = open(self.settings_path, "rb").read()
        messages = decrypt(encrypted_message).split("\n")

        # Set sync path, domain and auth token
        self.sync_path, self.domain, self.token = messages[:3]

        if not static_functions.validate_token(self.domain, self.token):
            print "\n[ERROR] The authentication token has been reset, you must generate a new on the canvas webpage and reset\n" \
                  "the CanvasSync settings using the -s or --setup command line arguments"
            sys.exit()

        # Extract synchronization settings
        for message in messages:
            if message[:12] == "SYNC COURSE$":
                if self.courses_to_sync[0] == "Not set":
                    self.courses_to_sync.pop(0)
                self.courses_to_sync.append(message.split("$")[-1])

            if message[:6] == "Files$":
                self.modules_settings["Files"] = True if message.split("$")[-1] == "True" else False

            if message[:11] == "HTML pages$":
                self.modules_settings["HTML pages"] = True if message.split("$")[-1] == "True" else False

            if message[:14] == "External URLs$":
                self.modules_settings["External URLs"] = True if message.split("$")[-1] == "True" else False

            if message[:12] == "Assignments$":
                self.sync_assignments = True if message.split("$")[-1] == "True" else False

            if message[:13] == "Linked files$":
                self.download_linked = True if message.split("$")[-1] == "True" else False

            if message[:17] == "Avoid duplicates$":
                self.avoid_duplicates = True if message.split("$")[-1] == "True" else False

    def set_settings(self):
        """
        Prompt the user for settings and write the information to a hidden file in the users home directory.
        """

        # Clear the console and print guidance
        self.print_settings(clear=True)

        # Prompt user for sync path
        self.sync_path = user_prompter.ask_for_sync_path()
        self.print_settings(clear=True)

        # Prompt user for domain
        self.domain = user_prompter.ask_for_domain()
        self.print_settings(clear=True)

        # Prompt user for auth token
        self.token = user_prompter.ask_for_token(domain=self.domain)
        self.print_settings(clear=True)

        # Prompt user for course sync selection
        self.courses_to_sync = user_prompter.ask_for_courses(self, api=self.api)
        self.print_settings(clear=True)

        # Ask user for advanced settings
        show_advanced = user_prompter.ask_for_advanced_settings(self)

        if show_advanced:
            self.modules_settings = user_prompter.ask_for_module_settings(self.modules_settings, self)

            self.sync_assignments = user_prompter.ask_for_assignment_sync(self)
            if not self.sync_assignments:
                self.download_linked = False
            else:
                self.download_linked = user_prompter.ask_for_download_linked(self)

            self.avoid_duplicates = user_prompter.ask_for_avoid_duplicates(self)

    def write_settings(self):
        self.print_settings(welcome=False, clear=True)
        self.print_advanced_settings(clear=False)
        print ANSI.format("\n\nThese settings will be saved", "announcer")

        # Write password encrypted settings to hidden file in home directory
        with open(self.settings_path, "w") as out_file:
            settings = self.sync_path + "\n" + self.domain + "\n" + self.token + "\n"

            for course in self.courses_to_sync:
                settings += "SYNC COURSE$" + course + "\n"

            settings += "Files$" + str(self.modules_settings["Files"]) + "\n"
            settings += "HTML pages$" + str(self.modules_settings["HTML pages"]) + "\n"
            settings += "External URLs$" + str(self.modules_settings["External URLs"]) + "\n"
            settings += "Assignments$" + str(self.sync_assignments) + "\n"
            settings += "Linked files$" + str(self.download_linked) + "\n"
            settings += "Avoid duplicates$" + str(self.avoid_duplicates)

            out_file.write(encrypt(settings))

    def print_advanced_settings(self, clear=True):
        """
        Print the advanced settings currently in memory.
        Clear the console first if specified by the 'clear' parameter
        """
        if clear:
            static_functions.clear_console()

        print ANSI.format("\nAdvanced settings", "announcer")

        module_settings_string = ANSI.BOLD + u"[*] Sync module items:        \t" + ANSI.ENDC

        count = 0
        for item in self.modules_settings:
            if self.modules_settings[item]:
                d = " & " if count != 0 else ""
                module_settings_string += d + ANSI.BLUE + item + ANSI.ENDC
                count += 1

        if count == 0:
            module_settings_string += ANSI.RED + "False" + ANSI.ENDC

        print module_settings_string
        print ANSI.BOLD + u"[*] Sync assignments:         \t" + ANSI.ENDC + (ANSI.GREEN if self.sync_assignments else ANSI.RED) + str(self.sync_assignments) + ANSI.ENDC
        print ANSI.BOLD + u"[*] Download linked files:    \t" + ANSI.ENDC + (ANSI.GREEN if self.download_linked else ANSI.RED) + str(self.download_linked) + ANSI.ENDC
        print ANSI.BOLD + u"[*] Avoid item duplicates:    \t" + ANSI.ENDC + (ANSI.GREEN if self.avoid_duplicates else ANSI.RED) + str(self.avoid_duplicates) + ANSI.ENDC

    def print_settings(self, welcome=True, clear=True):
        """ Print the settings currently in memory. Clear the console first if specified by the 'clear' parameter """
        if clear:
            static_functions.clear_console()

        if welcome:
            print ANSI.format("Welcome to CanvasSync!\nYou must specify at least the following settings"
                              " in order to run CanvasSync:\n", "announcer")
        else:
            print ANSI.format("-----------------------------", "file")
            print ANSI.format("CanvasSync - Current settings", "file")
            print ANSI.format("-----------------------------\n", "file")
            print ANSI.format("Standard settings", "announcer")


        print ANSI.BOLD + u"[*] Sync path:             \t" + ANSI.ENDC + ANSI.BLUE + self.sync_path + ANSI.ENDC
        print ANSI.BOLD + u"[*] Canvas domain:         \t" + ANSI.ENDC + ANSI.BLUE + self.domain + ANSI.ENDC
        print ANSI.BOLD + u"[*] Authentication token:  \t" + ANSI.ENDC + ANSI.BLUE + self.token + ANSI.ENDC

        if len(self.courses_to_sync) != 0:
            if self.courses_to_sync[0] == "Not set":
                d = ""
            else:
                d = "1) "
            print ANSI.BOLD + u"[*] Courses to be synced:  \t%s" % d + ANSI.ENDC + ANSI.BLUE + self.courses_to_sync[0] + ANSI.ENDC

            for index, course in enumerate(self.courses_to_sync[1:]):
                print u" "*27 + "\t%s) " % (index+2) + ANSI.BLUE + course + ANSI.ENDC
