import datetime
from dataclasses import field
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, SerializeAsAny

from filter.data_models import Condition
from option.aggregate import Option
from vote.aggregate import Vote


class ReadFullVote(BaseModel):
    vote: Vote
    options: list[Option]


class UpdateOption(BaseModel):
    title: str
    ordering: int


class UpdateVote(BaseModel):
    title: str
    prompt: str
    filter: Optional["UpdateVoteFilter"] = None


class UpdateVoteFilter(BaseModel):
    id: UUID
    version: int


class UpdateFilter(BaseModel):
    title: str
    condition: Condition
