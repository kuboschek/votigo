import os
from uuid import UUID

from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from auth.middleware import CurrentUser, FakeUser
from votigo.application import Votigo



app = FastAPI()
votigo = Votigo()

if os.getenv("FAKE_AUTH") == "true":
    User = FakeUser
else:
    User = CurrentUser

@app.post("/vote")
def create_vote(creator: UUID, user: User):
    vote_id = votigo.create_vote(creator)
    return read_vote(vote_id)

@app.get("/vote/{vote_id}")
def read_vote(vote_id: UUID):
    return votigo.get_vote(vote_id)