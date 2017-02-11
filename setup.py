#!/usr/bin/env python2.7

from distutils.core import setup


setup(name='CanvasSync',
      version='0.1.1',
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
