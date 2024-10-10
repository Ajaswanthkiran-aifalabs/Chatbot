from fastapi_pagination import Page
from pydantic import BaseModel,Json
from typing import Union,List,Any

from chatbot.schema.history import PaginateHistory


class Error(BaseModel):
    status_code: int
    message: str

class ChatPromptResponse(BaseModel):
    prompt: str
    response: str
    isreversed: bool
    language_type: int
    istranslated: bool 
    translated_prompt: str | None
    translated_language_id: int | None


class StatsResponse(BaseModel):
    no_of_echo_messages: int
    no_of_translated_messages: int
    no_of_reversed_messages: int
    no_of_translated_messages_in_tel: int
    no_of_translated_messages_in_eng: int 
    no_of_translated_messages_in_tamil: int 
    no_of_translated_messages_in_urd: int

class Token(BaseModel):
    access_token: str
    token_type: str="bearer"

class Response(BaseModel):
    error: Error = None
    response: List[ChatPromptResponse] | StatsResponse | Token | bool | str =None
    response_type: str= None
