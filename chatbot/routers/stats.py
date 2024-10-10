from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from chatbot.db.db import get_db
from chatbot.schema.response import Response
from chatbot.schema.user import GetUsers,UpdateUser,AddUsers
from chatbot.services.stats import stats_services,stats_by_user_services
from chatbot.services.user import get_all,add,update,delete
from chatbot.db.models.user import User
from chatbot.services.hassing import becrypt

router=APIRouter(
    prefix="/stats",
    tags=['stats']
)


@router.get("")
def get_stats(db: Session=Depends(get_db)):
    return stats_services(db=db)

@router.get("/user")
def get_stats_by_user(request: Request,db: Session=Depends(get_db)):
    user_id=request.state.user_id
    return stats_by_user_services(db=db,user_id=user_id)
