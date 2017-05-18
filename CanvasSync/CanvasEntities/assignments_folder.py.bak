#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017

--------------------------------------------

assignments_folder.py, CanvasEntity Class

The AssignmentsFolder class is a simple container class storing a list of child Assignment objects.
It is one level below the parent Course class and inherits from the Entity base class.

A Course object is the parent object.

See developer_info.txt file for more information on the class hierarchy of CanvasEntities objects.

"""

# Future imports
from __future__ import print_function

# Third party
from six import text_type

# CanvasSync module imports
from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.CanvasEntities.assignment import Assignment
from CanvasSync.Statics.ANSI import ANSI


class AssignmentsFolder(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, assignments_info, parent):
        """
        Constructor method, initializes base Entity class

        assignments_info : dict   | A list of dictionaries of information on all Canvas assignments object under a course
        parent           : object | The parent object, a Course object
        """

        self.assignments_info = assignments_info

        # Initialize entity with hardcoded ID and name, we always want the folder to be named "Assignments"
        assignments_folder_id = -1
        assignments_folder_name = u"Assignments"
        assignments_folder_path = parent.get_path() + assignments_folder_name

        # Initialize base class
        Entity.__init__(self,
                        id_number=assignments_folder_id,
                        name=assignments_folder_name,
                        sync_path=assignments_folder_path,
                        parent=parent,
                        identifier=u"assignment_folder")

    def __repr__(self):
        """ String representation, overwriting base class method """
        status = ANSI.format(u"[SYNCED]", formatting=u"green")
        return status + u" " * 7 + u"|   " + u"\t" * self.indent + u"%s: %s" \
                                                                   % (ANSI.format(u"Assignments Folder",
                                                                                  formatting=u"assignments"),
                                                                      self.name)

    def add_assignments(self):
        """ Add an Assignment object to the list of children """

        for assignment_info in self.assignments_info:
            assignment = Assignment(assignment_info, self)
            self.add_child(assignment)

    def walk(self, counter):
        """ Walk by adding all Assignment objects to the list of children """
        print(text_type(self))

        self.add_assignments()

        counter[0] += 1
        for assignment in self:
            assignment.walk(counter)

    def sync(self):
        """
        1) Adding all Assignment objects to the list of children
        2) Synchronize all children objects
        """
        print(text_type(self))

        self.add_assignments()

        for child in self:
            child.sync()

    def show(self):
        """ Show the folder hierarchy by printing every level """
        print(text_type(self))

        for child in self:
            child.show()
