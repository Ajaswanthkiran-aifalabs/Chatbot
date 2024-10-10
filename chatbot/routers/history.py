from fastapi import APIRouter, HTTPException,Request,Depends
from sqlalchemy.orm import Session
from chatbot.db.db import get_db
from uuid import UUID
from chatbot.schema.response import Response
from chatbot.services.history import get_all_service,get_paginate_service,get_paginate_filter_service
from fastapi_pagination import add_pagination,Page
from chatbot.schema.history import PaginateHistory
from helpers.response_type_enum import ResponseType
from chatbot.schema.history import PaginateHistory

router=APIRouter(
    tags=['History'],
    prefix='/history'
)



@router.get("",response_model=Response)
def get_all(request:Request,db: Session=Depends(get_db)):
    user_id=request.state.user_id
    return get_all_service(user_id=user_id,db=db)

# @router.get("/paginate",response_model=Page[PaginateHistory])
# def get_paginate(request:Request,page:int,size:int,db: Session=Depends(get_db)):
#     try:
#         user_id=request.state.user_id
#         param=Params(page=page,size=size)
#         q=get_paginate_service(user_id=user_id,db=db)
#         return paginate(q,param)
#     except:
#         return { "error":   { "Status code": 422,
#                             "message":"Error occured during the pagination"
#                             },
#                 "response": None,
#                 "response type": None
#                 }
    
@router.get('/paginate',response_model=Page[PaginateHistory])
def get_paginate_filter(request:Request,sort_by:str,sort_order: str="asc",search_by:str=None,istranslated:bool=True,translated_language_id:int=None,isreversed:bool=False,db: Session=Depends(get_db)):
    try:
        user_id=request.state.user_id

        if istranslated==False and translated_language_id is not None:
            raise Exception("Translated is given flase and translated language is given")
        return get_paginate_filter_service(user_id=user_id,db=db,search_by=search_by,sort_by=sort_by,sort_order=sort_order,istranslated=istranslated,translated_language_id=translated_language_id,isreversed=isreversed)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail={"message": "Error occurred during pagination", "error": str(e)}
        )

add_pagination(router)