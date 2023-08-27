# CanvasSync
Synchronise modules, assignments and files located on a Canvas by Instructure web server to your local computer.

Description
-----------
CanvasSync helps students automatically synchronize modules, assignments & files located on their institutions Canvas web server
to a mirrored folder on their local computer. It traverses the folder hierarchy in Canvas from the top course level down to individual
files and creates a similar folder structure on the local computer:

![](resources/overview.png)

First, CanvasSync creates a folder hierarchy on the local computer reflecting the 'Modules' section on the Canvas server.
Files are stored in folders such as ../SyncFolder/Course/Module/SubFolder/file.txt. Both regular files, links to external
web pages as well as Canvas 'Pages' (HTML pages) representing assignments etc. may be downloaded. In addition, CanvasSync
may download Canvas assignments along with all linked files that can be found in the description of the assignment. Both
files stored on Canvas as well as external files will be detected.
Lastly, all files that do not fall into the above categories are downloaded and stored in the 'Various Files' folder.

The user may specify various settings including:
- What type of items to be synchronized (files, HTML pages, external links)
- If assignments should be synchronized
- If CanvasSync should attempt to find external files described in the assignment description

Installation
-------------
The easiest way to install and run CanvasSync is by using PIP. Download and install CanvasSync along with its
dependencies (see below) by running:

```
pip install CanvasSync
```

Alternatively, download the source distribution from the https://github.com/perslev/CanvasSync/tree/master/dist on GitHub
(.tar.gz for UNIX and .zip for Windows) and run the following command on the distribution file:

```
pip install CanvasSync-<VERSION>.tar.gz
```

Lastly, you may use the supplied setup.py file to create your own source package or built package for your system.

If you choose not to work with PIP, CanvasSync has the following dependencies that must be installed:

Dependencies
---------------
- Requests  (http://docs.python-requests.org/en/master/)
- PyCrypto  (https://pypi.python.org/pypi/pycrypto)
- py-bcrypt (http://www.mindrot.org/projects/py-bcrypt/)
- six (https://pypi.python.org/pypi/six)

Usage examples
--------------
After installation CanvasSync is launched by executing the following command in the console:

```
canvas
```

When launched without commandline arguments, CanvasSync will start synchronizing with previously specified settings or
prompt the user to enter new settings if no previous settings could be found.

Command line arguments:
-i or --info will display the currently saved settings
-s or --setup will prompt the user to reinitialize settings
-h or --help will show the help screen
-S or --sync to synchronize
-p to specify settings password (potentially dangerous)

Setup
----------
CanvasSync uses the Canvas LMS API (https://canvas.instructure.com/doc/api/) to pull resources on the Canvas server. In
order to authenticate with the server an authentication token must be generated on the Canvas web server. This is done by
going to the 'Account' section followed by 'Settings'. Near the bottom under the 'Approved integrations' section, a new authentication
token may be generated. A token is a substitution to the familiar username-password based authentication and allows
3rd party applications such as CanvasSync to authenticate with the Canvas server API and pull resources. Please note that
by supplying an authentication token to the CanvasSync software, you allow CanvasSync to communicate with the Canvas server on
your behalf, see Disclaimer below.

The process of generating a token is illustrated below:

![](resources/auth_token.png)

The authentication token is stored in an local file encrypted using a private password. Consequently, the user must
specify the password whenever CanvasSync is launched to synchronize at a later time. Passwords and/or auth tokens are
cannot and will not be shared with third parties.

Statusbar
----------
For MacOS CanvasSync has also a statusbar, for Windows a icon at the taskbar. From here you can initalise a Synchronisation manually or setup an automatic sync.

<img src="resources/macos_statusbar.png" width="350">   <img src="resources/windows_systemtray.png" width="350">

To run the Statusbar simply execute ```/GUI/macos_statusbar.py``` or ```/GUI/windows_systemtray.py```. You can also add it to the system startup by executing ```/GUI/startup_installer.py```. This script also contains a function to remove the statusbar from the system startup again.

Still ToDo:
- quiting does not work
- preferences GUI still has to be added
(On MacOS the you have to grant CanvasSync access to access the KeyChain. CanvasSync saves the password here. ToDo: Make PopUp to give access if CanvasSync does not have access.)

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
