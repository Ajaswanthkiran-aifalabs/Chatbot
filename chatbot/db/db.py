
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import declarative

Base=declarative.declarative_base()
engine=create_engine(url="postgresql://postgres:1234@127.0.0.1:5432/chatbot",echo=True)
Session=sessionmaker(bind=engine,autoflush=False,autocommit=False)

def get_db():
    session=Session()
    try:
        yield session
    finally:
        session.close()


