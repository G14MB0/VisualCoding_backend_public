'''
Here the table models are defined using sqlalchemy by expanding the Base from database.py

models are defined as classes and columns as attributes
'''

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from app.database import Base


class Nodes(Base):
    __tablename__ = "nodes"  # This is used to define the table name

    id = Column(Integer, primary_key=True, nullable=False) # nullable=False means that is not Null
    name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=True)
    data = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))  #this text will put in pgadmin the text inside (now()) so in this case to create the now() default value
    name = Column(String, nullable=False, server_default="new function")

