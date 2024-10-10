from sqlalchemy import Integer,String,Column
from chatbot.db.db import Base

class UserRole(Base):

    __tablename__="userrole"
    id=Column(Integer,nullable=False,primary_key=True)
    role=Column(String,nullable=False,unique=True)
