from fastapi import Request,HTTPException,status
from fastapi.responses import JSONResponse
from chatbot.services.token import verify_token


async def authorization(request: Request, call_next):
    try:
        if request.url.path in ['/login','/docs','/openapi.json']:
            response = await call_next(request)
            return response
        else:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            print(request.headers)
            if "Authorization" not in request.headers:
                raise HTTPException(status_code=404, detail="Authorization Header not found")
            else:
                token=request.headers["Authorization"]
                verification_of_token,user_id=verify_token(token,credentials_exception)
                request.state.user_id=user_id
                if verification_of_token:
                    response = await call_next(request)
                    return response
                else:
                    return JSONResponse(status_code=403,content={"reason":"Validation failed"}) # or 401
    except Exception as er:
        return JSONResponse(status_code=401,content={'reason': str(er)})