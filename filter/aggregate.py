from uuid import UUID
from eventsourcing.domain import Aggregate, event


class Filter(Aggregate):
    def __init__(self, creator: UUID) -> None:
        self.creator = creator
        self.condition_tree: dict = {}

    @event("ChangeCondition")
    def change_condition(self, new_condition: str):
        # ToDo: Parse filter condition string
        self.condition_tree = {}

    def evaluate(self, dict_to_check) -> bool:
        # ToDo: Actually evaluate filter on object
        return True