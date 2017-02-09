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
"""

# CanvasSync modules
from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.CanvasEntities.module import Module
from CanvasSync.CanvasEntities.assignments_folder import AssignmentsFolder
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Statics import static_functions


class Course(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, course_info, parent):
        """
        Constructor method, initializes base Entity class and adds all children Module objects to the list of children

        course_info   : dict    | A dictionary of information on the Canvas course object
        parent        : object  | The parent object, the Synchronizer object
        """

        self.course_info = course_info

        course_id = self.course_info["id"]
        course_name = static_functions.get_corrected_name(self.course_info["course_code"].split(";")[-1])
        course_path = parent.get_path() + course_name

        # Initialize base class
        Entity.__init__(self,
                        id_number=course_id,
                        name=course_name,
                        sync_path=course_path,
                        parent=parent)

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (ANSI.format("Course", formatting="course"),
                                                                        self.name)

    def download_modules(self):
        """ Returns a list of dictionaries representing module objects """
        return self.api.get_modules(self.id)

    def add_modules(self):
        """ [HIDDEN]  Method that adds all Module objects to the list of Module objects """

        # Download list of dictionaries representing modules and add them all to the list of children
        for position, module_info in enumerate(self.download_modules()):
            module = Module(module_info, position+1, parent=self)
            self.add_child(module)

    def download_assignemtns(self):
        """ Return a list of dictionaries representing assignment objects """
        return self.api.get_assigments(self.id)

    def add_assignments_folder(self):
        """ Add an AssigmentsFolder object to the children list """

        # Download potential assignments
        assignments_info_list = self.download_assignemtns()

        if len(assignments_info_list) == 0:
            return

        assignments = AssignmentsFolder(assignments_info_list, self)
        self.add_child(assignments)

    def walk(self, counter):
        """ Walk by adding all Modules and AssignmentFolder objects to the list of children """
        self.add_modules()

        # Add an AssignmentsFolder if at least one assignment is found under the course
        self.add_assignments_folder()

        counter[0] += 1
        print unicode(self)
        for child in self:
            child.walk(counter)

    def sync(self):
        """
        1) Adding all Modules and AssignmentFolder objects to the list of children
        2) Synchronize all children objects
        """
        print unicode(self)

        self.add_modules()

        # Add an AssignmentsFolder if at least one assignment is found under the course
        self.add_assignments_folder()

        for child in self:
            child.sync()

    def show(self):
        """ Show the folder hierarchy by printing every level """
        print unicode(self)

        for child in self:
            child.show()
