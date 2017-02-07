# CanvasSync
Synchronise files located on a Canvas by Instructure server to your local computer

Description
-----------
PyEx makes an entire Python project folder (or a single Python module file) globally executable in
Bash through the following sequence of steps:

* PyEx will either move a single Python module or zip the content of an entire Python project folder
into a pre-specified folder that has been added to the Bash path variable.
* The module or zip archive will be padded with a shebang line directing Bash to the appropriate Python interpreter.
* The module or zip archive is finally made executable to the user using chmod (a+x).

Requirements
------------
- Requests (http://docs.python-requests.org/en/master/)
- PyCrypto (https://pypi.python.org/pypi/pycrypto)
- py-bcrpt (https://pypi.python.org/pypi/pycrypto)

Usage example
-------------
```
pyex -i /path/to/favorite/project -n FavProject -v 2.7
```

Will make the project at the specified path globally accessible and executable in Bash using the command "FavProject". The -v flag specifies the Python interpreter version (optional).

Note: If a project folder is made executable using PyEx, the top-level folder of the zip archive must include a
\_\_main\_\_.py file containing the main function calls. This is not required if PyEx is used on single Python modules.
