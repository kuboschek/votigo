import datetime
import uuid
from dataclasses import dataclass, field
from uuid import UUID

from eventsourcing.domain import Aggregate, event

from filter.data_models import BasicDict, Condition


@dataclass
class FilterIndex(Aggregate):
    # These three are auto-created by the Aggregate class.
    # They are included here so they are serialized in FastAPI.

    _id: UUID = field(init=False)
    _created_on: datetime.datetime = field(init=False)
    _modified_on: datetime.datetime = field(init=False)

    # Singleton, so no need for default_factory
    _filter_titles_by_id: dict[UUID, str] = field(default_factory=dict, init=False)

    @staticmethod
    def create_id() -> UUID:
        return uuid.uuid5(uuid.NAMESPACE_DNS, "/filter")

    @event("UpdateFilter")
    def update_filter(self, id: UUID, title: str = ""):
        self._filter_titles_by_id[id] = title

    @event("RemoveFilter")
    def remove_filter(self, id: UUID):
        del self._filter_titles_by_id[id]

    @property
    def titles_by_id(self):
        return self._filter_titles_by_id


@dataclass
class Filter(Aggregate):
    # These three are auto-created by the Aggregate class.
    # They are included here so they are serialized in FastAPI.

    _id: UUID = field(init=False)
    _created_on: datetime.datetime = field(init=False)
    _modified_on: datetime.datetime = field(init=False)

    creator_id: str
    condition: Condition

    title: str = ""

    @event("ChangeCondition")
    def change_condition(self, new_condition: Condition):
        # ToDo: Parse filter condition string
        self.condition = new_condition

    @event("ChangeTitle")
    def change_title(self, new_title: str):
        self.title = new_title

    def evaluate(self, dict_to_check: BasicDict) -> bool:
        return self.condition.test(dict_to_check)
