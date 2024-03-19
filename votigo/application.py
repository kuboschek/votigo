from uuid import UUID
from eventsourcing.application import Application

from vote.aggregate import Vote



class Votigo(Application):
    def create_vote(self, creator):
        vote = Vote(creator)
        self.save(vote)

        return vote.id
    
    def get_vote(self, vote_id: UUID) -> Vote:
        vote: Vote = self.repository.get(vote_id)
        return vote