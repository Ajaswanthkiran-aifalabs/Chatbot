from chatbot.db.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from chatbot.schema.user import AddUsers,UpdateUser
from helpers.response_type_enum import ResponseType
def get_all(db:Session):

    try:
        return db.query(User).all()
    except Exception as exp:
        return { "error":   { 
                        "status_code": 400,
                        "message":"Can't retrive all the users"
                    }
                }
        

def add(user: AddUsers, db: Session ):
    try:
        db.add(user)
        db.commit()
        return { 
                "response": True,
                "response_type": ResponseType.boolean
                }
    except Exception as exp:
        return { "error":{  
                    "status_code": 400,
                    "message":"Error adding user"
                    }
                }

def update(user: UpdateUser,db:Session):
    try:
        update_user=db.query(User).filter(User.user_name==user.user_name).first()
        update_user.name=user.name
        db.commit()
        return { 
                    "response": True,
                    "response_type": ResponseType.boolean
                }
    except Exception as exp:
        return { "error":{
                        "status_code": 400,
                        "message":"Error Updating user"
                    }
                }
        

def delete(user_name:str,db: Session):

    try:
        u=db.query(User).filter(User.user_name==user_name).first()
        u.isdeleted=True
        db.commit()
        return { 
                "response": True,
                "response_type": ResponseType.boolean
                }
    except Exception as exp:
        return { "error":{ 
                        "status_code": 400,
                        "message":str(exp)
                        }
                }
