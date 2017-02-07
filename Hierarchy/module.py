#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
module.py, Third level class in hierarchy

The Module class is the third level Entity object in the folder hierarchy. It inherits from the base Entity
class and extends its functionality to allow downloading information on Items listed under the module in the Canvas
system. An Item object or Folder object is initialized for each item found and appended to a list of children under the
Module object.

The hierarchy of Entity objects is displayed below:

       Level 1        Synchronizer   <--- Inherits from Entity base class
                           |
                           |
       Level 2           Course      <--- Inherits from Entity base class
                           |
                           |
[THIS] Level 3           Module      <--- Inherits from Entity base class
                           |
                           |
       Level 4 to N     (Folder)     <--- Inherits from Entity base class
                           |
                          ...
                        (Folder)
                          ...
                           |
       Level 4 or N+1     Item       <--- Inherits from Entity base class

The Module object encapsulates a list of children Folder objects or Item objects and has a Course object as parent.
"""

# CanvasSync modules
from CanvasSync.Hierarchy.entity import Entity
from CanvasSync.Hierarchy.item import Item
from CanvasSync.Hierarchy.subfolder import Folder
from CanvasSync.Statics import static_functions
from CanvasSync.Statics.ANSI import Colors


class Module(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, module_id, module_name, module_path, parent):
        """
        Constructor method, initializes base Entity class and adds all children Folder and/or Item objects to the
        list of children

        module_id   : int    | The ID number of the module
        module_name : string | The name representation of the module
        module_path : string | The path pointing to the module location in the local folder hierarchy
        parent      : object | The parent object, a Course object
        """

        # Initialize base class
        Entity.__init__(self, id_number=module_id, name=module_name, sync_path=module_path, parent=parent)

        # Add all items as Folder or Item objects to the list of children
        self._add_items()

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (Colors.RED + "Module" + Colors.ENDC,
                                                                        self.name)

    def _add_item(self, item_id, item_name, item_position, item_type, url):
        """
        [HIDDEN] Method that adds a Item object to the list of children

        item_id       : int    | The ID number of the item to initialize an Item object on
        item_name     : string | The name representation of the item
        item_position : int    | An integer representing the position of the item in the parent folder, such that
                                 the item listed first in Canvas gets the item_position '1'.
        item_type     : string | The type of item, could be a 'header' or 'file'
        url           : string | The API URL pointing to the resource specifying information on the item in Canvas
        """

        # Get path to Item in local folder
        item_path = self.sync_path + "%s" % item_name

        # Initialize Item object and add to list of children
        self._add(Item(item_id, item_name, item_path, item_position, item_type, self, url))

    def _add_sub_folder(self, folder_id, folder_name, folder_position, folder_items):
        """
        [HIDDEN] Method that adds a Folder object to the list of children

        folder_id       : int    | The ID number of the folder to initialize an Folder object on
        folder_name     : string | The name representation of the folder
        folder_position : int    | An integer representing the position of the folder in the parent folder, such that
                                   the folder listed first in Canvas gets the folder_position '1'.
        folder_items    : dict   | A dictionary of information on items contained by the sub-folder
        """

        # Get path to folder in local folder
        sub_folder_path = self.sync_path + u"%s - %s" % (folder_position, folder_name)

        # Initialize Folder object and add to list of children
        self._add(Folder(folder_id, folder_name, sub_folder_path, parent=self, items=folder_items))

    def _download_items(self):
        """ Returns a dictionary of items from the Canvas server """
        return self.api.get_items(self.get_parent().get_id(), self.id)

    def _add_items(self):
        """
        [HIDDEN]  Method that adds all Items under the module to the list of children.
                  If the item is a sub-folder it will be added as a Folder object instead.
        """

        # Download dictionary of items
        items = self._download_items()

        # Determine which items are in the outer-scope (located in the folder represented by this module) and which
        # items are located in sub-folders under this module.
        items_in_this_scope, sub_folders = static_functions.reorganize(items)

        # Add all non-sub-folder items to the list of children. Currently, only file items are added.
        for item in items_in_this_scope:
            item_id = item["id"]
            item_name = static_functions.get_corrected_name(item["title"])
            item_position = item["position"]
            item_type = item["type"]

            # If the item is a file, add it
            if item_type == "File":
                url = item["url"]
                self._add_item(item_id, item_name, item_position, item_type, url)

        # Add all sub-folders as Folder objects to the list of children
        for position, folder in enumerate(sub_folders):
            folder_id = folder[0]["id"]
            folder_name = static_functions.get_corrected_name(folder[0]["title"])
            folder_items = folder[1:]

            self._add_sub_folder(folder_id, folder_name, position + 1, folder_items)

    def get_folders(self):
        """ Getter-method for the list of children, calls _get_children method of base class """
        return self._get_children()
