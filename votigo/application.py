from typing import Optional
from uuid import UUID

from eventsourcing.application import AggregateNotFound, Application
from eventsourcing.persistence import Transcoder

from filter.aggregate import Filter, FilterIndex
from filter.data_models import BasicDict
from filter.transcoding import ConditionTranscoding
from option.aggregate import Option
from vote.aggregate import Vote, VoteIndex, VoteStatus
from votigo.data_models import UpdateFilter, UpdateOption, UpdateVote


class Votigo(Application):
    def _get_filter_index(self) -> FilterIndex:
        try:
            return self.repository.get(FilterIndex.create_id())
        except AggregateNotFound:
            return FilterIndex()

    def _get_vote_index(self) -> VoteIndex:
        try:
            return self.repository.get(VoteIndex.create_id())
        except AggregateNotFound:
            return VoteIndex()

    def create_vote(self, creator_id: str):
        vote = Vote(creator_id)

        vote_index = self._get_vote_index()
        vote_index.update_vote_title(vote.id, vote.title)
        vote_index.update_vote_status(vote.id, VoteStatus.EDITABLE)

        self.save(vote, vote_index)

        return vote

    def get_vote(self, vote_id: UUID) -> Vote:
        return self.repository.get(vote_id)

    def update_vote(self, vote_id: UUID, values: UpdateVote):
        vote: Vote = self.repository.get(vote_id)

        if values.title != vote.title:
            vote.set_title(values.title)

        if values.prompt != vote.prompt:
            vote.set_prompt(values.prompt)

        if values.filter and (
            values.filter.id != vote.filter_id
            or values.filter.version != vote.filter_version
        ):
            vote.set_filter(values.filter.id, values.filter.version)

        self.save(vote)

    def lock_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        vote.lock_settings()
        options: list[Option] = [
            self.repository.get(option_id) for option_id in vote.option_ids
        ]

        for option in options:
            if option.count > 0:
                raise ValueError(
                    "Can't start vote with options that already have votes"
                )
            option.lock_editing()

        self.save(*options, vote)

    def start_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        vote_index = self._get_vote_index()

        vote.start()
        vote_index.update_vote_status(vote.id, VoteStatus.OPEN)

        self.save(vote)

    def stop_vote(self, vote_id: UUID):
        vote: Vote = self.repository.get(vote_id)
        vote_index = self._get_vote_index()

        vote.stop()
        vote_index.update_vote_status(vote.id, VoteStatus.CLOSED)

        self.save(vote)

    def vote(
        self,
        vote_id: UUID,
        user_id: str,
        option_id: UUID,
        user_details: BasicDict = dict(),
    ):
        """Count a vote for the authenticated user."""
        vote: Vote = self.repository.get(vote_id)
        option: Option = self.repository.get(option_id)

        if not vote.filter_id or not vote.filter_version:
            raise ValueError("This vote is in an invalid state.")

        filter: Filter = self.repository.get(
            vote.filter_id, version=vote.filter_version
        )

        if not vote.can_be_voted_on:
            raise ValueError("This vote is not ready to vote on.")

        if user_id in vote.voter_ids:
            raise ValueError("You already voted")

        if option_id not in vote.option_ids:
            raise ValueError("The selected option is not in this vote")

        if not filter.evaluate(user_details):
            raise ValueError("You are not allowed to vote on this vote")

        vote.add_voter(user_id)
        option.count_vote()

        self.save(vote, option)

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

    def create_filter(self, creator: str) -> Filter:
        filter = Filter(creator, {})
        self.save(filter)
        return filter

    def get_all_filters(self):
        return self._get_filter_index().titles_by_id

    def get_all_votes(self):
        return self._get_vote_index().titles_by_id

    def get_filter(self, filter_id: UUID, version: Optional[int] = None) -> Filter:
        return self.repository.get(filter_id, version=version)

    def update_filter(self, filter_id: UUID, data: UpdateFilter):
        filter: Filter = self.repository.get(filter_id)
        filter.change_condition(data.condition)
        filter.change_title(data.title)

        index: FilterIndex = self._get_filter_index()
        index.update_filter(filter._id, data.title)

        self.save(filter, index)

    def construct_transcoder(self) -> Transcoder:
        t = super().construct_transcoder()
        t.register(ConditionTranscoding())

        return t
