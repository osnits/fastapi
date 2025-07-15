#conda create --name <env_name> --file requirements.txt
#pip install -r requirements.txtcond

from fastapi import FastAPI
from app.database import engine
from . import models, config
from .routers import post, user, auth, vote

#to allows other domains to talk to our 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# who (domains) can talk to us
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)



#create our models from the engine
#models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# the decorator turns a fun into path operation
@app.get("/") # "/" the url pat
# the name of fun does not matter 
async def root():
    return {"message": "Hello World"} # -> automatically convert dict into JSON


