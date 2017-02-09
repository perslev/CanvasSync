#!/usr/bin/env python2.7

"""
CanvasSync by Mathias Perslev

MSc Bioinformatics, University of Copenhagen
February 2017
"""

"""
static_function.py, module

A collection of small static helper-functions used in various modues of CanvasSync.
"""

# Inbuilt modules
import os


def reorganize(items):
    """
    Takes a dictionary of items and parses them for sub-folders.

    A list of items located in the outer scope is returned along with a list of containing dictionaries of items
    contained within each potential sub-folder.

    items : list | A list of JSON dictionary objects containing information on Canvas item objects
    """

    # If no items, return empty lists
    if len(items) == 0:
        return [], []

    # Create a list that will store all files located in the outer most scope of the hierarchy
    outer_scope_files = []

    # Create a list that will hold sub dictionaries containing information on all files in the sub-folder
    sub_folders = []

    # Counter value used to keep track of how many the index of the current sub-folder that is being reorganized.
    current_sub_folder_index = -1

    # Get the indent level of the outer most scope, should be that of the 0th item in the list, but we check all here.
    outer_indent = min([items[index]["indent"] for index in range(len(items))])

    # Reorganize all items in 'items'
    for item in items:
        # Get the type of item and indent level
        item_type = item["type"]
        item_indent = item["indent"]

        if item_type == "SubHeader":
            # If "SubHeader" the item is a sub-folder, add it to the list of sub-folders
            current_sub_folder_index += 1
            sub_folders.append([item])
        elif item_indent == outer_indent or current_sub_folder_index == -1:
            # If not a folder, is the item in the outer most scope?
            outer_scope_files.append(item)
        else:
            # File is located in a sub-folder
            sub_folders[current_sub_folder_index].append(item)

    return outer_scope_files, sub_folders


def clear_console():
    """ Clears the console on UNIX and Windows """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_corrected_path(path, parent_path, folder):
    """
    Returns a corrected path string containing no forward slashed in the file name (will be misinterpreted as a
    folder). Also adds a trailing forward slash if not present.

    path        : string  | A string representing a path
    parent_path : string  | A string representing the path of the parent of the object calling this method
                             It is used to determine what part of the 'path' variable is the actual path and what is
                             the name of the sub-folder/file that could potentially contain forward slahsed that must
                             be replaced by dots.
    folder      : boolean | Does the input path point to a folder? (False = file)
                             If the path points to a folder, a trailing forward slash is appended to the path string.
    """
    if parent_path:
        name = path.split(parent_path)[-1]
        path = parent_path + name.replace("/", ".")

    path = os.path.abspath(path)
    path += "/" if folder else ""

    return path


def get_corrected_name(name):
    """
    Validates the name of an Entry
    This method may be extended in the feature to include more validations.

    name : string | A string representing the name of an Entry (Module, File etc.)
    """
    if len(name) > 60:
        # The name is too long, this may happen for sub-folders where the title is accidentally used to describe the
        # content of the folder. Reduce the length of the name and append trailing dots '...'
        name = name[:60] + "..."
    return name
