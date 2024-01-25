from typing import List, Optional, Dict, Any
import json

from pydantic import BaseModel, validator, EmailStr #used as an isistance() to check data type
from datetime import datetime


######################################################
##              USER OPERATION TOKEN                ##
######################################################  

# Define a model for the node structure
class Node(BaseModel):
    id: str
    type: str
    data: dict
    position: dict

# Define a model for the edge structure
class Edge(BaseModel):
    source: str
    target: str
    sourceHandle: str

# Define a model for the complete data structure you expect from React
class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


class FunctionNode(BaseModel):
    id: str
    data: dict


