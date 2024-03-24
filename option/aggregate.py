from dataclasses import dataclass, field
import datetime
from uuid import UUID
from eventsourcing.domain import Aggregate, event
from pydantic import BaseModel


@dataclass
class Option(Aggregate):
    _id: UUID = field(init=False)
    _created_on: datetime.datetime = field(init=False)
    _modified_on: datetime.datetime = field(init=False)

    title: str = ""
    count: int = 0
    ordering: int = 0
    editable: bool = True

    @event("UpdateTitle")
    def set_title(self, new_title: str):
        self.title = new_title

    @event("UpdateOrdering")
    def update_ordering(self, new_ordering):
        self.ordering = new_ordering

    @event("CountVote")
    def count_vote(self):
        self.count += 1

    @event("LockEditing")
    def lock_editing(self):
        self.editable = False