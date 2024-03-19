from uuid import UUID
from fastapi import FastAPI

from votigo.application import Votigo

app = FastAPI()
votigo = Votigo()

@app.post("/vote")
def create_vote(creator: UUID):
    vote_id = votigo.create_vote(creator)
    return read_vote(vote_id)

@app.get("/vote/{vote_id}")
def read_vote(vote_id: UUID):
    return votigo.get_vote(vote_id)