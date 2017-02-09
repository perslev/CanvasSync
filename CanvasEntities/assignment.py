#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

# Inbuilt modules
import re

# CanvasSync module imports
from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.CanvasEntities.file import File
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Statics import static_functions


class Assignment(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, assignment_info, parent):
        """
        Constructor method, initializes base Entity class

        assignment_info : dict   | A dictionary of information on the Canvas assignment object
        assignment_path : string | The path pointing to the assignment location in the local folder hierarchy
        parent          : object | The parent object, a course object
        """

        self.assignment_info = assignment_info

        assignment_id = self.assignment_info["id"]
        assignment_name = static_functions.get_corrected_name(assignment_info["name"])
        assignment_path = parent.get_path() + assignment_name

        # Initialize base class
        Entity.__init__(self,
                        id_number=assignment_id,
                        name=assignment_name,
                        sync_path=assignment_path,
                        parent=parent)

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (ANSI.format("Assignment",
                                                                                    formatting="assignment"),
                                                                        self.name)

    def add_files(self):
        """ Add all files that can be found in the description of the assignment to the list of children and sync """
        # Get URL pointing to file objects described somewhere in the description section
        file_info_urls = re.findall(r'data-api-endpoint=\"(.*?)\"', self.assignment_info["description"])

        # Download information on all found files and add File objects to the children
        for url in file_info_urls:
            try:
                file_info = self.api.download_item_information(url)
            except Exception:
                continue

            item = File(file_info, parent=self)
            self.add_child(item)

    def walk(self, counter):
        """ Walk by adding all File objects to the list of children """
        self.add_files()

        counter[0] += 1
        print unicode(self)
        for file in self:
            file.walk(counter)

    def sync(self):
        """
        1) Adding all File objects to the list of children
        2) Synchronize all children objects
        """
        print unicode(self)

        self.add_files()

        for file in self:
            file.sync()

    def show(self):
        """ Show the folder hierarchy by printing every level """
        print unicode(self)

        for file in self:
            file.show()
