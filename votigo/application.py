from uuid import UUID
from eventsourcing.application import Application

from option.aggregate import Option
from vote.aggregate import Vote
from votigo.data_models import ReadFullVote, UpdateOption



class Votigo(Application):
    def create_vote(self, creator_id: str):
        vote = Vote(creator_id)
        self.save(vote)

        return vote
    
    def add_option(self, vote_id: UUID, values: UpdateOption):
        vote: Vote = self.repository.get(vote_id)
        if not vote.editable:
            raise ValueError("Can't add option to a vote that's already started")

        option = Option()
        option.set_title(values.title)
        option.update_ordering(values.ordering)

        vote.add_option(option.id)
        self.save(vote, option)

        return option
    
    def update_option(self, option_id: UUID, values: UpdateOption):
        option: Option = self.repository.get(option_id)
        if not option.editable:
            raise ValueError("Can't update option once it's read only")

        if values.title != option.title:
            option.set_title(values.title)

        if values.ordering != option.ordering:
            option.update_ordering(values.ordering)

        self.save(option)

    def remove_option(self, vote_id: UUID, option_id: UUID):
        option: Option = self.repository.get(option_id)
        vote: Vote = self.repository.get(vote_id)

        if not option.editable:
            raise ValueError("Can't remove an option that's read only")

        if option.count > 0:
            raise ValueError("Can't remove option that has votes")

        vote.remove_option(option_id)
        self.save(vote)

    def get_option(self, option_id: UUID) -> Option:
        return self.repository.get(option_id)

    def vote(self, vote_id: UUID, user_id: str, option_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        option: Option = self.repository.get(option_id)

        if not vote.can_be_voted_on:
            raise ValueError("Can't vote on this vote")
        
        if user_id in vote.voter_ids:
            raise ValueError("User already voted")
        
        if option_id not in vote.option_ids:
            raise ValueError("Option not in vote")
        
        vote.add_voter(user_id)
        option.count_vote()

        self.save(vote, option)

    def get_vote(self, vote_id: UUID) -> Vote:
        return self.repository.get(vote_id)
    
    def lock_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        vote.lock_settings()
        self.save(vote)

    def start_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        options: list[Option] = [self.repository.get(option_id) for option_id in vote.option_ids]

        for option in options:
            if option.count > 0:
                raise ValueError("Can't start vote with options that already have votes")
            option.lock_editing()
            
        vote.start()
        self.save(*options, vote)
    
    def stop_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        vote.stop()
        self.save(vote)