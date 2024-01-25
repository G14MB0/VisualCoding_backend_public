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

    filePath = ""
    if data.filePath == "":
        filePath = tk_save_as()
    else:
        filePath = clean_file_path(data.filePath)
    
    print(filePath)
    # Get the nodes and edges data
    toSave = getNodesAndEdges()
    # Convert the data to a JSON string
    data_str = json.dumps(toSave, indent=4)
    # Save the JSON string to a file with the .r2f extension
    with open(filePath, 'w') as file:
        file.write(data_str)
    return {'filePath': filePath}



@router.get("/load/")
async def load_graph():

    filePath = tk_selectFile(fileType="r2f")
    # Open the file with the .r2f extension
    with open(filePath, 'r') as file:
        # Parse the JSON string in the file to a Python dictionary
        data = json.load(file)
    updateNodesAndEdges(data)
    return {'filePath': filePath}

    


@router.websocket("/ws/info/start")
async def websocket_endpoint_info(websocket: WebSocket):

    # Accept 
    await websocket.accept()
    consecutive_not_running_count = 0
    try:
        while True:
            # Wait for a notification of change
            messageDict = await asyncio.wait_for(global_var.notificationQueue.get(), timeout=2)
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