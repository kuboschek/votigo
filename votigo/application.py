from uuid import UUID

from eventsourcing.application import AggregateNotFound, Application

from option.aggregate import Option
from vote.aggregate import Vote
from votigo.data_models import ReadFullVote, UpdateOption, UpdateVote


class Votigo(Application):
    def create_vote(self, creator_id: str):
        vote = Vote(creator_id)
        self.save(vote)

        return vote
    
    def get_vote(self, vote_id: UUID) -> Vote:
        return self.repository.get(vote_id)
    
    def update_vote(self, vote_id: UUID, values: UpdateVote):
        vote: Vote = self.repository.get(vote_id)

        if values.title != vote.title:
            vote.set_title(values.title)

        if values.prompt != vote.prompt:
            vote.set_prompt(values.prompt)
        
        self.save(vote)

    
    def add_option(self, vote_id: UUID, values: UpdateOption) -> Option:
        vote: Vote = self.repository.get(vote_id)
        if not vote.editable:
            raise ValueError("Can't add option to a vote that's already started")

        option = Option()
        option.set_title(values.title)
        option.set_ordering(values.ordering)

        vote.add_option(option.id)
        self.save(vote, option)

        return option
    
    def update_option(self, option_id: UUID, values: UpdateOption):
        option: Option = self.repository.get(option_id)
        if not option.editable:
            raise ValueError("Can't update option once it's read only")

        if values.title and values.title != option.title:
            option.set_title(values.title)

        if values.ordering and values.ordering != option.ordering:
            option.set_ordering(values.ordering)

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
            raise ValueError("This vote is not ready to vote on.")
        
        if user_id in vote.voter_ids:
            raise ValueError("You already voted")
        
        if option_id not in vote.option_ids:
            raise ValueError("The selected option is not in this vote")
        
        vote.add_voter(user_id)
        option.count_vote()

        self.save(vote, option)
    
    def lock_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        vote.lock_settings()
        options: list[Option] = [self.repository.get(option_id) for option_id in vote.option_ids]

        for option in options:
            if option.count > 0:
                raise ValueError("Can't start vote with options that already have votes")
            option.lock_editing()

        self.save(*options, vote)

    def start_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
            
        vote.start()
        self.save(vote)
    
    def stop_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        vote.stop()
        self.save(vote)