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

from six import text_type


class ANSI(object):
    GREEN           = '\033[32m'
    YELLOW          = '\033[93m'
    RED             = '\033[91m'
    COURSE          = '\033[94m'
    MODULE          = '\033[31m'
    FILE            = '\033[93m'
    PAGE            = '\033[96m'
    EXTERNALURL     = '\033[35m'
    ASSIGNMENT      = '\033[33m'
    WHITE           = ''
    ASSIGNMENTS     = '\033[37m'
    SUBHEADER       = '\033[34m'
    FOLDER          = '\033[93m'
    BLUE            = '\033[36m'
    ANNOUNCER       = '\033[31m'
    ENDC            = '\033[0m'
    BOLD            = '\033[1m'
    UNDERLINE       = '\033[4m'
    LINE_UP         = '\033[F'

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

        # Convert to text
        text = text_type(text)

        return ANSI._get(formatting) + text + ANSI._get("end")
