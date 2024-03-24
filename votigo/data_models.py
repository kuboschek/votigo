

from dataclasses import field
import datetime
from uuid import UUID
from pydantic import BaseModel, Field, SerializeAsAny

from option.aggregate import Option
from vote.aggregate import Vote

class ReadFullVote(BaseModel):
    vote: Vote
    options: list[Option]

class UpdateOption(BaseModel):
    title: str
    ordering: int