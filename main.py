import os
from uuid import UUID

from fastapi import Depends, FastAPI

from auth.middleware import CurrentUser, FakeUser
from vote.aggregate import Vote
from votigo.application import Votigo
from votigo.data_models import ReadFullVote, UpdateOption

tags_metadata = [
    {
        "name": "votes",
        "description": "Operations regarding votes",
    },
    {
        "name": "options",
        "description": "Operations regarding options",
    },
]

app = FastAPI(openapi_tags=tags_metadata)
votigo = Votigo()

if os.getenv("FAKE_AUTH") == "true":
    User = FakeUser
else:
    User = CurrentUser


@app.post("/vote", tags=["votes"], response_model=ReadFullVote)
def create_vote(user: User):
    new_vote = votigo.create_vote(user.id)
    return ReadFullVote(vote=new_vote, options=[])


@app.get("/vote/{vote_id}", tags=["votes"], response_model=ReadFullVote)
def read_vote(vote_id: UUID):
    vote = votigo.get_vote(vote_id)
    options = [votigo.get_option(option_id) for option_id in vote.option_ids]

    return ReadFullVote(vote=vote, options=options)


@app.post("/vote/{vote_id}/open", tags=["votes"])
def open_vote(vote_id: UUID, user: User):
    return votigo.start_vote(vote_id)


@app.post("/vote/{vote_id}/close", tags=["votes"])
def close_vote(vote_id: UUID, user: User):
    return votigo.stop_vote(vote_id)


@app.post("/vote/{vote_id}/vote", tags=["votes"])
def vote(vote_id: UUID, user: User, option_id: UUID):
    return votigo.vote(vote_id, user.id, option_id)


@app.post("/vote/{vote_id}/option", tags=["options"])
def add_option(vote_id: UUID, values: UpdateOption):
    return votigo.add_option(vote_id, values)


@app.put("/option/{option_id}", tags=["options"])
def update_option(option_id: UUID, values: UpdateOption):
    return votigo.update_option(option_id, values)


@app.delete("/vote/{vote_id}/option/{option_id}", tags=["options"])
def remove_option(vote_id: UUID, option_id: UUID):
    return votigo.remove_option(vote_id, option_id)
