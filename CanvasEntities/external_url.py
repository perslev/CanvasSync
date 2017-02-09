#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

# Inbuilt modules
import sys

from CanvasSync.CanvasEntities.entity import Entity
from CanvasSync.Statics.ANSI import ANSI
from CanvasSync.Statics import static_functions
from CanvasSync.Statics.url_shortcut_maker import make_url_shortcut


class ExternalUrl(Entity):
    """ Derived class of the Entity base class """

    def __init__(self, url_info, parent):
        """
        Constructor method, initializes base Entity class and synchronizes the Item (downloads if not downloaded)

        url_info : dict   | A dictionary of information on the Canvas ExternalUrl object
        parent   : object | The parent object, a Module or SubFolder object
        """
        self.url_info = url_info

        url_id = self.url_info["id"]
        url_name = static_functions.get_corrected_name(self.url_info["title"])
        url_path = parent.get_path() + url_name

        # Initialize base class
        Entity.__init__(self,
                        id_number=url_id,
                        name=url_name,
                        sync_path=url_path,
                        parent=parent,
                        folder=False)

    def __repr__(self):
        """ String representation, overwriting base class method """
        return u" " * 15 + u"|   " + u"\t" * self.indent + u"%s: %s" % (ANSI.format("ExternalUrl",
                                                                                    formatting="externalurl"),
                                                                        self.name)

    def walk(self, counter):
        """ Stop walking, endpoint """

        counter[0] += 1
        print unicode(self)
        return

    def sync(self):
        """
        Synchronize by creating a local URL shortcut file in in at the sync_pat
        ExternalUrl objects have no children objects and represents an end point of a folder traverse.
        """
        make_url_shortcut(url=self.url_info["external_url"], path=self.sync_path)

        # As opposed to the File and Page classes we never write the "DOWNLOAD" status as we already have
        # all information needed to create the URL shortcut at this point. Here we just print the SYNCED status
        # no matter if the shortcut was recreated or not
        print ANSI.format(u"[SYNCED]", formatting="green") + unicode(self)[len("[SYNCED]"):]
        sys.stdout.flush()

    def show(self):
        """ Show the folder hierarchy by printing every level """
        print unicode(self)
