from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from chatbot.db.db import get_db

from chatbot.schema.login import Login

from chatbot.db.models import user
from chatbot.schema.response import Response
from helpers.response_type_enum import ResponseType
from fastapi.security import OAuth2PasswordRequestForm

from chatbot.services import login as c, token
router=APIRouter(
    prefix="/login",
    tags=["Login"]
)


@router.post("", response_model=Response)
def login(details: OAuth2PasswordRequestForm= Depends(),db: Session=Depends(get_db)):
    print(details)
    res=c.check(details.username,details.password,db)
    if not res:
        return False
    user_id=str(res.id)
    access_token = token.create_access_token(
            data={"sub": res.user_name,"user_id":user_id})
    return { 
                "response": {
                        "access_token":access_token
                    },
                "response_type": ResponseType.json
                }