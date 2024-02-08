from typing import List, Optional, Dict, Any
import json

from pydantic import BaseModel, validator, EmailStr #used as an isistance() to check data type
from datetime import datetime


######################################################
##                     NODE                         ##
######################################################  

# Define a model for the node structure
class Node(BaseModel):
    id: str
    type: str
    data: dict
    style: dict
    position: dict

        

class AddNode(BaseModel):
    type: str
    data: dict
    style: dict
    name: str
    category: str

   

        
class GetNode(BaseModel):
    type: str
    data: dict
    name: str
    style: dict
    category: str

    # Serialize data when dumping to JSON
    class Config:
        json_encoders = {
            dict: lambda v: json.dumps(v)
        }

    @validator('data', 'style', pre=True, each_item=False)
    def parse_json(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                raise ValueError(f"Unable to parse string to dict: {v}")
        return v


class DeleteNode(BaseModel):
    name: str


######################################################
##                     EDGE                         ##
######################################################  
    
# Define a model for the edge structure
class Edge(BaseModel):
    source: str
    target: str
    sourceHandle: str
    targetHandle: str


######################################################
##                     GRAPH                        ##
######################################################  
# Define a model for the complete data structure you expect from React
class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


class FunctionNode(BaseModel):
    id: str
    data: dict


class Save(BaseModel):
    filePath: str = ""


class GlobalVar(BaseModel):
    name: str



######################################################
##                    SETTING                       ##
######################################################  
class SetSetting(BaseModel):
    name: str
    value: str


class Info(BaseModel):
    info: str