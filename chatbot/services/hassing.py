from passlib.context import CryptContext

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

def becrypt(password: str):
    return pwd_cxt.hash(password)

def verify(actual_pass,given_pass):
    return pwd_cxt.verify(given_pass,actual_pass)