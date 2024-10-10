import json
from chatbot.db.models.user_role import UserRole
from chatbot.db.models.user import User


def add_dependent_data(db):
    userrole=UserRole(id=2,role="user")
    user=User(name="ajk2",user_name="ajk2",password="1234",role=2)
    db.add(userrole)
    db.commit()
    db.add(user)
    db.commit()
    
    
def test_get_all_user(client,db_session,login):
    add_dependent_data(db=db_session)
    response = client.get("/user")
    payload=response.json()
    assert response.status_code == 200 
    assert payload[1]['name']=='ajk2'
    assert payload[1]['user_name']=='ajk2'

def test_create_user(client,db_session,login):
    data={"name":'ajk2',"user_name":"ajk2","password":"1234"}
    
    response = client.post("/user",json=data)
    playload=response.json()
    assert response.status_code==200
    assert playload['response']==True

def test_create_user_error(client,db_session,login):
    data={"name":'ajk',"user_name":"ajk","password":"1234"}
    
    response = client.post("/user",json=data)
    playload=response.json()
    assert response.status_code==200
    assert playload['error']['status_code']==400

def test_create_user_error_name(client,db_session,login):
    data={"name":'',"user_name":"ajk2","password":"1234"}
    
    response = client.post("/user",json=data)
    assert response.status_code==422

def test_create_user_error_username(client,db_session,login):
    data={"name":'ajk2',"user_name":"a","password":"1234"}
    
    response = client.post("/user",json=data)
    assert response.status_code==422
   
def test_create_user_error_password(client,db_session,login):
    data={"name":'ajk2',"user_name":"a","password":""}
    
    response = client.post("/user",json=data)
    assert response.status_code==422

def test_update_name_of_user(client,db_session,login):
    data={"name":'ajk2',"user_name":"ajk"}
    response = client.put("/user",json=data)
    assert response.status_code==200
    assert response.json()['response']==True

def test_update_name_of_user_error_wrong_user_name(client,db_session,login):
    data={"name":'ajk2',"user_name":"ajj"}
    response = client.put("/user",json=data)
    assert response.status_code==200
    assert response.json()['error']["status_code"]==400

def test_delete_user_by_user_name(client,db_session,login):
    add_dependent_data(db=db_session)
    response = client.delete("/user?user_name=ajk")
    assert response.status_code==200
    assert response.json()['response']==True

def test_delete_user_by_user_name_error(client,db_session,login):
    add_dependent_data(db=db_session)
    response = client.delete("/user?user_name=ajk1")
    assert response.status_code==200
    assert response.json()['error']['status_code']==400
