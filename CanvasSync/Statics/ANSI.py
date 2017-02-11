#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017

--------------------------------------------

ANSI.py, Class

A small helper-object containing various ANSI escape sequences used to manipulate print statements in the
terminal window.
"""


class ANSI(object):
    GREEN           = u'\033[32m'
    YELLOW          = u'\033[93m'
    RED             = u'\033[91m'
    COURSE          = u'\033[94m'
    MODULE          = u'\033[31m'
    FILE            = u'\033[93m'
    PAGE            = u'\033[96m'
    EXTERNALURL     = u'\033[35m'
    ASSIGNMENT      = u'\033[33m'
    WHITE           = u''
    ASSIGNMENTS     = u'\033[37m'
    SUBHEADER       = u'\033[34m'
    FOLDER          = u'\033[93m'
    BLUE            = u'\033[36m'
    ANNOUNCER       = u'\033[31m'
    ENDC            = u'\033[0m'
    BOLD            = u'\033[1m'
    UNDERLINE       = u'\033[4m'
    LINE_UP         = u'\033[F'

    esc_seq_dict = {"green": GREEN,
                    "yellow": YELLOW,
                    "blue": BLUE,
                    "red": RED,
                    "file": FILE,
                    "page": PAGE,
                    "externalurl": EXTERNALURL,
                    "course": COURSE,
                    "module": MODULE,
                    "linkedfile": COURSE,
                    "subheader": SUBHEADER,
                    "assignment": ASSIGNMENT,
                    "white": WHITE,
                    "folder": GREEN,
                    "announcer": ANNOUNCER,
                    "assignments": ASSIGNMENTS,
                    "lineup": LINE_UP,
                    "bold": BOLD,
                    "underline": UNDERLINE,
                    "end": ENDC}

    @staticmethod
    def _get(formatting):
        """ Return the ANSI escape sequence linked to a formatting string """
        return ANSI.esc_seq_dict[formatting.lower()]

    @staticmethod
    def format(text, formatting):
        """ Format a string of text using ANSI escape sequences """

        return ANSI._get(formatting) + text + ANSI._get("end")
