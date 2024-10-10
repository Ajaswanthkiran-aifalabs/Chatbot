from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class AddChatPrompt(BaseModel):
    prompt: str

class ChatPrompt(AddChatPrompt):
    id: int
    created_by: str
    created_date: datetime 
    updated_date: datetime
    updated_id: UUID=None
    content_type_id: int
    isreversed: bool
    language_type: int
    istranslated: bool
    translated_prompt: str=None
    translated_language_id: int=None
    isdeleted: bool







