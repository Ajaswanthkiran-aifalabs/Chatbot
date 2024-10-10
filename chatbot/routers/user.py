from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from chatbot.db.db import get_db
from chatbot.schema.user import GetUsers,UpdateUser,AddUsers
from chatbot.services.user import get_all,add,update,delete
from chatbot.db.models.user import User
from chatbot.services.hassing import becrypt
router=APIRouter(
    prefix="/user",
    tags=['user']
)

@router.get("",response_model=list[GetUsers])
def get_all_users(db: Session=Depends(get_db)):
    return get_all(db=db)

@router.post("")
def add_user(user: AddUsers,db: Session=Depends(get_db)):
    return add(user=User(name=user.name, user_name=user.user_name, password=becrypt(user.password)),db=db)

@router.put("")
def updat_user(user: UpdateUser,db: Session=Depends(get_db)):
    return update(user=user,db=db)

@router.delete("")
def delete_user(user_name: str,db: Session=Depends(get_db)):
    return delete(user_name=user_name,db=db)

    