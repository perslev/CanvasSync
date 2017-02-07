# CanvasSync
Synchronise files located on a Canvas by Instructure web server to your local computer.

Description
-----------
CanvasSync
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
CanvasSync may be invoked simply by pointing the interpreter either to the CanvasSync folder or the __main__ file
located at ../CanvasSync/__main__.py
```
python CanvasSync
```
When launched without commandline arguments, CanvasSync will start synchronizing with previously specified settings or
prompt the user to enter new settings.

Command line arguments:
$-i$ or $--info$ will display the currently saved settings.
