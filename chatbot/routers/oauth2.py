

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer


from chatbot.schema.token import TokenData
from chatbot.services.token import verify_token


from fastapi import APIRouter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str =Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token,credentials_exception)
    