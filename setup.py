#!/usr/bin/env python2.7

from distutils.core import setup
import re


VERSION_FILE = "./CanvasSync/_version.py"


def get_version():
    """ Load the CanvasSync package version string """

    version_string = open(VERSION_FILE, "r").read()
    regex = r"__version__[ ]?=[ ]?['\"]([^'\"]*)['\"]"

    match = re.search(regex, version_string)

    if match:
        return match.group(1)
    else:
        raise RuntimeError("Unable to load version string in %s" % VERSION_FILE)


setup(name='CanvasSync',
      version=get_version(),
      description='Synchronizes modules, assignments and files from a Canvas server to a local folder',
      long_description=open("README.rst").read(),
      author='Mathias Perslev',
      author_email='mathias@perslev.com',
      url='https://github.com/perslev/CanvasSync',
      license="LICENSE.txt",
      packages=["CanvasSync", "CanvasSync/CanvasEntities", "CanvasSync/Settings", "CanvasSync/Statics"],
      scripts=['bin/canvas.py'],
      install_requires=["requests", "pycrypto", "py-bcrypt", "six"],
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX',
                   'Programming Language :: Python',
                   'License :: OSI Approved :: MIT License']
     )
