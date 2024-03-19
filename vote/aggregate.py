from enum import Enum
from typing import List
from uuid import UUID
from eventsourcing.domain import Aggregate, event

from filter.aggregate import Filter

class InvalidStateTransition(Exception):
    pass

class Vote(Aggregate):
    def __init__(self, creator: UUID) -> None:
        self.creator = creator
        self.voters: List[str] = []

        self.filter_id: UUID

        self.editable = True
        self.started = False
        self.stopped = False

    @event("UpdateTitle")
    def update_title(self, new_title: str):
        self.title = new_title

    @event("ChooseFilter")
    def choose_filter(self, filter_id: UUID):
        self.filter_id = filter_id

    @event("NoMoreEdits")
    def lock_settings(self):
        self.editable = False

    def start(self):
        if self.editable:
            raise InvalidStateTransition("Can't open a vote that's still editable")

        self._start()

    @event("StartVote")
    def _start(self):
        self.started = True

    def stop(self):
        if not self.started:
            raise InvalidStateTransition("Can't close a vote that's not open.")
        
        self._stop()

    @event("StopVote")
    def _stop(self):
        self.stopped = True

    @event("AddVoter")
    def add_voter(self, voter_id):
        self.voters.append(voter_id)

    @property
    def can_be_voted_on(self):
        return all((not self.editable, self.started, not self.stopped))
    
