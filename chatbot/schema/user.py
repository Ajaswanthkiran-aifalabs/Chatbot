from pydantic import BaseModel,field_validator
from uuid import UUID

class User(BaseModel):
    id: UUID
    name: str
    user_name: str
    password: str

    @field_validator("name")
    def name_validation(cls,name):
        if len(name)<3:
            raise ValueError('name must be atleast 3 characters')
        return name
    
    @field_validator("user_name")
    def user_name_validation(cls,user_name):
        if len(user_name)<3:
            raise ValueError('name must be atleast 3 characters')
        return user_name


class GetUsers(BaseModel):
    name: str
    user_name: str

class AddUsers(BaseModel):
    name: str
    user_name: str
    password: str
    @field_validator("name")
    def name_validation(cls,name):
        if len(name)<3:
            raise ValueError('name must be atleast 3 characters')
        return name
    
    @field_validator("user_name")
    def user_name_validation(cls,user_name):
        if len(user_name)<3:
            raise ValueError('name must be atleast 3 characters')
        return user_name

class UpdateUser(BaseModel):
    name: str
    user_name: str
    @field_validator("name")
    def name_validation(cls,name):
        if len(name)<3:
            raise ValueError('name must be atleast 3 characters')
        return name
    
    @field_validator("user_name")
    def user_name_validation(cls,user_name):
        if len(user_name)<3:
            raise ValueError('name must be atleast 3 characters')
        return user_name

    