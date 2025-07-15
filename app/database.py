from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor 
import time

from .config import settings
# where our postgres DB is located -> each DB has an unique url
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/apicourse"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#engine is responsible for connecting to Posgres DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
        raise
    

#just for connecting to DB to use raw SQL
""" # par: host: ip to connnect to; database; username; password
while True:    
    try:
        conn = psycopg2.connect(host='localhost', database='apicourse', user='postgres', password='123', cursor_factory = RealDictCursor) 
        # just give values, no cols names, so add RealDictCursor for this
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as error:
        print("Connecting to DB failed")
        print("Error: ", error)
        time.sleep(2) # other very fast comsuming looping 
 """