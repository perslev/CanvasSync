#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
ANSI.py, Class

A small helper-object that simply contains various ANSI escape sequences used to manipulate print statements in the
terminal window.
"""

class Colors(object):
    GREEN = u'\033[32m'
    YELLOW = u'\033[93m'
    COURSE = u'\033[94m'
    MODULE = u'\033[96m'
    ITEM = u'\033[93m'
    FOLDER = u'\033[95m'
    BLUE = u'\033[36m'
    RED = u'\033[91m'
    ENDC = u'\033[0m'
    BOLD = u'\033[1m'
    UNDERLINE = u'\033[4m'
    LINE_UP = u'\033[F'
