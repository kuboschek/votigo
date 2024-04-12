import unittest
import uuid
from uuid import UUID

from eventsourcing.domain import Aggregate

from vote.aggregate import InvalidStateTransition, Vote, VoteIndex, VoteStatus


class TestVoteAggregate(unittest.TestCase):
    def setUp(self):
        self.creator_id = uuid.uuid4()
        self.vote = Vote(self.creator_id)

    def test_update_title(self):
        new_title = "New Vote Title"
        self.vote.set_title(new_title)
        self.assertEqual(self.vote.title, new_title)

    def test_update_prompt(self):
        new_prompt = "New Vote Prompt"
        self.vote.set_prompt(new_prompt)
        self.assertEqual(self.vote.prompt, new_prompt)

    def test_choose_filter(self):
        filter_id = uuid.uuid4()
        filter_version = 12
        self.vote.choose_filter(filter_id, filter_version)
        self.assertEqual(self.vote.filter_id, filter_id)
        self.assertEqual(self.vote.filter_version, filter_version)

    def test_lock_settings(self):
        # Votes are editable
        self.assertTrue(self.vote.editable)

        self.vote.lock_settings()

        # But not after locking the settings
        self.assertFalse(self.vote.editable)

    def test_open_vote(self):
        # Can't open a vote that's still editable
        with self.assertRaises(InvalidStateTransition):
            self.vote.start()

        self.assertFalse(self.vote.started)

    def test_open_vote_happy(self):
        self.vote.lock_settings()
        self.vote.start()
        self.assertTrue(self.vote.started)

    def test_close_vote(self):
        # Can't close a vote that's not open
        with self.assertRaises(InvalidStateTransition):
            self.vote.stop()

        self.assertFalse(self.vote.started)
        self.assertFalse(self.vote.stopped)

    def test_add_voter(self):
        voter_id = uuid.uuid4()
        self.vote.add_voter(voter_id)
        self.assertIn(voter_id, self.vote.voter_ids)

    def test_invalid_state_transition(self):
        with self.assertRaises(InvalidStateTransition):
            self.vote.stop()

    def test_can_be_voted_on(self):
        self.assertFalse(self.vote.can_be_voted_on)
        self.vote.lock_settings()
        self.assertFalse(self.vote.can_be_voted_on)
        self.vote.start()
        self.assertTrue(self.vote.can_be_voted_on)
        self.vote.stop()
        self.assertFalse(self.vote.can_be_voted_on)


class TestVoteIndexAggregate(unittest.TestCase):
    def setUp(self):
        self.vote_index = VoteIndex()

    def test_update_title_happy(self):
        vote_id = uuid.uuid4()
        vote_title = "Vote Title"
        self.vote_index.update_vote_title(id=vote_id, title=vote_title)
        self.assertEqual(self.vote_index.titles_by_id[vote_id], vote_title)

    def test_update_status_happy(self):
        vote_id = uuid.uuid4()
        self.vote_index.update_vote_status(id=vote_id, status=VoteStatus.OPEN)
        self.assertIn(vote_id, self.vote_index.by_status[VoteStatus.OPEN])

    def test_update_status_happy_2(self):
        vote_id = uuid.uuid4()
        self.vote_index.update_vote_status(id=vote_id, status=VoteStatus.OPEN)
        self.vote_index.update_vote_status(id=vote_id, status=VoteStatus.CLOSED)

        self.assertIn(vote_id, self.vote_index.by_status[VoteStatus.CLOSED])


if __name__ == "__main__":
    unittest.main()
