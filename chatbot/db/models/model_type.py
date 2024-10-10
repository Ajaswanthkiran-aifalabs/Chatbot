from sqlalchemy import Column,Integer,String
from chatbot.db.db import Base

class ModelType(Base):

    __tablename__="modeltype"
    id=Column(Integer,primary_key=True)
    type=Column(String,nullable=False)