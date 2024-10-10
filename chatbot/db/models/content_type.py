from sqlalchemy import Column,Integer,String
from chatbot.db.db import Base

class ContentType(Base):
    
    __tablename__="contenttype"
    id=Column(Integer,primary_key=True)
    type=Column(String,nullable=False)
    