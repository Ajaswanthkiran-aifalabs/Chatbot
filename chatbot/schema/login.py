from pydantic import BaseModel, Field


class Login(BaseModel):
    username: str
    password: str