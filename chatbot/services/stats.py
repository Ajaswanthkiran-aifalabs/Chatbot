
from sqlalchemy.orm import Session
from sqlalchemy import func,case
from chatbot.db.models.chat_prompt import ChatPrompt
from chatbot.db.models.chat_response import ChatResponse
from chatbot.db.models.languages import Languages
from chatbot.schema.response import StatsResponse
from helpers.response_type_enum import ResponseType

def stats_services(db: Session):

    try:
        q1 = db.query(ChatPrompt.prompt).filter(ChatPrompt.isdeleted==False).count()
        
        q2=db.query(ChatPrompt.istranslated).filter(ChatPrompt.istranslated == True).count()
        
        q3=db.query(ChatPrompt.isreversed).filter(ChatPrompt.isreversed == True).count()
                
                
        
        q = db.query(Languages.name,func.count(ChatPrompt.translated_language_id).filter(ChatPrompt.translated_language_id!=None))\
                .join(Languages, ChatPrompt.translated_language_id == Languages.id).group_by(Languages.name)

      
        return {
            "response": {"no_of_echo_messages":q1,
                         "no_of_translated_messages":q2,
                         "no_of_reversed_messages":q3,
                         "no_of_translated_messages_in_to_each_lang":q},
            "response_type": ResponseType.json
        }
        
    except Exception as e:
        return {
            "error": {
                "status_code": 400,
                "message": str(e)
            }
        }


    

def stats_by_user_services(db: Session,user_id):

    try:
        q1 = db.query(ChatPrompt.prompt).filter((ChatPrompt.isdeleted==False) & (ChatPrompt.created_by==user_id)).count()
        
        q2=db.query(ChatPrompt.istranslated).filter((ChatPrompt.istranslated == True) & (ChatPrompt.created_by==user_id)).count()
        
        q3=db.query(ChatPrompt.isreversed).filter((ChatPrompt.isreversed == True) & (ChatPrompt.created_by==user_id)).count()
                
                
        
        q = db.query(Languages.name,func.count(ChatPrompt.translated_language_id).filter(ChatPrompt.translated_language_id!=None))\
                .join(Languages, ChatPrompt.translated_language_id == Languages.id).filter(ChatPrompt.created_by==user_id).group_by(Languages.name)

       
        return {
            "response": {"no_of_echo_messages":q1,
                         "no_of_translated_messages":q2,
                         "no_of_reversed_messages":q3,
                         "no_of_translated_messages_in_to_each_lang":q},
            "response_type": ResponseType.json
        }
        
    except Exception as e:
        return {
            "error": {
                "status_code": 400,
                "message": str(e)
            }
        }


    