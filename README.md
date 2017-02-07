# CanvasSync
Synchronise files located on a Canvas by Instructure web server to your local computer.

Description
-----------
CanvasSync helps students automatically synchronize all files located on their institutions Canvas web server
to their local computer. It traverses the folder hierarchy in Canvas from the top course level down to individual
files and creates a similar folder structure on the local computer.

CanvasSync uses the Canvas LMS API (https://canvas.instructure.com/doc/api/) to pull resources on a Canvas server. In
order to authenticate as the user an authentication token mut be generated on the Canvas web server under the
'Accounts --> Settings' menu as showed below:



*

Requirements
------------
The CanvasSync module has the following dependencies:

- Requests  (http://docs.python-requests.org/en/master/)
- PyCrypto  (https://pypi.python.org/pypi/pycrypto)
- py-bcrypt (http://www.mindrot.org/projects/py-bcrypt/)

Using PIP the latest versions may be installed by executing the following commands:
```
pip install requests
pip install pycrypto
pip install py-bcrypt
```

Usage examples
--------------
CanvasSync may be invoked by pointing the interpreter to either the CanvasSync folder or the __main__ file
located at ../CanvasSync/__main__.py
```
python CanvasSync
```
* NOTE that it is important that the main folder is not renamed, it must be named CanvasSync for module imports to work.

When launched without commandline arguments, CanvasSync will start synchronizing with previously specified settings or
prompt the user to enter new settings.

Command line arguments:
-i or --info will display the currently saved settings
-s or --setup will prompt the user to reinitialize settings
-h or --help will show the help screen
