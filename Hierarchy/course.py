#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
course.py, Second level class in hierarchy

The Course class is the second level Entity object in the folder hierarchy. It inherits from the base Entity
class and extends its functionality to allow downloading information on Modules listed under the course in the Canvas
system. A Module object is initialized for each module found and appended to a list of children under the
Course object.

The hierarchy of Entity objects is displayed below:

       Level 1        Synchronizer   <--- Inherits from Entity base class
                           |
                           |
[THIS] Level 2           Course      <--- Inherits from Entity base class
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
       Level 4 or N+1     Item       <--- Inherits from Entity base class

The Course object encapsulates a list of children Module objects and has the Synchronizer object as parent.
"""

# CanvasSync modules
from CanvasSync.Hierarchy.entity import Entity
from CanvasSync.Hierarchy.module import Module

from CanvasSync.Statics.ANSI import Colors
from CanvasSync.Statics import static_functions


class Course(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, course_id, course_name, course_path, parent):
        """
        Constructor method, initializes base Entity class and adds all children Module objects to the list of children

        course_id   : int    | The ID number of the course
        course_name : string | The name representation of the course
        course_path : string | The path pointing to the course location in the local folder hierarchy
        parent      : object | The parent object, the Synchronizer object
        """

        # Initialize base class
        Entity.__init__(self, id_number=course_id, name=course_name, sync_path=course_path, parent=parent)

        # Add all modules as Module objects to the list of children
        self._add_modules()

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (Colors.COURSE + "Course" + Colors.ENDC,
                                                                        self.name)

    def _add_module(self, module_id, module_name, module_position):
        """
        [HIDDEN] Method that adds a Module object to the list of Module objects

        module_id       : int    | The ID number of the module to initialize a Module object on
        module_name     : string | The name representation of the module
        module_position : int    | An integer representing the position of the Module in the parent folder, such that
                                   the module listed first in Canvas gets the module_position '1'.
        """

        # Get path to module in local folder
        module_path = self.sync_path + u"%s - %s" % (module_position, module_name)

        # Initialize Module object and add to list of children
        self._add(Module(module_id, module_name, module_path, parent=self))

    def _download_modules(self):
        """ Returns a dictionary of modules from the Canvas server """
        return self.api.get_modules(self.id)

    def _add_modules(self):
        """ [HIDDEN]  Method that adds all Module objects to the list of Module objects """

        # Download dictionary of modules and add them all to the list of children
        for position, module in enumerate(self._download_modules()):
            module_id = module["id"]
            module_name = static_functions.get_corrected_name(module["name"])

            self._add_module(module_id, module_name, position + 1)

    def get_modules(self):
        """ Getter-method for the list of children, calls _get_children method of base class """
        return self._get_children()
