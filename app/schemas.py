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

    # # Serialize data when dumping to JSON
    # class Config:
    #     json_encoders = {
    #         dict: lambda v: json.dumps(v)
    #     }

    

        
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

# Define a model for the edge structure
class Edge(BaseModel):
    source: str
    target: str
    sourceHandle: str
    targetHandle: str

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
##                   PYTHONBUS                      ##
######################################################  

class UserChannelConfig(BaseModel):
    hw_channel: int
    serial_number: int
    ch_num: int  #application channel number
    # hw_type: str #this is something like "VN1630" and is then converted in the method to the corresponding int
    bitrate: int = 500000
    fd: bool = False
    data_bitrate: int = 2000000 #if the fd parameter is true, this is used as data bitrate for the arbitration in CAN-FD
    name: str = "" # this is optional but is needed in the log filename.
    txtLog: bool = False


class VectorChannelConfig(UserChannelConfig):
    db_path: str
    maxSize: int = 100 * 1024 * 1024 #default 100 Mb, max file size for logging part
    decode: bool = False
    propagate: str = ""  #this must be a list of element separated by a comma (,). it will be used to propagate the value of those elements in all the code


class RemoveChannel(BaseModel):
    serial_number: int
    name: str
    hw_channel: int

class DAIOstart(BaseModel):
    serial_number: int
    frequency: int = 1000
    ch_num: int


######################################################
##                    SETTING                       ##
######################################################  
class SetSetting(BaseModel):
    name: str
    value: str


class Info(BaseModel):
    info: str