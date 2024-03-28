import os
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from auth.middleware import CurrentUser, FakeUser, User as UserModel
from vote.aggregate import Vote
from votigo.application import Votigo, AggregateNotFound
from votigo.data_models import ReadFullVote, UpdateOption

tags_metadata = [
    {
        "name": "votes",
        "description": "Votes represent an individual choice users can make.",
    },
    {
        "name": "options",
        "description": "Options represent the individual choices within a vote.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

origins = os.getenv("CORS_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("FAKE_AUTH") == "true":
    User = FakeUser
else:
    User = CurrentUser

votigo = Votigo()

@app.post("/vote", tags=["votes"], response_model=ReadFullVote)
def create_vote(user: User):
    new_vote = votigo.create_vote(user.id)
    return ReadFullVote(vote=new_vote, options=[])


@app.get("/vote/{vote_id}", tags=["votes"], response_model=ReadFullVote)
def read_vote(vote_id: UUID):
    try:
        vote = votigo.get_vote(vote_id)
        options = [votigo.get_option(option_id) for option_id in vote.option_ids]
    except AggregateNotFound:
        raise HTTPException(status_code=404, detail="Vote not found")

    return ReadFullVote(vote=vote, options=options)


@app.post("/vote/{vote_id}/open", tags=["votes"])
def open_vote(vote_id: UUID, user: User):
    return votigo.start_vote(vote_id)


@app.post("/vote/{vote_id}/close", tags=["votes"])
def close_vote(vote_id: UUID, user: User):
    return votigo.stop_vote(vote_id)


@app.post("/vote/{vote_id}/vote", tags=["votes"])
def vote(vote_id: UUID, user: User, option_id: UUID):
    """
        Register a vote for a user on a vote.
    """
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
