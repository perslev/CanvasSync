# CanvasSync
Synchronise files located on a Canvas by Instructure web server to your local computer.

Description
-----------
CanvasSync helps students automatically synchronize files located on their institutions Canvas web server
to their local computer. It traverses the folder hierarchy in Canvas from the top course level down to individual
files and creates a similar folder structure on the local computer:


![alt tag](https://cloud.githubusercontent.com/assets/12041524/22702853/63eaa498-ed62-11e6-9227-de5823cb39c6.png)


CanvasSync uses the Canvas LMS API (https://canvas.instructure.com/doc/api/) to pull resources on a Canvas server. In
order to authenticate as the user an authentication token mut be generated on the Canvas web server under the
'Accounts --> Settings' menu as showed below:


![alt tag](https://cloud.githubusercontent.com/assets/12041524/22701027/c25ccbd8-ed5c-11e6-9ace-c8687e124bc8.png)


The authentication token along with a path pointing to a folder to where the sync will take place and the domain
of the Canvas server must be set up during the initial launch of CanvasSync. These settings will be stored in an
encrypted local file to keep the authentication token secure. Thus, the user must specify a password that must also be
supplied whenever CanvasSync is launched at a later time.

Usage examples
--------------
CanvasSync is launched by pointing the Python interpreter to either the CanvasSync main folder or the __main__.py file
located at ../CanvasSync/__main__.py
```
python /path/to/CanvasSync
```
* NOTE that it is important that the main folder is not renamed, it must be named 'CanvasSync'.

When launched without commandline arguments, CanvasSync will start synchronizing with previously specified settings or
prompt the user to enter new settings if no previous settings could be found.

Command line arguments:
-i or --info will display the currently saved settings
-s or --setup will prompt the user to reinitialize settings
-h or --help will show the help screen


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

Disclaimer
----------
Please note that by using CanvasSync the user allows the software to authenticate with the Canvas server on the users
behalf. CanvasSync stores the authentication key encrypted and locally and the key is never shared with 3rd parties.
The official version of CanvasSync will only pull resources from the server and never remove or modify resources on the
server. Modified/rogue versions of the software could however use the authentication token to remove or modify
resources that the user has access to on the server on the users behalf.

CanvasSync is still in its early version and is not guaranteed to be stable.

Use this software on your own risk :-)


Additional resources
--------------------
https://www.instructure.com
https://canvas.instructure.com/doc/api/index.html
