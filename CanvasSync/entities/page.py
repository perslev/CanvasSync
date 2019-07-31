"""
CanvasSync by Mathias Perslev
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

from CanvasSync.entities.canvas_entity import CanvasEntity
from CanvasSync.utilities.ANSI import ANSI
from CanvasSync.utilities import helpers
from CanvasSync.entities.file import File
from CanvasSync.entities.linked_file import LinkedFile


class Page(CanvasEntity):
    def __init__(self, page_info, parent):
        """
        Constructor method, initializes base CanvasEntity class

        page_info : dict   | A dictionary of information on the Canvas page object
        parent    : object | The parent object, a Module or SubHeader object
        """

        # Sometimes the Page object is initialized with a json dict of information on the file like object representing
        # the HTML page instead of an object on the page itself. This file like object does not store the actual HTML
        # body, which will be downloaded in the self.download() method. The slightly messy code below makes the class
        # functional with either information supplied.
        self.page_item_info = page_info
        self.page_info = self.page_item_info if u"id" not in self.page_item_info else None

        page_id = self.page_item_info[u"id"] if not self.page_info else self.page_info[u"page_id"]
        page_name = helpers.get_corrected_name(self.page_item_info[u"title"])
        page_path = parent.get_path() + page_name

        # Initialize base class
        CanvasEntity.__init__(self,
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
        canvas_file_urls = re.findall(r'data-api-endpoint=\"(.*?)\"', html_body or "")

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
            urls = re.findall(r'href=\"([^ ]*[.]{1}.{1,10})\"', html_body or "")

            for url in urls:
                linked_file = LinkedFile(url, self)

                if linked_file.url_is_valid():
                    self.add_child(linked_file)
                    sub_files = True
                else:
                    del linked_file

        return sub_files

    def push_down(self):
        """
        Lower the level of this page once into a sub-folder of similar name
        """
        self._make_folder()
        base, tail = os.path.split(self.sync_path)
        self.sync_path = self.sync_path + u"/" + tail

    def download(self):
        """ Download the page """
        if os.path.exists(self.sync_path + u".html"):
            return False

        # Print download status
        self.print_status(u"DOWNLOADING", color=u"blue")

        # Download additional info and HTML body of the Page object if not already supplied
        self.page_info = self.api.download_item_information(self.page_item_info[u"url"]) if not self.page_info else self.page_info

        # Create a HTML page locally and add a link leading to the live version
        body = self.page_info.get(u"body", "")
        html_url = self.page_info.get(u"html_url", "")

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
