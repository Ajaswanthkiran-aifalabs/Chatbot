from sqlalchemy import Column,Integer,DateTime,String,Boolean,UUID,ForeignKey
from uuid import uuid4
from chatbot.db.db import Base
from chatbot.db.models.content_type import ContentType
from chatbot.db.models.user import User
from chatbot.db.models.model_type import ModelType
from chatbot.db.models.languages import Languages
from helpers.mixin_models import MixinLog,MixinDelete

class ChatPrompt(Base, MixinLog,MixinDelete):
    __tablename__='chatprompt'

    id=Column(UUID, default=lambda: uuid4(),primary_key=True)
    prompt=Column(String,nullable=False)
    updated_id=Column(UUID)
    model_type=Column(Integer,ForeignKey(ModelType.id))
    content_type_id=Column(Integer,ForeignKey(ContentType.id))
    created_by=Column(UUID,ForeignKey(User.id))
    isreversed=Column(Boolean,default=False)
    language_type=Column(Integer,ForeignKey(Languages.id),nullable=False)
    istranslated=Column(Boolean,default=False)
    translated_prompt=Column(String)
    translated_language_id=Column(Integer,ForeignKey(Languages.id))


    