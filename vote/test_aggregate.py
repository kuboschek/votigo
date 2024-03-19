import unittest
from uuid import UUID
from eventsourcing.domain import Aggregate
from vote.aggregate import Vote, InvalidStateTransition
import uuid

class TestVoteAggregate(unittest.TestCase):
    def setUp(self):
        self.creator_id = uuid.uuid4()
        self.vote = Vote(self.creator_id)

    def test_update_title(self):
        new_title = "New Vote Title"
        self.vote.update_title(new_title)
        self.assertEqual(self.vote.title, new_title)

    def test_choose_filter(self):
        filter_id = uuid.uuid4()
        self.vote.choose_filter(filter_id)
        self.assertEqual(self.vote.filter_id, filter_id)

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
        self.assertIn(voter_id, self.vote.voters)

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


if __name__ == "__main__":
    unittest.main()
