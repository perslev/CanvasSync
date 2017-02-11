#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017

--------------------------------------------

sub_header.py, Third level class in hierarchy

The SubHeader class is the fourth-to Nth level Entity object in the folder hierarchy. It inherits from the base Module
class and extends its slightly by adding the ability to instantiate with a dictionary of file information that does not
need downloading from the Canvas server. All other functionality is identical to the Module object. The SubHeader object
may instantiate itself for recursive traversing of the folder hierarchy.
An Item object or SubHeader object is initialized for each item found and appended to a list of children under the
SubHeader object.

Note: There could be another SubHeader encapsulated by this SubHeader object, which is handled by recursion.
"""

# Future imports
from __future__ import print_function

# Third party
from six import text_type

# CanvasSync modules
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.CanvasEntities.module import Module


class SubHeader(Module):
    """ Derived class of the Entity base class """

    def __init__(self, folder_info, folder_position, parent, items):
        """
        Constructor method, initializes base Module class and adds all children Folder and/or Item objects to
        the list of children

        folder_info     : dict   | A dictionary of information on the Canvas subHeader object
        folder_position : int    | An integer representing the position in the folder (1 for first folder)
        parent          : object | The parent object, a Module or Folder object
        items           : list   | A list of dictionaries on Canvas item objects stored in the folder
        """

        self.folder_info = folder_info

        # Add 'title' value to new key 'name' as this is the key used in the Module object
        self.folder_info[u"name"] = self.folder_info[u"title"]

        # Initialize base Module class
        Module.__init__(self,
                        module_info=folder_info,
                        module_position=folder_position,
                        parent=parent,
                        identifier=u"sub_header")

        self.items = items

    def __repr__(self):
        """ String representation, overwriting base class method """
        status = ANSI.format(u"[SYNCED]", formatting=u"green")
        return status + u" " * 7 + u"|   " + u"\t" * self.indent + u"%s: %s" \
                                                                   % (ANSI.format(u"Sub header", formatting=u"subheader"),
                                                                      self.name)

    def walk(self, counter):
        """
        Walk by adding all File, Page, ExternalLink and SubFolder objects to the list of children
        SubFolder is instantiated with a list of dictionaries of item information and will supply this to the add_items
        method. add_items will then not download the items from the server.
        """
        print(text_type(self))

        self.add_items(items=self.items)

        counter[0] += 1
        for item in self:
            item.walk(counter)

    def sync(self):
        """
        1) Adding all File, Page, ExternalLink and SubFolder objects to the list of children
        2) Synchronize all children objects

        SubFolder is instantiated with a list of dictionaries of item information and will supply this to the add_items
        method. add_items will then not download the items from the server.
        """
        print(text_type(self))

        self.add_items(items=self.items)

        for child in self:
            child.sync()
