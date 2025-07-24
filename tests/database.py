from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base

from alembic import command

import pytest


#SQLALCHEMY_DATABASE_URL =  "postgresql://postgres:123@localhost/apicourse"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
#engine is responsible for connecting to Posgres DB

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)

#another fixture that returns the DB
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    except:
        db.close()
        raise

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # every time where route has get_db(), it will call override_get_db()     
    app.dependency_overrides[get_db] = override_get_db
    # "with" gives no global Clients
    with TestClient(app) as test_client:
        yield test_client

