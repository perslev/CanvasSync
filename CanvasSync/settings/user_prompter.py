"""
CanvasSync by Mathias Perslev
February 2017

---------------------------------------------

user_prompter.py, module

A collection of functions used to prompt the user for settings.

"""

# TODO
# - Comments
# - Make a Y/N function to reduce code redundancy

# Future
from __future__ import print_function

# Inbuilt modules
import glob
import os

# Check for UNIX or Windows platform
try:
    import readline
    unix = True
except ImportError:
    unix = False

# If python 2.7, use raw_input(), otherwise use input()
from six.moves import input

# CanvasSync module import
from CanvasSync.utilities import helpers
from CanvasSync.utilities.ANSI import ANSI


def show_main_screen(settings_file_exists):
    """
    Prompt the user for initial choice of action. Does not allow Synchronization before settings file has been set
    """

    choice = -1
    to_do = "quit"
    while choice not in (0, 1, 2, 3, 4):
        helpers.clear_console()

        # Load version string
        import CanvasSync
        version = CanvasSync.__version__

        title = u"CanvasSync, "
        pretty_string = u"-" * (len(title) + len(version))

        print(ANSI.format(u"%s\n%s%s\n%s" % (pretty_string, title, version, pretty_string), u"file"))

        print(ANSI.format(u"Automatically synchronize modules, assignments & files located on a Canvas web server.",
                          u"announcer"))
        print(ANSI.format(u"\nWhat would you like to do?", u"underline"))
        print(u"\n\t1) " + ANSI.format(u"Synchronize my Canvas", u"blue"))
        print(u"\t2) " + ANSI.format(u"Set new settings", u"white"))
        print(u"\t3) " + ANSI.format(u"Show current settings", u"white"))
        print(u"\t4) " + ANSI.format(u"Show help", u"white"))
        print(u"\n\t0) " + ANSI.format(u"Quit", u"yellow"))

        try:
            choice = int(input(u"\nChoose number: "))
            if choice < 0 or choice > 4:
                continue
        except ValueError:
            continue

        if choice == 1 and not settings_file_exists:
            to_do = u"set_settings"
        else:
            to_do = [u"quit", u"sync", u"set_settings", u"show_settings", u"show_help"][choice]

    return to_do


def ask_for_sync_path():
    """
    Prompt the user for a path to a folder that will be used to synchronize the Canvas page into
    The path should point into a directory along with a sub-folder name of a folder not already existing.
    This folder wll be created using the os module.
    """

    # Enable auto-completion of path and cursor movement using the readline and glob modules
    def path_completer(text, state):
        if u"~" in text:
            text = text.replace(u"~", os.path.expanduser(u"~"))

        paths = glob.glob(u"%s*" % text)
        paths.append(False)

        return os.path.abspath(paths[state]) + u'/'

    if unix:
        readline.set_completer_delims(u' \t\n;')
        readline.parse_and_bind(u"tab: complete")
        readline.set_completer(path_completer)

    found = False
    # Keep asking until a valid path has been entered by the user
    while not found:
        sync_path = input(u"\nEnter a relative or absolute path to sync to (~/Desktop/Canvas etc.):\n$ ")

        # Expand tilde if present in the sync_path
        if u"~" in sync_path:
            sync_path = sync_path.replace(u"~", os.path.expanduser(u"~"))
        sync_path = os.path.abspath(sync_path)

        if not os.path.exists(os.path.split(sync_path)[0]):
            print(u"\n[ERROR] Base path '%s' does not exist." % os.path.split(sync_path)[0])
        else:
            found = True

    if unix:
        # Disable path auto-completer
        readline.parse_and_bind(u'set disable-completion on')

    return sync_path


def ask_for_domain():
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
        domain = u"https://" + input(u"\nEnter the Canvas domain of your institution:\n$ https://")
        found = helpers.validate_domain(domain)

    return domain


def ask_for_token(domain):
    """
    Prompt the user for an authentication token.

    The token must be generated on the Canvas web page when login in under the "Settings" menu.
    To ensure that the entered token is valid, a request GET call is made on a resource that requires authentication
    on the server. If the server responds with the resource the token is valid.
    """
    found = False

    # Keep asking until a valid authentication token has been entered by the user
    while not found:
        token = input(u"\nEnter authentication token (see 'Setup' section on https://github.com/perslev/CanvasSync for details):\n$ ")
        found = helpers.validate_token(domain, token)

    return token


def ask_for_courses(settings, api):

    courses = api.get_courses()

    if settings.use_nicknames: 
        courses = [name[u"name"] for name in courses]
    else:
        courses = [name[u"course_code"].split(";")[-1] for name in courses]

    choices = [True]*len(courses)

    choice = -1
    while choice != 0:
        settings.print_settings(clear=True)
        print(ANSI.format(u"\n\nPlease choose which courses you would like CanvasSync to sync for you:\n", u"white"))

        print(ANSI.format(u"Sync this item\tNumber\tCourse Title", u"blue"))
        for index, course in enumerate(courses):
            print(u"%s\t\t[%s]\t%s" % (ANSI.format(str(choices[index]), u"green" if choices[index] else u"red"),
                                          index+1, courses[index]))
        print(u"\n\n\t\t[%s]\t%s" % (0, ANSI.format(u"Confirm selection (at least one course required)", "blue")))
        print(u"\t\t[%s]\t%s" % (-1, ANSI.format(u"Select all", u"green")))
        print(u"\t\t[%s]\t%s" % (-2, ANSI.format(u"Deselect all", u"red")))

        try:
            choice = int(input(u"\nChoose number: "))
            if choice < -2 or choice > len(courses):
                continue
        except ValueError:
            continue

        if choice == 0:
            if sum(choices) == 0:
                choice = -1
                continue
            else:
                break
        elif choice == -1:
            choices = [True] * len(courses)
        elif choice == -2:
            choices = [False] * len(courses)
        else:
            choices[choice-1] = choices[choice-1] is not True

    print(choices)

    return [x for index, x in enumerate(courses) if choices[index]]


