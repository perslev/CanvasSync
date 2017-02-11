CanvasSync helps students automatically synchronize modules, assignments & files located on their institutions Canvas web server
to a mirrored folder on their local computer. It traverses the folder hierarchy in Canvas from the top course level down to individual
items and creates a similar folder structure on the local computer.

First, CanvasSync creates a folder hierarchy on the local computer reflecting the 'Modules' section on the Canvas server.
Files are stored in folders such as ../CanvasFolder/Course/Module/SubFolder/file.txt. Both regular files, links to external
web pages as well as Canvas 'Pages' (HTML pages) representing assignments etc. may be downloaded. In addition, CanvasSync
may download Canvas Assignments along with all linked files that can be found in the description of the assignment. Both
files stored on Canvas as well as external files will be detected.
Lastly, all files that do not fall into the above categories are downloaded and stored in the 'Various Files' folder.

See https://github.com/perslev/CanvasSync for additional info and source code.
