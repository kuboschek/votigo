import datetime
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from typing import List, Optional
from uuid import UUID

from eventsourcing.domain import Aggregate, event


class InvalidStateTransition(Exception):
    pass


class VoteStatus(StrEnum):
    EDITABLE = "editable"
    OPEN = "open"
    CLOSED = "closed"
    ARCHIVED = "archived"


@dataclass
class VoteIndex(Aggregate):
    # These three are auto-created by the Aggregate class.
    # They are included here so they are serialized in FastAPI.

    _id: UUID = field(init=False)
    _created_on: datetime.datetime = field(init=False)
    _modified_on: datetime.datetime = field(init=False)

    _vote_titles_by_id: dict[UUID, str] = field(default_factory=dict, init=False)
    _vote_by_status: dict[VoteStatus, list[UUID]] = field(
        default_factory=lambda: defaultdict(list), init=False
    )

    @staticmethod
    def create_id() -> UUID:
        return uuid.uuid5(uuid.NAMESPACE_DNS, "/vote")

    @event("UpdateVoteTitle")
    def update_vote_title(
        self,
        id: UUID,
        title: str = "",
    ):
        self._vote_titles_by_id[id] = title

    @event("UpdateVoteStatus")
    def update_vote_status(self, id: UUID, status: VoteStatus):
        self._vote_by_status[status].append(id)

        for vote_status in VoteStatus:
            if vote_status != status:
                try:
                    self._vote_by_status[vote_status].remove(id)
                except ValueError:
                    pass  # The vote wasn't in that status, we don't care

    @property
    def titles_by_id(self):
        return self._vote_titles_by_id

    @property
    def by_status(self):
        return self._vote_by_status


@dataclass
class Vote(Aggregate):
    # These three are auto-created by the Aggregate class.
    # They are included here so they are serialized in FastAPI.

    _id: UUID = field(init=False)
    _created_on: datetime.datetime = field(init=False)
    _modified_on: datetime.datetime = field(init=False)

    creator_id: str
    voter_ids: List[str] = field(default_factory=list, init=False)
    option_ids: List[UUID] = field(default_factory=list, init=False)
    filter_id: Optional[UUID] = None
    filter_version: int = 1
    editable: bool = True
    started: bool = False
    stopped: bool = False
    title: str = ""
    prompt: str = ""

    @event("SetTitle")
    def set_title(self, new_title: str):
        self.title = new_title

    @event("SetPrompt")
    def set_prompt(self, new_prompt: str):
        self.prompt = new_prompt

    @event("ChooseFilter")
    def choose_filter(self, filter_id: UUID, filter_version: int):
        self.filter_id = filter_id
        self.filter_version = filter_version

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
    def add_voter(self, voter_id: str):
        self.voter_ids.append(voter_id)

    @event("AddOption")
    def add_option(self, option_id: UUID):
        self.option_ids.append(option_id)

    @event("RemoveOption")
    def remove_option(self, option_id: UUID):
        self.option_ids.remove(option_id)

    @property
    def can_be_voted_on(self):
        return all((not self.editable, self.started, not self.stopped))
