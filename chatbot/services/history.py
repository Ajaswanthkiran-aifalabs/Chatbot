from chatbot.db.models.chat_prompt import ChatPrompt
from chatbot.db.models.chat_response import ChatResponse
from chatbot.db.models.languages import Languages
from sqlalchemy.orm import Session,aliased
from sqlalchemy import func,desc,asc,alias
from fastapi import HTTPException
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate
from helpers.response_type_enum import ResponseType
from chatbot.schema.response import ChatPromptResponse

def get_all_service(db: Session,user_id):

    try:
        q=db.query(ChatPrompt.prompt,ChatResponse.response,ChatResponse.language_type,ChatPrompt.isreversed,ChatPrompt.istranslated,ChatPrompt.translated_prompt,ChatPrompt.translated_language_id).join(ChatResponse, ChatResponse.prompt_id==ChatPrompt.id).filter((ChatPrompt.created_by==user_id)& (ChatPrompt.isdeleted==None) | (ChatPrompt.isdeleted==False)).all()
        
        chat_responses = [
            ChatPromptResponse(
                    prompt=prompt,
                    response=response,
                    language_type=language_type,
                    isreversed=isreversed,
                    istranslated=istranslated,
                    translated_prompt=translated_prompt,
                    translated_language_id=translated_language_id
                )
            for prompt, response, language_type,isreversed, istranslated, translated_prompt, translated_language_id in q
        ]
        return {
            "response":chat_responses,
            "response_type": ResponseType.json
        }
    except Exception as e:
        return {
            "error":{
                "status_code": 400,
                "message": "Can't retive the prompts"
            }
        }
        
def get_paginate_service(db: Session,user_id):

    try:
        return db.query(ChatPrompt.prompt,ChatResponse.response,ChatResponse.language_type,ChatPrompt.isreversed,ChatPrompt.istranslated,ChatPrompt.translated_prompt,ChatPrompt.translated_language_id)\
                    .join(ChatResponse, ChatResponse.prompt_id==ChatPrompt.id)\
                    .filter((ChatPrompt.created_by==user_id)& (ChatPrompt.isdeleted==None) | (ChatPrompt.isdeleted==False))\
                    .all()
    except Exception as e:
        return {
            "error":{
                "status_code": 400,
                "message": str(e)
            }
        }

def get_paginate_filter_service(db: Session,user_id,search_by,sort_by,sort_order,translated_language_id:int,istranslated,isreversed):

    mapper={
        "prompt":ChatPrompt.prompt,
        "response": ChatResponse.response,
        "lang":ChatResponse.language_type,
        "date": ChatPrompt.created_date
    }

    is_lan=db.query(Languages).filter(Languages.id==translated_language_id).first()

    if is_lan is None and translated_language_id is not None:
        raise Exception("The provided Language is not avialble")
    
    if search_by is None:
        search_by=""
        
    search_pattern = f"%{search_by}%"

    prompt_lang,translated_lan=aliased(Languages),aliased(Languages)

    q=db.query(ChatPrompt.prompt,ChatResponse.response,prompt_lang.name.label("language_type"),ChatPrompt.isreversed,ChatPrompt.istranslated,ChatPrompt.translated_prompt,translated_lan.name.label('translated_language_id'),ChatPrompt.created_date)\
                .join(ChatResponse, ChatResponse.prompt_id==ChatPrompt.id)\
                .join(prompt_lang,(ChatPrompt.language_type==prompt_lang.id))\
                .outerjoin(translated_lan, (ChatPrompt.translated_language_id == translated_lan.id))\
                .filter((ChatPrompt.created_by==user_id) & (ChatPrompt.isdeleted==False) & ChatPrompt.prompt.ilike(search_pattern) & ((ChatPrompt.translated_language_id==translated_language_id) | (translated_language_id==None)) & (ChatPrompt.isreversed==isreversed) ).order_by(asc(mapper[sort_by]) if sort_order=='asc' else desc(mapper[sort_by]))
    
    if istranslated==False:
        q.filter(ChatPrompt.istranslated==False)

    return paginate(q)

