from sqlalchemy import Column,Integer,String,UUID,ForeignKey
from uuid import uuid4
from chatbot.db.db import Base
from chatbot.db.models.chat_prompt import ChatPrompt
from chatbot.db.models.content_type import ContentType
from chatbot.db.models.languages import Languages

class ChatResponse(Base):

    __tablename__="chatresponse"
    id=Column(UUID,primary_key=True,default=lambda : uuid4())
    prompt_id=Column(UUID,ForeignKey(ChatPrompt.id),index=True,unique=True)
    response=Column(String,nullable=False)
    content_type=Column(Integer,ForeignKey(ContentType.id))
    language_type=Column(Integer,ForeignKey(Languages.id))
    