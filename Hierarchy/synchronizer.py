#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
synchronizer.py, First level class in hierarchy

The Synchronizer class is the highest level Entity object in the folder hierarchy. It inherits from the base Entity
class and extends its functionality to allow downloading information on courses listed in the Canvas system. A Course
object is initialized for each course found and appended to a list of children under the Synchronizer object.

The hierarchy of Entity objects is displayed below:

[THIS] Level 1        Synchronizer   <--- Inherits from Entity base class
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
       Level 4 or N+1     Item       <--- Inherits from Entity base class

The Synchronizer encapsulates a list of children Course objects.
"""

# CanvasSync modules
from CanvasSync.Hierarchy.course import Course
from CanvasSync.Hierarchy.entity import Entity

from CanvasSync.Statics import static_functions


class Synchronizer(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, settings, api):
        """
        Constructor method, initializes base Entity class and adds all children Course objects to the list of children

        settings : object | A Settings object, has top-level sync path attribute
        api      : object | A InstructureApi object
        """

        # Start sync by clearing the console window
        static_functions.clear_console()

        # Get the corrected top-level sync path
        sync_path = static_functions.get_corrected_path(settings.sync_path_, False, folder=True)

        # Initialize base class
        Entity.__init__(self, id_number=-1, name="", sync_path=sync_path, api=api)

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u"\n[*] Synchronizing to folder: %s\n" % self.sync_path

    def _add_course(self, course_id, course_name):
        """
        [HIDDEN] Method that adds a Course object to the list of Course objects

        course_id   : int    | The ID number of the course to initialize a Course object on
        course_name : string | The name representation of the course
        """

        # Get the sync path to the course
        course_path = self.sync_path + "%s" % course_name

        # Initialize the Course object and then add it to the list of courses
        self._add(Course(course_id, course_name, course_path, parent=self))

    def _download_courses(self):
        """ [HIDDEN] Returns a dictionary of courses from the Canvas server """
        return self.api.get_courses()

    def _add_courses(self):
        """ [HIDDEN]  Method that adds all Course objects to the list of Course objects """

        # Download dictionary of courses and add them all to the list of children
        for course in self._download_courses():
            course_id = course["id"]
            course_name = course["course_code"].split(";")[-1]

            self._add_course(course_id, course_name)

    def get_courses(self):
        """ Getter-method for the list of children, calls _get_children method of base class """
        return self._get_children()

    def sync(self):
        self._add_courses()

    def show(self):
        """ Traverses the folder hierarchy and prints every level """
        print u"\n%s" % self
        for course in self:
            print course
            for module in course:
                print module
                for item in module:
                    print item
