#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
folder.py, Third level class in hierarchy

The SubHeader class is the fourth-to Nth level Entity object in the folder hierarchy. It inherits from the base Module
class and extends its slightly by adding the ability to instantiate with a dictionary of file information that does not
need downloading from the Canvas server. All other functionality is identical to the Module object. The SubHeader object
may instantiate itself for recursive traversing of the folder hierarchy.
An Item object or Folder object is initialized for each item found and appended to a list of children under the
Folder object.

Note: There could be another sub-folder encapsulated by this Folder object, which is handled by recursion.
"""

# CanvasSync modules
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.CanvasEntities.file import File
from CanvasSync.Statics import static_functions


class Folder(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, folder_info, parent, black_list=False):
        """
        Constructor method, initializes base Module class and adds all children Folder and/or Item objects to
        the list of children

        folder_info     : dict   | A dictionary of information on the Canvas subHeader object
        folder_position : int    | An integer representing the position in the folder (1 for first folder)
        parent          : object | The parent object, a Module or Folder object
        items           : list   | A list of dictionaries on Canvas item objects stored in the folder
        """

        self.folder_info = folder_info

        folder_id = self.folder_info["id"]
        folder_name = static_functions.get_corrected_name(self.folder_info["name"])
        folder_path = parent.get_path() + folder_name

        # Initialize base Module class
        Entity.__init__(self,
                        id_number=folder_id,
                        name=folder_name,
                        sync_path=folder_path,
                        parent=parent,
                        identifier="folder")

        self.black_list = black_list

    def __repr__(self):
        """ String representation, overwriting base class method """
        status = ANSI.format("[SYNCED]", formatting="green")
        return status + u" " * 7 + u"|   " + u"\t" * self.indent + u"%s: %s" \
                                                                   % (ANSI.format("Folder", formatting="folder"),
                                                                      self.name)

    def initialize_black_list(self):
        """
        Some files may have been added to Module or Assignment objects already, so we do not need to store them again
        This method initializes a list of all file names that exist in the hierarchy of the Course object so far
        """

        # Get all entities listed in the Synchronizer object under the course.
        entities = self.get_synchronizer().get_entities(self.get_course().get_id())

        # Get list of names of all the File objects of the entities list
        black_list = [x.get_id() for x in entities if x.get_identifier_string() == "file"]

        return black_list

    def add_files(self):
        """ Add all files stored by this folder to the list of children """
        files = self.api.get_files_in_folder(self.id)

        for file in files:
            # Skip duplicates if this settings is active (otherwise the list will be empty)
            if file["id"] in self.black_list:
                continue

            file = File(file, self, add_to_list_of_entities=False)
            self.add_child(file)

    def add_sub_folders(self):
        """ Add all sub-folders stored by this folder to the list of children """
        folders = self.api.get_folders_in_folder(self.id)

        for folder in folders:
            if folder["name"] == "course_image":
                # Do we really need that course image?
                continue

            folder = Folder(folder, self, black_list=self.black_list)
            self.add_child(folder)

    def walk(self, counter):
        """
        Walk by adding all Files and Folder objects to the list of children
        """
        print unicode(self)

        # If avoid duplicated setting is active, initialize black list of files found in Modules and
        # Assignments if it was not passed to the object at initialization.
        if not self.black_list and self.settings.avoid_duplicates:
            self.black_list = self.initialize_black_list()
        elif not self.settings.avoid_duplicates:
            self.black_list = []

        self.add_files()
        self.add_sub_folders()

        counter[0] += 1
        for item in self:
            item.walk(counter)

    def sync(self):
        """
        1) Adding all Files and Folder objects to the list of children
        2) Synchronize all children objects
        """
        print unicode(self)

        # If avoid duplicated setting is active, initialize black list of files found in Modules and
        # Assignments if it was not passed to the object at initialization.
        if not self.black_list and self.settings.avoid_duplicates:
            self.black_list = self.initialize_black_list()
        elif not self.settings.avoid_duplicates:
            self.black_list = []

        self.add_files()
        self.add_sub_folders()

        for item in self:
            item.sync()
