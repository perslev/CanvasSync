#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
item.py, Lowest level class in hierarchy

The Item class is the fourth or N+1th level Entity object in the folder hierarchy. It inherits from the base Entity
class and extends its functionality to allow downloading information on the represented item listed in the Canvas
system as well as downloading the payload of the item.

The hierarchy of Entity objects is displayed below:

       Level 1        Synchronizer   <--- Inherits from Entity base class
                           |
                           |
       Level 2           Course      <--- Inherits from Entity base class
                           |
                           |
       Level 3           Module      <--- Inherits from Entity base class
                           |
                           |
       Level 4 to N     (Folder)     <--- Inherits from Entity base class
                           |
                          ...
                        (Folder)
                          ...
                           |
[THIS] Level 4 or N+1     Item       <--- Inherits from Entity base class
"""

# Inbuilt modules
import os
import sys
import io

from CanvasSync.Hierarchy.entity import Entity
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Statics import static_functions
from CanvasSync.Statics.url_shortcut_maker import make_url_shortcut


class Item(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, id, name, path, position, type, parent, url):
        """
        Constructor method, initializes base Entity class and synchronizes the Item (downloads if not downloaded)

        id       : int    | The ID number of the item
        name     : string | The name representation of the item
        path     : string | The path pointing to the item location in the local folder hierarchy
        position : int    | An integer representing the position of the item in the parent folder, such that
                            the item listed first in Canvas gets the item_position '1'.
        type     : string | A string representing the type of file
        parent   : object | The parent object, a Module or Folder object
        url      : string | The API URL pointing to the resource specifying information on the item in Canvas
        """

        # Initialize base class
        Entity.__init__(self, id_number=id, name=name, sync_path=path, parent=parent, folder=False, verbose=False)

        self.position = position   # Currently not used!
        self.type = type
        self.url = url
        self.file_info = None

        if self.type == "ExternalUrl":
            # The file type is an external URL. Create a URL shortcut for the appropriate platform.
            was_downloaded = self.sync_url()
        elif self.type == "Page":
            was_downloaded = self.sync_page()
        else:
            was_downloaded = self.sync_file()

        self.print_status("SYNCED", color="green", overwrite_previous_line=was_downloaded)

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (ANSI.get(self.type) + "%s" % self.type +
                                                                        ANSI.get("end"), self.name)

    def _get_file_information(self):
        """ Returns a dictionary of information on the item from the Canvas server """
        self.file_info = self.api.download_file_information(self.url)

    def sync_url(self):
        make_url_shortcut(url=self.url, path=self.sync_path)

        # Always return False as the DOWNLOADING prompt is not shown, and we don't need to overwrite last line
        # when printing synced status
        return False

    def sync_page(self):
        if os.path.exists(self.sync_path + ".html"):
            return False

        # Print download status
        self.print_status("DOWNLOADING", color="blue")

        # Download dictionary of information on the file
        self._get_file_information()

        # Create a HTML page locally and add a link leading to the live version
        body = self.file_info["body"]
        html_url = self.file_info["html_url"]

        if not os.path.exists(self.sync_path):
            with io.open(self.sync_path + ".html", "w", encoding="utf-8") as out_file:
                out_file.write(u"<h1><strong>%s</strong></h1>" % self.name)
                out_file.write(u"<big><a href=\"%s\">Click here to open this page in Canvas</a></big>" % html_url)
                out_file.write(u"<hr>")
                out_file.write(body)

        return True

    def sync_file(self):
        """
        Synchronize the file by downloading it from the Canvas server and saving it to the sync path
        If the file has already been downloaded, skip downloading.
        """

        # We must download file information before we can check, if it has already been downloaded, as we need to get
        # the file name. This is quick however, as the payload of the file is not downloaded here.
        self._get_file_information()

        # Extract file information from the item dictionary
        file_name = static_functions.get_corrected_name(self.file_info["filename"])
        download_url = self.file_info["url"]
        download_path = self.sync_path[:-len(self.name)] + file_name

        # Might be useful in the feuture
        # file_type = self.file_info["mime_class"]
        # size = self.file_info["size"]

        if os.path.exists(download_path):
            return False

        self.print_status("DOWNLOADING", color="blue")

        # Download file payload from server
        file_data = self.api.download_file_payload(download_url)

        # Write data to file
        try:
            with open(download_path, "wb") as out_file:
                out_file.write(file_data)

        except KeyboardInterrupt as e:
            # If interrupted mid-writing, delete the corrupted file
            if os.path.exists(download_path):
                os.remove(download_path)

            # Re-raise, will be catched in __main__.py
            raise e

        return True

    def print_status(self, status, color, overwrite_previous_line=False):
        """ Print status to console """

        if overwrite_previous_line:
            # Move up one line
            print ANSI.get("lineup")
            sys.stdout.flush()

        print ANSI.get(color) + u"[%s]" % status + ANSI.get("end") + unicode(self)[len(status) + 2:]
