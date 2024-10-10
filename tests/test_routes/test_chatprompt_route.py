from chatbot.db.models.chat_prompt import ChatPrompt
from chatbot.db.models.chat_response import ChatResponse
from chatbot.db.models.content_type import ContentType
from chatbot.db.models.languages import Languages
from chatbot.db.models.model_type import ModelType
from chatbot.db.models.user_role import UserRole
from chatbot.db.models.user import User



def add_data_for_prompt(db):
    user=db.query(User).filter(User.user_name=="ajk").first()
    chatprompt=ChatPrompt(prompt="Hello",created_by=user.id,content_type_id=1,model_type=1,language_type=1)
    db.add(chatprompt)
    db.commit()
    qu=db.query(ChatPrompt).filter(ChatPrompt.created_by==user.id).order_by(ChatPrompt.created_date.desc()).first()
    chatresponse=ChatResponse(prompt_id=qu.id,response="Hello",content_type=1,language_type=1)
    db.add(chatresponse)
    db.commit()


def add_dependent_data(db):
    contenttype=ContentType(id=1,type="text")
    modeltype=ModelType(id=1,type="gpt")
    language=Languages(id="1",name="English",lang_code='eng')
    language2=Languages(id="2",name="Telugu",lang_code='tel')
    db.add(language)
    db.add(language2)
    db.add(contenttype)
    db.add(modeltype)
    db.commit()
    

def test_get_prompts(client,db_session,login):
    add_dependent_data(db=db_session)
    add_data_for_prompt(db=db_session)
    response = client.get("/chat")
    payload=response.json()['response']
    assert response.status_code == 200
    assert payload[0]['prompt']=='Hello'
    assert payload[0]['response']=='Hello'
    assert payload[0]['isreversed']==False
    assert payload[0]['language_type']==1
    assert payload[0]['istranslated']==False
    assert payload[0]['translated_prompt']==None
    assert payload[0]['translated_language_id']==None

def test_get_prompts_empty(client,db_session,login):
    response = client.get("/chat")
    payload=response.json()['response']
    assert response.status_code == 200
    assert payload==[]

def test_add_new_prompt(client,db_session,login):
    add_dependent_data(db=db_session)
    data={"prompt":"my name is not translated"}
    response = client.post("/chat",json=data)
    payload=response.json()['response']
    assert response.status_code == 200

def test_add_new_prompt_reversed(client,db_session,login):
    add_dependent_data(db=db_session)
    data={"prompt":"my name is not translated"}
    response = client.post("/chat?reverse=true",json=data)
    payload=response.json()['response']
    assert response.status_code == 200

def test_add_new_prompt_reversed_translate(client,db_session,login):
    add_dependent_data(db=db_session)
    data={"prompt":"my name is not translated"}
    response = client.post("/chat?reverse=true&lang=tel",json=data)
    payload=response.json()['response']
    assert response.status_code == 200