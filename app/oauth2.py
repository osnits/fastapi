from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import engine, get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # the end point of our loging process 

#SECRET_KEY
#algorithms 
#expiration_time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            id: str = payload.get("user_id")

            if id is None:
                raise credentials_exception
            
            #just for data validation -> what all data are there
            token_data = schemas.TokenData(id=id)
        except JWTError:
            raise credentials_exception
        
        return token_data
        
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    #fetching user in this protected path 
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user