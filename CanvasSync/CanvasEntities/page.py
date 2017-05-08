#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017

--------------------------------------------

page, CanvasEntity Class

The Page class stores information on HTML pages hosted on the Canvas server. It represents an end point in the hierarchy
and contains no child objects. When the sync method is invoked the HTML pages will be downloaded or skipped depending on
if it is already present in at the sync path. The HTML page will be appended with the title of the page along with a
URL pointing to the live version of the HTML page on the server.

A Module or SubHeader object is the parent object.

See developer_info.txt file for more information on the class hierarchy of CanvasEntities objects.

"""

# Future imports
from __future__ import print_function

# Inbuilt modules
import os
import sys
import io
import re

# Third party
from six import text_type

from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Statics import static_functions
from CanvasSync.CanvasEntities.file import File
from CanvasSync.CanvasEntities.linked_file import LinkedFile


class Page(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, page_info, parent):
        """
        Constructor method, initializes base Entity class

        page_info : dict   | A dictionary of information on the Canvas page object
        parent    : object | The parent object, a Module or SubHeader object
        """

        self.page_info = page_info

        page_id = self.page_info[u"id"]
        page_name = static_functions.get_corrected_name(self.page_info[u"title"])
        page_path = parent.get_path() + page_name

        # Initialize base class
        Entity.__init__(self,
                        id_number=page_id,
                        name=page_name,
                        sync_path=page_path,
                        parent=parent,
                        folder=False,
                        identifier=u"page")

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (ANSI.format(u"Page",
                                                                                    formatting=u"page"),
                                                                        self.name)

    def download_linked_files(self, html_body):
        sub_files = False

        # Look for files in the HTML body
        # Get file URLs pointing to Canvas items
        canvas_file_urls = re.findall(r'data-api-endpoint=\"(.*?)\"', html_body)

        # Download information on all found files and add File objects to the children
        for url in canvas_file_urls:
            try:
                file_info = self.api.download_item_information(url)
                if u'display_name' not in file_info:
                    continue
            except Exception:
                continue

            item = File(file_info, parent=self)
            self.add_child(item)
            sub_files = True

        if self.settings.download_linked:
            # We also look for links to files downloaded from other servers
            # Get all URLs ending in a file name (determined as a ending with a '.'
            # and then between 1 and 10 of any characters after that). This has 2 purposes:
            # 1) We do not try to re-download Canvas server files, since they are not matched by this regex
            # 2) We should stay clear of all links to web-sites (they could be large to download, we skip them here)
            urls = re.findall(r'href=\"([^ ]*[.]{1}.{1,10})\"', html_body)

            for url in urls:
                linked_file = LinkedFile(url, self)

                if linked_file.url_is_valid():
                    self.add_child(linked_file)
                    sub_files = True
                else:
                    del linked_file

        return sub_files

    def push_down(self):
        """ Lower the level of this page once into a sub-folder of similar name """
        self._make_folder()
        base, tail = os.path.split(self.sync_path)
        self.sync_path = self.sync_path + u"/" + tail

    def download(self):
        """ Download the page """
        if os.path.exists(self.sync_path + u".html"):
            return False

        # Print download status
        self.print_status(u"DOWNLOADING", color=u"blue")

        # Download additional info and HTML body of the Page object
        self.page_info = self.api.download_item_information(self.page_info[u"url"])

        # Create a HTML page locally and add a link leading to the live version
        body = self.page_info[u"body"]
        html_url = self.page_info[u"html_url"]

        if self.download_linked_files(body):
            self.push_down()

        if not os.path.exists(self.sync_path):
            with io.open(self.sync_path + u".html", u"w", encoding=u"utf-8") as out_file:
                out_file.write(u"<h1><strong>%s</strong></h1>" % self.name)
                out_file.write(u"<big><a href=\"%s\">Click here to open the live page in Canvas</a></big>" % html_url)
                out_file.write(u"<hr>")
                out_file.write(body)

        return True

    def print_status(self, status, color, overwrite_previous_line=False):
        """ Print status to console """
        if overwrite_previous_line:
            # Move up one line
            sys.stdout.write(ANSI.format(u"", formatting=u"lineup"))
            sys.stdout.flush()

        print(ANSI.format(u"[%s]" % status, formatting=color) + str(self)[len(status) + 2:])
        sys.stdout.flush()

    def walk(self, counter):
        """ Stop walking, endpoint """
        print(text_type(self))

        counter[0] += 1
        return

    def sync(self):
        """
        Synchronize the page by downloading it from the Canvas server and saving it to the sync path
        If the page has already been downloaded, skip downloading.
        Page objects have no children objects and represents an end point of a folder traverse.
        """

        was_downloaded = self.download()
        self.print_status(u"SYNCED", color=u"green", overwrite_previous_line=was_downloaded)

        for file in self:
            file.update_path()
            file.sync()

    def show(self):
        """ Show the folder hierarchy by printing every level """
        print(text_type(self))
