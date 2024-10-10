from datetime import datetime
from pydantic import BaseModel

class PaginateHistory(BaseModel):
    prompt: str 
    response:str 
    language_type:str | None
    isreversed:bool | None
    istranslated:bool | None
    translated_prompt:str | None
    translated_language_id:str | None
    created_date: datetime 