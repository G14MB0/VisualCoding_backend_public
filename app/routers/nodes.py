from app import schemas
from lib.node.utils import *
#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends

#pydantic things
from typing import  List #list is used to define a response model that return a list


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