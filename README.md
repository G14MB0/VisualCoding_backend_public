# Visual Coding Software
### *** THIS IS ONLY THE SERVER ***
In this repository you'll find the server (logic + API + database) for a fully functional visual coding software build with React and Electorn (Frontend repo, look below for the link) and Python (this repo).

This software is just a base sw, intended to be expanded for custom, specific usages and it's written by taking this Idea on mind.

In order to make this working, clone both this and the frontend repo, create an executable of the backend repo (for example using pyinstaller) and put the exec. in the "server" folder of the frontend repo. then run the command "npm run build" followed by "npm run electron:serve" in the frontend folder to create an installer for the sw. 
Many customization can be made before all those steps. 


## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Usage](#usage)
- [License](#license)
- [Authors and Acknowledgments](#authors-and-acknowledgments)

## Features
All the features of this software are inside of the nodes so, any listed feature is also a node in the software.
Nodes can be added by the user before the packaging and, if so, they must be hardcoded both on the frontend and backend.
in order to do so you have to:
- create a custom node mantaining the same format of the others contained in ./lib/nodes/node.py
- add it's definition in ./lib/nodes/utils.py as describend in the file header comment
- Create the node in the frontend as described in the frontend repo docs
- Rebuild all

List of the software's nodes features:
- Algebraic operations
- Local and global variable management
- Signals and portals
- Demuxer
- Timer nodes
- Function node for Python scripts
- Many more...


## Prerequisites

- Python (version 3.8.x or greater)
- Node.js (I used version 10.1.0 but can works with other)
- all dependencies depicted in package.json and requirements.txt (the last in backend repo)

## Installation

both this and the backend repo must be packaged.
for a simpler usage process, here the istallation folder: ->

### Since I'm using pyinstaller, there's the possibility that the antivisur recognise the .exe made by pyinstaller as a trojan. If so, you need to make an installer by yourself and avoid using my installton folder.

### Frontend

On the frontend repo


### Backend

This is the procedure to create a distributable using pyinstaller:
- using auto-py-to-exe, use main.py (root folder) as the main file, then add lib and app folder. built as desktop (console) application since the process will be spawned with the console hidden by Electron in the frontend.
- using pyinstaller terminal command, replicate the above description following pyinstaller docs


## Usage

To use the software, you can interact with API (default APIs docs at 127.0.0.1:12345/docs)


## License

This software is released under the MIT License. This license permits free use, modification, and distribution, under the conditions that the license and copyright notice are included with all copies or substantial portions of the software. For more details, see the LICENSE file in the source distribution.

## Authors and Acknowledgments

Gianmaria Castaldini

