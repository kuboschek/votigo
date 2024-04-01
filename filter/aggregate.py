from dataclasses import dataclass, field
import datetime
from uuid import UUID
from eventsourcing.domain import Aggregate, event

from filter.data_models import BasicDict, Condition


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
        # ToDo: Actually evaluate filter on object
        return self.condition.test(dict_to_check)