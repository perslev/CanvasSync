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

# CanvasSync modules
from CanvasSync.Hierarchy.entity import Entity
from CanvasSync.Statics import static_functions
from CanvasSync.Statics.ANSI import Colors


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
        self.type = type           # Currently not used!
        self.url = url

        # Download dictionary of information on the file
        self.file_info = self.get_file()

        # Synchronize file (download if not already downloaded)
        self.sync()

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (Colors.ITEM + "Item" + Colors.ENDC,
                                                                        self.name)

    def get_file(self):
        """ Returns a dictionary of information on the item from the Canvas server """
        return self.api.get_file(self.url)

    def sync(self):
        """
        Synchronize the file by downloading it from the Canvas server and saving it to the sync path
        If the file has already been downloaded, skip downloading.
        """

        # Extract file information from the item dictionary
        file_name = static_functions.get_corrected_name(self.file_info["filename"])
        dowload_url = self.file_info["url"]
        download_path = self.sync_path[:-len(self.name)] + file_name

        # Might be useful in the feuture
        # file_type = self.file_info["mime_class"]
        # size = self.file_info["size"]

        if not os.path.exists(download_path):
            # If not already downloaded.
            # Print 'DOWNLOADING' status line
            print Colors.BLUE + u"[DOWNLOADING]" + Colors.ENDC + unicode(self)[len("[DOWNLOADING]"):]

            # Download file payload from server
            file_data = self.api.download_file(dowload_url)

            # Write data to file
            try:
                with open(download_path, "wb") as out_file:
                    out_file.write(file_data)

                # Move up one line
                sys.stdout.write('\033[F')
                sys.stdout.flush()
            except KeyboardInterrupt as e:
                # If interrupted mid-writing, delete the corrupted file
                if os.path.exists(download_path):
                    os.remove(download_path)

                # Re-raise, will be catched in __main__.py
                raise e

        # If here, file was donwloaded, show 'SYNCED' status line
        print u"\r" + Colors.GREEN + u"[SYNCED]" + Colors.ENDC + unicode(self)[len("[SYNCED]"):]
        sys.stdout.flush()
