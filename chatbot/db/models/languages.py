from sqlalchemy import Integer,Boolean,String,Column
from chatbot.db.db import Base

class Languages(Base):
    __tablename__="languages"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    lang_code=Column(String,nullable=False)