from app import schemas
from lib import global_var
from app.database import get_db
from app import models
import json
from sqlalchemy.orm import Session

#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends
import re

from typing import List

router = APIRouter(
    prefix="/functions",
    tags=['Functions']
)


@router.get("/", response_model=List[schemas.GetNode])
def getAllFuncitons(db: Session = Depends(get_db)):
    functions = db.query(models.Nodes).all()
    return functions


@router.post("/")
def addFunciton(data: schemas.AddNode, db: Session = Depends(get_db)):

    print(data)
    newNode = models.Nodes(type=data.type,
                           data=json.dumps(data.data),
                           style=json.dumps(data.style),
                           category=data.category,
                           name=data.name)
    
    db.add(newNode)
    db.commit()
    db.refresh(newNode)
                           
    return newNode


@router.post("/delete")
def deleteFunction(data: schemas.DeleteNode, db: Session = Depends(get_db)):

    # Use the filter() method to find nodes with the matching type
    affected_rows = db.query(models.Nodes).filter(models.Nodes.name == data.name).delete()
    # If no rows were affected, it means no nodes matched the type to be deleted
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Node not found")

    # Commit the changes to the database
    db.commit()

    return {"detail": f"{affected_rows} node(s) deleted"}
