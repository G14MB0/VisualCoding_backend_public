#database, schemas and models
# from .. import schemas

#fastAPI things
from fastapi import APIRouter
from lib.tkinter.methods import *
import os
import subprocess
from lib.local_config import config_folder_path


router = APIRouter(
    prefix="/tkinter",
    tags=['WindowsFileExplorer']
)


@router.get("/")
def getInfo():
    return "FileExplorer"


@router.get("/file")
async def selectFile():
    """open a windows filedialog window to select a file path without path parameter
    """   
    file = await run_file_dialog("")
    return file

@router.get("/file/{filetype}")
async def selectFile(filetype = ""):
    """open a windows filedialog window to select a file path

    Args:
        filetype (_type_): the type of the file. must be inserted as without the dot (dbc and not .dbc)

    Returns:
        _type_: the path of the selected file
    """    
    file_path = await run_file_dialog(filetype)
    print(file_path)
    return file_path


@router.get("/folder")
async def selectFolder():
    folder_path = await run_folder_dialog()
    print(folder_path)
    return folder_path


@router.get("/openfolder/{folder}")
def openFolder(folder):
    if folder == "config":
        # Check if the path is a valid directory
        if os.path.isdir(config_folder_path):
            # Open the folder using the default file explorer
            subprocess.Popen(f'explorer "{config_folder_path}"')
        else:
            return "The folder does not exist."
    
    elif folder == "log":
        # Check if the path is a valid directory
        if os.path.isdir("C:\\VisualCoding"):
            # Open the folder using the default file explorer
            subprocess.Popen(f'explorer C:\\VisualCoding')
        else:
            return "The folder does not exist."