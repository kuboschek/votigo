from dataclasses import dataclass, field
import datetime
from uuid import UUID
from eventsourcing.domain import Aggregate, event
from pydantic import BaseModel


class InvalidEdit(Exception):
    pass

@dataclass
class Option(Aggregate):
    # These three are auto-created by the Aggregate class.
    # They are included here so they are serialized in FastAPI.
    _id: UUID = field(init=False)
    _created_on: datetime.datetime = field(init=False)
    _modified_on: datetime.datetime = field(init=False)

    title: str = ""
    count: int = 0
    ordering: int = 0
    editable: bool = True

    def set_title(self, new_title: str):
        if not self.editable:
            raise InvalidEdit("Can't update title on a locked option")

        self._set_title(new_title)

    @event("UpdateTitle")
    def _set_title(self, new_title: str):
        self.title = new_title

    def set_ordering(self, new_ordering: int):
        if not self.editable:
            raise InvalidEdit("Can't update ordering on a locked option")
        
        self._set_ordering(new_ordering)

    @event("UpdateOrdering")
    def _set_ordering(self, new_ordering):
        self.ordering = new_ordering

    def count_vote(self):
        if self.editable:
            raise InvalidEdit("Can't count votes on an option that's still editable")

        self._count_vote()

    @event("CountVote")
    def _count_vote(self):
        self.count += 1

    @event("LockEditing")
    def lock_editing(self):
        self.editable = False