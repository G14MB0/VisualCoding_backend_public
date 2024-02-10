from app import schemas
from lib.node.utils import *
from lib.tkinter.methods import *
from lib import global_var
#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends, WebSocket, WebSocketDisconnect
import re
#pydantic things
from typing import  List #list is used to define a response model that return a list
import json
import traceback

router = APIRouter(
    prefix="/nodes",
    tags=['nodes']
)


@router.post("/graph/")
async def update_graph(graph_data: schemas.GraphData):
    print("updating nodes...")
    updateNodesAndEdges(graph_data.dict())
    # Process the graph data as needed
    return {"message": "Graph data received", "data": graph_data}


@router.get("/plot/")
async def update_graph():
    plotGraph()
    # Process the graph data as needed
    return {"message": "data plotted"}


@router.get("/nodes")
def getNodes():
    return getNodesAndEdges()


@router.get("/run")
def run_raph():
    runGraph()
    return {"message": "running"}


@router.get("/stop")
def stop_Graph():
    stopGraph()
    return {"message": "stopped"}



def clean_file_path(file_path):
    # Use a regular expression to remove invisible control characters
    clean_path = re.sub(r'[\u200e\u200f\u202a\u202b\u202c\u202d\u202e]', '', file_path)
    return clean_path


@router.post("/save/")
async def save_graph(data: schemas.Save):

    try:
        filePath = ""
        if data.filePath == "":
            filePath = await run_save_as_dialog(file_types=[("VisualCoding","vscd")])
        else:
            filePath = clean_file_path(data.filePath)
        
        print(filePath)
        # Get the nodes and edges data
        graphSchema = getNodesAndEdges()
        toSave = {
            "graphSchema": graphSchema,
            "globalVar": global_var.globalVarDict
        }
        # Convert the data to a JSON string
        data_str = json.dumps(toSave, indent=4)
        # Save the JSON string to a file with the .r2f extension
        with open(filePath, 'w') as file:
            file.write(data_str)
        return {'filePath': filePath}
    except:
        print(traceback.print_exc())
        return {'filePath': ""}



@router.get("/load/")
async def load_graph():

    try:
        file_path = await run_file_dialog("vscd")
        # Open the file with the .r2f extension
        with open(file_path, 'r') as file:
            # Parse the JSON string in the file to a Python dictionary
            data = json.load(file)
        updateNodesAndEdges(data['graphSchema'])
        global_var.globalVarDict = data['globalVar']
        return {'filePath': file_path}
    except:
        return {'filePath': ""}



@router.get("/globalvar/")
def getGlobalVar():
    return global_var.globalVarDict


@router.post("/globalvar/")
def addGlobalVar(data: schemas.GlobalVar):
    if not data.name in global_var.globalVarDict.keys():
        global_var.globalVarDict[data.name] = None
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Already defined this global variable: {data.name}")
    return {"message": f"successfully added new global variabl: {data.name}"}


@router.post("/globalvar/delete")
def deleteGlobalVar(data: schemas.GlobalVar):
    if data.name in global_var.globalVarDict.keys():
        global_var.globalVarDict.pop(data.name, None)
    return {"message": f"{data.name} delete"}



@router.websocket("/ws/info/start")
async def websocket_endpoint_info(websocket: WebSocket):

    timeout = getattr(global_var, "biggerTimerValue", None)
    timeout = timeout + 1 if timeout else timeout
    await asyncio.sleep(0.5)
    # Accept 
    await websocket.accept()
    try:
        while True:
            # Wait for a notification of change
            messageDict = await asyncio.wait_for(global_var.notificationQueue.get(), timeout=timeout)
            # If there are messages, send them as a single array
            if messageDict:
                await websocket.send_text(json.dumps(messageDict))

    except asyncio.TimeoutError:
        print("Timeout due to inactivity. Disconnecting.")
        await websocket.close()
    except WebSocketDisconnect:
        # Handle the disconnect
        print("WebSocket disconnected")
        # Exit the while loop
        return
    except Exception as e:
        print(e)
        print("WebSocket disconnected")
        return