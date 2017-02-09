#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
Implements a class representing files not located on the Canvas server
Initialization of this object thus does not require a info dictionary as is the case for all classes representing true
Canvas entities. Instead, LinkedFile should be initialized with a direct download link.
However, the LinkedFile is derived from the base entity class and the walk, sync and show methods are implemented
and should be used in a similar fashion to other entity objects.
"""

# Inbuilt modules
import os
import sys

# Third party modules
import requests

# CanvasSync module imports
from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.Statics.ANSI import ANSI


class LinkedFile(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, download_url, parent):
        """
        Constructor method, initializes base Entity class

        assignment_info : dict   | A dictionary of information on the Canvas assignment object
        assignment_path : string | The path pointing to the assignment location in the local folder hierarchy
        parent          : object | The parent object, a course object
        """

        self.download_url = download_url
        self.valid_url = True

        # Get the potential file name from the URL
        # OBS: We do not correct the name in this class, as we need to use the length of the name to determine
        # if the link is valid.
        file_name = os.path.split(download_url)[-1]

        # File path
        file_path = parent.get_path() + file_name

        # No file extension or weirdly long filename will not be allowed
        # (this is not strictly necessary as the regex should only match OK URLs)
        if not os.path.splitext(file_name)[-1] or len(file_name) > 60:
            self.valid_url = False

        # Initialize base class
        Entity.__init__(self,
                        id_number=-1,
                        name=file_name,
                        sync_path=file_path,
                        parent=parent,
                        folder=False,
                        identifier="linked_file")

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (ANSI.format("Linked File",
                                                                                    formatting="linkedfile"),
                                                                        self.name)

    def url_is_valid(self):
        return self.valid_url

    def print_status(self, status, color, overwrite_previous_line=False):
        """ Print status to console """

        if overwrite_previous_line:
            # Move up one line
            sys.stdout.write(ANSI.format("", formatting="lineup"))
            sys.stdout.flush()

        print ANSI.format(u"[%s]" % status, formatting=color) + unicode(self)[len(status) + 2:]
        sys.stdout.flush()

    def download(self):
        """
        Download the file, returns True or False depecting if the file was downloaded or not. Returns -1 if the file
        was attempted downloaded but failed.
        """
        if os.path.exists(self.sync_path):
            return False

        self.print_status("DOWNLOADING", color="blue")

        # Attempt to download the file
        try:
            data = requests.get(self.download_url)
        except Exception:
            # Could not download, catch any exception
            self.print_status("FAILED", "red", overwrite_previous_line=True)
            return -1

        # Check for OK 200 HTTP response
        if not data.status_code == 200:
            self.print_status("FAILED", "red", overwrite_previous_line=True)
            return -1

        # If here, download was successful, write to disk and print status
        with open(self.sync_path, "wb") as out_file:
            out_file.write(data.content)

    def walk(self, counter):
        """ Stop walking, endpoint """

        counter[0] += 1
        print unicode(self)
        return

    def sync(self):
        """
        Attempt to download a file a the url 'download_url' to the path 'path'/filename while printing
        the status using an indent of print_indent to align with the parent object
        """
        was_downloaded = self.download()

        if was_downloaded != - 1:
            self.print_status("SYNCED", color="green", overwrite_previous_line=was_downloaded)

    def show(self):
        """ Show the folder hierarchy by printing every level """
        print unicode(self)
