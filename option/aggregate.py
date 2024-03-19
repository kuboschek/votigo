from uuid import UUID
from eventsourcing.domain import Aggregate, event


class Option(Aggregate):
    def __init__(self, creator: UUID) -> None:
        self.creator = creator
        
        self.count = 0
        self.ordering = 0

    @event("UpdateTitle")
    def set_title(self, new_title: str):
        self.title = new_title

    @event("CountVote")
    def count_vote(self):
        self.count += 1

    @event("UpdateOrdering")
    def update_ordering(self, new_ordering):
        self.ordering = new_ordering