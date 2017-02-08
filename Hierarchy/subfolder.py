#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
subfolder.py, Third level class in hierarchy

The Folder class is the fourth-to Nth level Entity object in the folder hierarchy. It inherits from the base Entity
class and extends its functionality to allow downloading information on Items listed under the sub-folder in the Canvas
system. An Item object or Folder object is initialized for each item found and appended to a list of children under the
Folder object.

Note: There could be another sub-folder encapsulated by this Folder object, which is handled by recursion.

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
[THIS] Level 4 to N     (Folder)     <--- Inherits from Entity base class
                           |
                          ...
                        (Folder)
                          ...
                           |
       Level 4 or N+1     Item       <--- Inherits from Entity base class

The Folder object encapsulates a list of children Folder objects or Item objects and has a Module or Folder object
as parent.
"""

# CanvasSync modules
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Hierarchy.module import Module


class SubFolder(Module):
    """ Derived class of the Entity base class """

    def __init__(self, folder_id, folder_name, folder_path, parent, items):
        """
        Constructor method, initializes base Module class and adds all children Folder and/or Item objects to
        the list of children

        folder_id   : int    | The ID number of the folder
        folder_name : string | The name representation of the folder
        folder_path : string | The path pointing to the folder location in the local folder hierarchy
        parent      : object | The parent object, a Module or Folder object
        """

        # Initialize base class
        Module.__init__(self, module_id=folder_id, module_name=folder_name, module_path=folder_path, parent=parent)

        # The Folder object may be initialized with a item dictionary instead of downloading them from the server
        self.items = items

        # Add all items as Folder or Item objects to the list of children
        self._add_items()

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (ANSI.format("Sub folder", formatting="subfolder"),
                                                                        self.name)
