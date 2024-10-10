from sqlalchemy import String,Column,UUID,Boolean,ForeignKey,Integer
from helpers.mixin_models import MixinDelete
from uuid import uuid4
from chatbot.db.db import Base
from chatbot.db.models.user_role import UserRole

class User(Base,MixinDelete):
    __tablename__="user"
    id=Column(UUID,default=lambda: uuid4(),primary_key=True)
    name=Column(String,nullable=False)
    user_name=Column(String,nullable=False,unique=True,index=True)
    password=Column(String,nullable=False)
    role=Column(Integer, ForeignKey(UserRole.id))

