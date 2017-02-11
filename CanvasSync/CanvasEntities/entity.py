#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
Entity.py, Base class

The base class of the CanvasSync folder hierarchy.
This object implements basic functionality shared across all entities in the folder structure of the Canvas server.
Higher level objects representing entities such as Courses, Modules, Folders and Items inherit from the object.

Note that in the CanvasSync notation 'parent' refers to the Entity object located one logical level above,
and a 'child' refers to an Entity object located one logical level below. For instance, a Module object is the parent
of a sub-folder entity. The sub-folder entity might in turn encapsulate 4 children Item objects.

In regards to inheritance, the Entity class is the base class of a Module object for instance,
while the Module is the derived class.
"""

# Inbuilt modules
import os

# Third party
from six import text_type

# CanvasSync module imports
from CanvasSync.Statics import static_functions


class Entity(object):
    def __init__(self, id_number, name, sync_path, parent=None, folder=True, api=None, settings=None, identifier="",
                 synchronizer=None, add_to_list_of_entities=True):
        """
        Constructor method

        id_number : string  | The ID number of the entity, e.g. this could be a Module ID number
        name      : string  | The name of the entity, e.g. this could be the name of a Course
        sync_path : string  | A string representing the path to where the entity is synced to in the local folder
        parent    : object  | An object representing the 'parent' to this Entity, that is the Entity one level above
                              Note that this does not mean parent in regards to inheritance.
        folder    : boolean | A boolean indicating whether this entity is a folder or file
        api       : object  | An InstructureApi object
        verbose   : boolean | A boolean indicating whether the string representation of this object should be printed
                              to the screen after initialization. This value is False for Item objects that implement
                              their own special printing functionality to account for download status etc.
        """

        # Identifier information
        self.id = id_number

        # Parent object
        self.parent = parent

        # Identifier, could be "course"
        self.identifier = identifier

        # Entity name
        self.name = name

        # Is this a folder or file?
        self.folder = folder

        # The same InstructureApi object is used across all Entities and so only the top-level Syncronizer object
        # is initialized with the object. All other lower level Entities fetches the object from their parent.
        if api:
            self.api = api
        else:
            self.api = self.get_parent().get_api()

        # Set settings object
        if settings:
            self.settings = settings
        else:
            self.settings = self.get_parent().get_settings()

        # Sync path
        if self.parent:
            parent_path = parent.get_path()
        else:
            parent_path = False

        # Get the path of the Entity in the local folder
        self.sync_path = static_functions.get_corrected_path(sync_path, parent_path, folder=folder)

        # Child objects, that is Entities that are located below this current level in the folder hierarchy
        # E.g. this list could contain Item objects located under a Module object.
        self.children = []

        # Indent level
        if self.parent:
            self.indent = self.get_parent().indent + 1
        else:
            self.indent = -1

        # If this Entity is a folder, create it
        if self.folder:
            self._make_folder()

        # Set synchronizer object
        if synchronizer:
            self.synchronizer = synchronizer
        else:
            self.synchronizer = self.get_parent().get_synchronizer()

            if add_to_list_of_entities:
                # Add Entity to the list in the Synchronizer object
                self.get_synchronizer().add_entity(self, self.get_course().get_id())

    def __getitem__(self, item):
        """ Container get-item method can be used to access a specific child object """
        return self.children[item]

    def __iter__(self):
        """ Iterator method yields all Entities contained by this Entity """
        for child in self.children:
            yield child

    def __repr__(self):
        """ String representation, overwritten in derived class """
        return u"Base object: %s" % self.name

    def __len__(self):
        """ len() method """
        return len(self.children)

    def __nonzero__(self):
        """ Boolean representation method. Always returns True after initialization. """
        return True

    def __bool__(self):
        """ Boolean representation method. Always returns True after initialization. """
        return self.__nonzero__()

    def get_identifier_string(self):
        """ Getter method for the identifier string """
        return self.identifier

    def get_course(self):
        """ Go up one level until the Course object is reached, then return it """

        if self.get_identifier_string() == u"course":
            return self

        parent = self.parent

        while parent.get_identifier_string().lower() != u"course":
            parent = parent.get_parent()

        return parent

    def get_name(self):
        """ Getter method for the name """
        return self.name

    def get_synchronizer(self):
        """ Getter method for the Synchronizer object """
        return self.synchronizer

    def get_id(self):
        """ Getter method for the ID number """
        return self.id

    def get_parent(self):
        """ Getter method for the parent object """
        return self.parent

    def get_api(self):
        """ Getter method for the InstructureApi object """
        return self.api

    def get_settings(self):
        """ Getter method for the Settings object """
        return self.settings

    def get_path(self):
        """ Getter method for the sync path """
        return self.sync_path

    def add_child(self, child):
        """ Add a child object to the list of children """
        self.children.append(child)

    def get_children(self):
        """ Getter method for the list of children """
        return self.children

    def _make_folder(self):
        """ Create a folder on the sync path if not already present """
        if not os.path.exists(self.sync_path):
            os.mkdir(self.sync_path)
