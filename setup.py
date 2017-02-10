#!/usr/bin/env python2.7

from distutils.core import setup

setup(name='CanvasSync',
      version='1.0',
      description='Synchronizes modules, assignments and files from a Canvas server to a local folder',
      author='Mathias Perslev',
      author_email='mathias@perslev.com',
      url='https://github.com/perslev/CanvasSync',
      packages=['CanvasSync', 'CanvasSync/CanvasEntities', 'CanvasSync/Settings', 'CanvasSync/Statics'],
      scripts=['CanvasSync/__main__.py'],
      package_data=['CanvasSync/README.md', 'CanvasSync/requirements.txt']
     )