def ask_for_advanced_settings(settings):
    choice = -1
    while choice not in (1, 2):
        settings.print_settings(clear=True)

        print(ANSI.format(u"\n\nAll mandatory settings are set. Do you wish see advanced settings?",
                          u"announcer"))

        print(ANSI.format(u"\n[1]\tShow advanced settings (recommended)", u"bold"))
        print(ANSI.format(u"[2]\tUse default settings", u"bold"))

        try:
            choice = int(input(u"\nChoose number: "))
        except ValueError:
            continue

        if choice == 1:
            return True
        elif choice == 2:
            return False
        else:
            continue


def ask_for_module_settings(module_settings, settings):
    choice = -1
    while choice != 0:
        settings.print_advanced_settings(clear=True)
        print(ANSI.format(u"\n\nModule settings", u"announcer"))
        print(ANSI.format(u"In Canvas, 'Modules' may contain various items such as files, HTML pages of\n"
                          u"exercises or reading material as well as links to external web-pages.\n\n"
                          u"Below you may specify, if you would like CanvasSync to avoid syncing some of these items.\n"
                          u"OBS: If you chose 'False' to all items, Modules will be skipped all together.", u"white"))

        print(ANSI.format(u"\nSync this item\tNumber\t\tItem", u"blue"))

        list_of_keys = list(module_settings.keys())
        for index, item in enumerate(list_of_keys):

            boolean = module_settings[item]

            print(u"%s\t\t[%s]\t\t%s" % (ANSI.format(str(boolean), u"green"
                                        if boolean else u"red"),
                                        index+1, item))

        print(u"\n\t\t[%s]\t\t%s" % (0, ANSI.format(u"Confirm selection", u"blue")))

        try:
            choice = int(input(u"\nChoose number: "))
            if choice < 0 or choice > len(module_settings):
                continue
        except ValueError:
            continue

        if choice == 0:
            break
        else:
            module_settings[list_of_keys[choice-1]] = module_settings[list_of_keys[choice-1]] is not True

    return module_settings


def ask_for_assignment_sync(settings):
    choice = -1

    while choice not in (1, 2):
        settings.print_advanced_settings(clear=True)
        print(ANSI.format(u"\n\nAssignments settings", u"announcer"))
        print(ANSI.format(u"Would you like CanvasSync to synchronize assignments?\n\n"
                          u"The assignment description will be downloaded as a HTML to be viewed offline\n"
                          u"and files hosted on the Canvas server that are described in the assignment\n"
                          u"description section will be downloaded to the same folder.\n", u"white"))

        print(ANSI.format(u"1) Sync assignments (default)", u"bold"))
        print(ANSI.format(u"2) Do not sync assignments", u"bold"))

        try:
            choice = int(input(u"\nChoose number: "))
        except ValueError:
            continue

        if choice == 1:
            return True
        elif choice == 2:
            return False
        else:
            continue


def ask_for_download_linked(settings):
    choice = -1

    while choice not in (1, 2):
        settings.print_advanced_settings(clear=True)
        print(ANSI.format(u"\n\nAssignments settings", u"announcer"))
        print(ANSI.format(u"You have chosen to synchronise assignments. URLs detected in the\n"
                          u"description field that point to files on Canvas will be downloaded\n"
                          u"to the assignment folder.\n\n"
                          u"CanvasSync may also attempt to download linked files that are NOT\n"
                          u"hosted on the Canvas server itself. CanvasSync is looking for URLs that\n"
                          u"end in a filename to avoid downloading other linked material such as\n"
                          u"web-sites. However, be aware that errors could occur.\n"
                          u"\nDo you wish to enable this feature?\n", u"white"))

        print(ANSI.format(u"1) Enable linked file downloading (default)", u"bold"))
        print(ANSI.format(u"2) Disable linked file downloading", u"bold"))

        try:
            choice = int(input(u"\nChoose number: "))
        except ValueError:
            continue

        if choice == 1:
            return True
        elif choice == 2:
            return False
        else:
            continue


def ask_for_avoid_duplicates(settings):
    choice = -1

    while choice not in (1, 2):
        settings.print_advanced_settings(clear=True)
        print(ANSI.format(u"\n\nVarious files settings", u"announcer"))
        print(ANSI.format(u"In addition to synchronizing modules and assignments,\n"
                          u"CanvasSync will sync files located under the 'Files'\n"
                          u"section in Canvas into a 'Various Files' folder.\n"
                          u"Often some of the files stored under 'Files' is mentioned in\n"
                          u"modules and assignments and may thus already exist in another\n"
                          u"folder after running CanvasSync.\n\n"
                          u"Do you want CanvasSync to avoid duplicates by only downloading\n"
                          u"files into the 'Various Files' folder, if they are not already\n"
                          u"present in one of the modules or assignments folders?\n", u"white"))

        print(ANSI.format(u"1) Yes, avoid duplicates (default)", u"bold"))
        print(ANSI.format(u"2) No, download all files to 'Various files'", u"bold"))

        try:
            choice = int(input(u"\nChoose number: "))
        except ValueError:
            continue

        if choice == 1:
            return True
        elif choice == 2:
            return False
        else:
            continue
