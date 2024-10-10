from fastapi import APIRouter,Depends,Request,File
from typing import Annotated
from chatbot.db.db import get_db
from sqlalchemy.orm import Session
from chatbot.services.chat_prompt import get,add,update,delete
from chatbot.schema.chat_prompt import ChatPrompt,AddChatPrompt
from chatbot.schema.response import Response
from uuid import UUID
router=APIRouter(
    tags=['Chat Prompt CRUD'],
    prefix="/chat"
)

@router.get("",response_model=Response)
def get_all_chats(request:Request,db: Session=Depends(get_db)):
    user_id=request.state.user_id
    return get(db=db,user_id=user_id)

#file: Annotated[bytes,File()] | None,
@router.post("",response_model=Response)
def add_prompt(request :Request,prompt: AddChatPrompt, reverse: bool=None,lang :str=None,db: Session=Depends(get_db)):
    user_id=request.state.user_id

    return add(details=prompt,db=db,user_id=user_id,content_type=1,reverse=reverse,response_lang=lang)

@router.put("",response_model=Response)
def update_prompt(request: Request,prompt: AddChatPrompt,id : UUID,reverse: bool=None,lang :str=None,db: Session=Depends(get_db)):
    user_id=request.state.user_id

    return update(details=prompt,db=db,user_id=user_id,content_type=1,reverse=reverse,response_lang=lang,prompt_id=id)

@router.delete("",response_model=Response)
def delete_prompt(id: UUID,db: Session=Depends(get_db)):
    return delete(id=id,db=db)