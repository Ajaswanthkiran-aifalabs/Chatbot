from chatbot.db.models.chat_prompt import ChatPrompt
from fastapi import HTTPException,Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from chatbot.schema.chat_prompt import AddChatPrompt
from chatbot.db.models.chat_response import ChatResponse
from chatbot.db.models.languages import Languages
from uuid import UUID
from googletrans import Translator
from iso639 import Lang
from chatbot.schema.response import ChatPromptResponse
from helpers.response_type_enum import ResponseType
import langid
from deep_translator import GoogleTranslator


def get(user_id, db: Session):
    try:
        results = db.query(
                        ChatPrompt.prompt, 
                        ChatResponse.response,
                        ChatPrompt.isreversed,
                        ChatPrompt.language_type,
                        ChatPrompt.istranslated,
                        ChatPrompt.translated_prompt,
                        ChatPrompt.translated_language_id
                    ).join(
                        ChatResponse, ChatPrompt.id == ChatResponse.prompt_id
                    ).filter(
                        ChatPrompt.created_by == UUID(user_id)
                    ).all()

                    # Convert the result to a list of dictionaries
        
        chat_responses = [
            ChatPromptResponse(
                    prompt=prompt,
                    response=response,
                    isreversed=isreversed,
                    language_type=language_type,
                    istranslated=istranslated,
                    translated_prompt=translated_prompt,
                    translated_language_id=translated_language_id
                )
            for prompt, response, isreversed, language_type, istranslated, translated_prompt, translated_language_id in results
        ]
        return {
            "response":chat_responses,
            "response_type": ResponseType.json
        }
    except Exception as exp:
        return { "error":  {
                        "status_code": 400,
                        "message": str(exp)
                    }
                }

# def add(details: AddChatPrompt,db: Session,user_id,content_type,reverse,response_lang):
#     try:
#         translator=Translator(service_urls=['translate.googleapis.com'],raise_exception=False)
#         prompt_lang=translator.detect(text=details.prompt)
#         prompt_pt2_lang=Lang(prompt_lang.lang).pt2b
#         prompt_language_id=db.query(Languages).filter(Languages.lang_code==prompt_pt2_lang).first().id

#         if prompt_pt2_lang==response_lang:
#             raise Exception("The provided prompt language and requested translation language are same.")
        
#         p=ChatPrompt(prompt=details.prompt,created_by=UUID(user_id),content_type_id=content_type,model_type=1,language_type=prompt_language_id)

#         if reverse:
#             details.prompt=details.prompt[::-1]
#             p.isreversed=True
#         if response_lang is not None:
#             p.istranslated=True
#             p.translated_language_id=prompt_language_id=db.query(Languages).filter(Languages.lang_code==Lang(response_lang).pt2b).first().id
#             p.translated_prompt=translator.translate(details.prompt,dest=Lang(response_lang).pt1).text
#         db.add(p)
#         db.commit()
#     except Exception as exp:
#         # HTTPException(status_code=400, detail="Can't insert prompts")
#         return { "error":{ 
#                         "status_code": 400,
#                         "message": str(exp)
#                     }
#                 }

#     last_prompt_id=db.query(ChatPrompt).filter(ChatPrompt.created_by==UUID(user_id)).order_by(ChatPrompt.created_date.desc()).first()

#     try:
#         r=ChatResponse(prompt_id=last_prompt_id.id,response=details.prompt,content_type=1,language_type=p.translated_language_id)
#         if response_lang is not None:
#             r.response=p.translated_prompt
#         db.add(r)
#         db.commit()
#     except Exception as exp:
        
#         return { "error":   
#                     { 
#                         "status_code": 400,
#                         "message": str(exp)
#                     }
#                 }
    
#     return {
#         "response": True,
#         "response_type": ResponseType.boolean
#     }


def add(details: AddChatPrompt,db: Session,user_id,content_type,reverse,response_lang):
    try:
        prompt_lang=langid.classify(details.prompt)[0]
        
        prompt_pt2_lang=Lang(prompt_lang).pt2b
        prompt_language_id=db.query(Languages).filter(Languages.lang_code==prompt_pt2_lang).first().id

        if prompt_pt2_lang==response_lang:
            raise Exception("The provided prompt language and requested translation language are same.")
        
        p=ChatPrompt(prompt=details.prompt,created_by=UUID(user_id),content_type_id=content_type,model_type=1,language_type=prompt_language_id)

        if reverse:
            details.prompt=details.prompt[::-1]
            p.isreversed=True
        if response_lang is not None:
            p.istranslated=True
            p.translated_language_id=prompt_language_id=db.query(Languages).filter(Languages.lang_code==Lang(response_lang).pt2b).first().id
            
            translated = GoogleTranslator(source='auto', target=Lang(response_lang).pt1).translate(details.prompt)
            p.translated_prompt=translated
        db.add(p)
        db.commit()

    except Exception as exp:
        # HTTPException(status_code=400, detail="Can't insert prompts")
        return { "error":{ 
                        "status_code": 400,
                        "message": str(exp)
                    }
                }

    last_prompt_id=db.query(ChatPrompt).filter(ChatPrompt.created_by==UUID(user_id)).order_by(ChatPrompt.created_date.desc()).first()

    try:
        r=ChatResponse(prompt_id=last_prompt_id.id,response=details.prompt,content_type=1,language_type=p.translated_language_id)
        if response_lang is not None:
            r.response=p.translated_prompt
        db.add(r)
        db.commit()
    except Exception as exp:
        
        return { "error":   
                    { 
                        "status_code": 400,
                        "message": str(exp)
                    }
                }
    
    return {
        "response": True,
        "response_type": ResponseType.boolean
    }

def update(details: AddChatPrompt,db: Session,user_id,content_type,reverse,response_lang,prompt_id):
    
    try:
        prev_prompt=db.query(ChatPrompt).filter(ChatPrompt.id==prompt_id).first()
        a=add(details=details,db=db,user_id=user_id,content_type=content_type,reverse=reverse,response_lang=response_lang)

        if "response" not in a:
            raise Exception("The prompt is not updated try again.")

        last_prompt_id=db.query(ChatPrompt).filter(ChatPrompt.created_by==UUID(user_id)).order_by(ChatPrompt.created_date.desc()).first()
        prev_prompt.updated_id=last_prompt_id.id
        db.add(prev_prompt)
        db.commit()
        
        return {
            "response": "Updated Successfully",
            "response_type":ResponseType.text
    }
    except Exception as exp:

        return { "error":   
                    { 
                        "status_code": 400,
                        "message":  str(exp)
                    }
                }
    
   

def delete(id,db: Session):

    try:
        p=db.query(ChatPrompt).filter(ChatPrompt.id==id).first()

        if p.isdeleted or p is None:
            raise Exception("Can't find or already deleted")
        p.isdeleted=True
        db.add(p)
        db.commit()
        return { 
                "response": True,
                "response_type": ResponseType.boolean
                }
    except Exception as e:
        return { "error":   
                    { 
                        "status_code": 400,
                        "message":str(e)
                    }
                }
