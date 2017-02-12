#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017

--------------------------------------------

assignment.py, CanvasEntity Class

The Assignment class stores a list of child File objects and creates HTML pages representing the assignment description.
It is one level below the parent container AssignmentsFolder class and inherits from the Entity base class.

An AssignmentsFolder object is the parent object.

See developer_info.txt file for more information on the class hierarchy of CanvasEntities objects.
"""

# Future imports
from __future__ import print_function

# Inbuilt modules
import re
import os
import io

# Third party
from six import text_type

# CanvasSync module imports
from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.CanvasEntities.file import File
from CanvasSync.CanvasEntities.linked_file import LinkedFile
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Statics import static_functions


class Assignment(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, assignment_info, parent):
        """
        Constructor method, initializes base Entity class

        assignment_info : dict   | A dictionary of information on the Canvas assignment object
        parent          : object | The parent object, an AssignmentsFolder object
        """

        self.assignment_info = assignment_info

        assignment_id = self.assignment_info[u"id"]
        assignment_name = static_functions.get_corrected_name(assignment_info[u"name"])
        assignment_path = parent.get_path() + assignment_name

        # Initialize base class
        Entity.__init__(self,
                        id_number=assignment_id,
                        name=assignment_name,
                        sync_path=assignment_path,
                        parent=parent,
                        identifier=u"assignment")

    def __repr__(self):
        """ String representation, overwriting base class method """
        status = ANSI.format(u"[SYNCED]", formatting=u"green")
        return status + u" " * 7 + u"|   " + u"\t" * self.indent + u"%s: %s" \
                                                                   % (ANSI.format(u"Assignment", formatting=u"assignment"),
                                                                      self.name)

    def make_html(self):
        """ Create the main HTML description page of the assignment """

        # Create URL pointing to Canvas live version of the assignment
        url = self.settings.domain + u"/courses/%s/assignments/%s" % (self.get_parent().get_parent().get_id(),
                                                                      self.get_id())

        if not os.path.exists(self.sync_path + self.name + u".html"):
            with io.open(self.sync_path + self.name + u".html", u"w", encoding=u"utf-8") as out_file:
                out_file.write(u"<h1><strong>%s</strong></h1>" % self.name)
                out_file.write(u"<big><a href=\"%s\">Click here to open the live page in Canvas</a></big>" % url)
                out_file.write(u"<hr>")
                out_file.write(self.assignment_info[u"description"])

    def add_files(self):
        """ Add all files that can be found in the description of the assignment to the list of children and sync """
        # Get URL pointing to file objects described somewhere in the description section

        # Get file URLs pointing to Canvas items
        canvas_file_urls = re.findall(r'data-api-endpoint=\"(.*?)\"', self.assignment_info[u"description"])

        # Download information on all found files and add File objects to the children
        for url in canvas_file_urls:
            try:
                file_info = self.api.download_item_information(url)
            except Exception:
                continue

            item = File(file_info, parent=self)
            self.add_child(item)

        if self.settings.download_linked:
            # We also look for links to files downloaded from other servers
            # Get all URLs ending in a file name (determined as a ending with a '.'
            # and then between 1 and 10 of any characters after that). This has 2 purposes:
            # 1) We do not try to re-download Canvas server files, since they are not matched by this regex
            # 2) We should stay clear of all links to web-sites (they could be large to download, we skip them here)
            urls = re.findall(r'href=\"([^ ]*[.]{1}.{1,10})\"', self.assignment_info[u"description"])

            for url in urls:
                linked_file = LinkedFile(url, self)

                if linked_file.url_is_valid():
                    self.add_child(linked_file)
                else:
                    del linked_file

    def walk(self, counter):
        """ Walk by adding all File objects to the list of children """
        print(text_type(self))

        self.add_files()

        counter[0] += 1
        for file in self:
            file.walk(counter)

    def sync(self):
        """
        1) Adding all File and LinkedFile objects to the list of children
        2) Synchronize all children objects
        """
        print(text_type(self))

        self.add_files()
        self.make_html()

        for file in self:
            file.sync()

    def show(self):
        """ Show the folder hierarchy by printing every level """
        print(text_type(self))

        for file in self:
            file.show()
