#!/usr/bin/env python
from setuptools import setup, find_packages
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


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGES.txt') as readme_file:
    changes = readme_file.read()

with open("requirements.txt") as req_file:
    requirements = list(filter(None, req_file.read().split("\n")))


setup(name='CanvasSync',
      version=get_version(),
      description='Synchronizes modules, assignments and files from a '
                  'Canvas server to a local folder',
      long_description=readme + "\n\n" + changes,
      author='Mathias Perslev',
      author_email='mathias@perslev.com',
      url='https://github.com/perslev/CanvasSync',
      license="LICENSE.txt",
      packages=find_packages(),
      package_dir={'CanvasSync': 'CanvasSync'},
      entry_points={
          'console_scripts': [
              'canvas=bin.canvas:entry',
          ],
      },
      install_requires=requirements,
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX',
                   'Programming Language :: Python',
                   'License :: OSI Approved :: MIT License']
     )
