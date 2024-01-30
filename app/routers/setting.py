from app import schemas

from lib import local_config


#fastAPI things
from fastapi import APIRouter


router = APIRouter(
    prefix="/setting",
    tags=['Settings']
)


@router.get("/")
def getSettings():
    settings = local_config.readLocalConfig()
    return settings


@router.post("/")
def setSetting(data: schemas.SetSetting):
    local_config.writeLocalConfigVariable(data.name, data.value)
    return local_config.readLocalConfig()

@router.get("/openfolder/{folder}")
def openFolder(folder):
    if folder == "config":
        # Check if the path is a valid directory
        if os.path.isdir(config_folder_path):
            # Open the folder using the default file explorer
            subprocess.Popen(f'explorer "{config_folder_path}"')
        else:
            return "The folder does not exist."
    elif folder == "report":
        # Check if the path is a valid directory
        if os.path.isdir(report_folder):
            # Open the folder using the default file explorer
            subprocess.Popen(f'explorer "{report_folder}"')
        else:
            return "The folder does not exist."
    elif folder == "log":
        # Check if the path is a valid directory
        if os.path.isdir(log_folder):
            # Open the folder using the default file explorer
            subprocess.Popen(f'explorer "{log_folder}"')
        else:
            return "The folder does not exist."