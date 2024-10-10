from chatbot.db.models.user import User
from chatbot.services.hassing import verify

def check(username,password,session):
    user=session.query(User).filter(User.user_name==username).first()
    if not verify(user.password,password):
        return  False
    return user
