
from sqlalchemy import Column,DateTime,func,Boolean

class MixinLog(object):
    created_date=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_date=Column(DateTime(timezone=True),nullable=True,onupdate=func.now())

class MixinDelete(object):
    isdeleted=Column(Boolean,default=False)