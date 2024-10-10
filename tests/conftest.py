from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

from chatbot.services.hassing import becrypt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py

from chatbot.db.db import Base
from chatbot.db.db import get_db
from api_router import router

from middleware import authorization

from chatbot.db.models.user_role import UserRole
from chatbot.db.models.user import User


from fastapi.security import OAuth2PasswordRequestForm

def create_tables():
    """
    This function creates tables which use Base model
    """
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI()
    app.include_router(router=router)
    app.middleware("http")(authorization)
    create_tables()
    return app


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@127.0.0.1:5432/chatbot"
# add _test for test schema
SQLALCHEMY_DATABASE_TEST_SCHEMA = "test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "options": "-csearch_path={}".format(SQLALCHEMY_DATABASE_TEST_SCHEMA)
    },
)

# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def login(db_session,client):
    userroles=UserRole(id=1,role='admin')
    user=User(name="ajk",user_name="ajk",password=becrypt("1234"),role=1)
    db_session.add(userroles)
    db_session.commit()
    db_session.add(user)
    db_session.commit()
    data = {
    "username": "ajk",
    "password": "1234"
    }   
    response = client.post("/login",data=data)
    playload=response.json()
    headers={"Authorization": playload["response"]["access_token"]}    
    client.headers.update(headers=headers)

@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    
    with TestClient(app) as client:
        yield client