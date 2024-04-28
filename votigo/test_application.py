import unittest
import uuid

from filter.data_models import Condition
from votigo.application import Votigo
from votigo.data_models import UpdateFilter, UpdateOption, UpdateVote, UpdateVoteFilter


class TestVotigoApplication(unittest.TestCase):
    def setUp(self):
        self.app = Votigo()
        self.user1 = str(uuid.uuid4())
        self.user2 = str(uuid.uuid4())
        self.user3 = str(uuid.uuid4())

    def test_create_vote(self):
        vote = self.app.create_vote(self.user1)
        self.assertEqual(vote.creator_id, self.user1)

    def test_create_filter(self):
        filter = self.app.create_filter("creator")
        self.assertEqual(filter.creator_id, "creator")

    def test_get_vote(self):
        vote = self.app.create_vote(self.user1)
        self.assertEqual(self.app.get_vote(vote.id), vote)

    def test_get_option(self):
        vote = self.app.create_vote(self.user1)
        option = self.app.add_option(
            vote.id, UpdateOption(title="Option 1", ordering=1)
        )
        self.assertEqual(self.app.get_option(option.id), option)

    def test_start_vote(self):
        vote = self.app.create_vote(self.user1)
        self.app.lock_vote(vote.id)
        self.app.start_vote(vote.id)
        self.assertTrue(self.app.get_vote(vote.id).started)

    def test_filter_access(self):
        filter = self.app.create_filter("creator")
        self.app.update_filter(
            filter_id=filter._id,
            data=UpdateFilter(
                title="Test Filter",
                condition=Condition(
                    tree={
                        "type": "AND",
                        "parts": [
                            {
                                "type": "EQ",
                                "pointer": "/username",
                                "target_value": "valid-username",
                            }
                        ],
                    }
                ),
            ),
        )
        filter = self.app.get_filter(filter._id)

        vote = self.app.create_vote(self.user1)
        self.app.update_vote(
            vote.id,
            UpdateVote(
                title="Test Vote",
                prompt="Test Prompt",
                filter=UpdateVoteFilter(id=filter.id, version=filter.version),
            ),
        )
        option = self.app.add_option(
            vote.id, UpdateOption(title="Option 1", ordering=1)
        )
        self.app.lock_vote(vote.id)
        self.app.start_vote(vote.id)

        # Can't vote with invalid username
        with self.assertRaises(ValueError):
            self.app.vote(
                vote.id, self.user2, option.id, {"username": "invalid-username"}
            )

        # Can vote with valid username
        self.app.vote(vote.id, self.user2, option.id, {"username": "valid-username"})

    def test_full_vote_cycle(self):
        # Set up
        filter = self.app.create_filter("creator")

        # The empty AND allows any voter
        filter.change_condition(
            Condition(
                tree={
                    "type": "AND",
                    "parts": [],
                }
            )
        )
        self.app.save(filter)

        vote = self.app.create_vote(self.user1)
        self.app.update_vote(
            vote.id,
            UpdateVote(
                title="Test Vote",
                prompt="Test Prompt",
                filter=UpdateVoteFilter(id=filter.id, version=filter.version),
            ),
        )

        option1 = self.app.add_option(
            vote.id, UpdateOption(title="Option 1", ordering=1)
        )
        option2 = self.app.add_option(
            vote.id, UpdateOption(title="Option 2", ordering=2)
        )
        option3 = self.app.add_option(
            vote.id, UpdateOption(title="Option 3", ordering=3)
        )

        vote = self.app.get_vote(vote.id)

        # Can't vote on a newly created vote
        with self.assertRaises(ValueError):
            self.app.vote(vote.id, self.user1, option1.id)

        # Lock the vote
        self.app.lock_vote(vote.id)

        option1 = self.app.get_option(option1.id)
        option2 = self.app.get_option(option2.id)
        option3 = self.app.get_option(option3.id)

        # Check that the vote and its options are locked
        self.assertFalse(self.app.get_vote(vote.id).editable)
        self.assertFalse(self.app.get_vote(vote.id).started)
        self.assertFalse(self.app.get_vote(vote.id).stopped)
        self.assertFalse(option1.editable)
        self.assertFalse(option2.editable)
        self.assertFalse(option3.editable)

        # Still can't vote, as the vote hasn't been opened yet
        with self.assertRaises(ValueError):
            self.app.vote(vote.id, self.user1, option1.id)

        # Start the vote
        self.app.start_vote(vote.id)

        self.assertTrue(self.app.get_vote(vote.id).started)
        self.assertFalse(self.app.get_vote(vote.id).stopped)

        # Vote
        self.app.vote(vote.id, self.user1, option1.id)
        self.app.vote(vote.id, self.user2, option2.id)

        # Can't vote twice on the same vote
        with self.assertRaises(ValueError):
            self.app.vote(vote.id, self.user1, option2.id)

        # Stop the vote
        self.app.stop_vote(vote.id)

        # Still can't vote twice
        with self.assertRaises(ValueError):
            self.app.vote(vote.id, self.user2, option2.id)

        # Can't vote after voting was stopped
        with self.assertRaises(ValueError):
            self.app.vote(vote.id, self.user3, option3.id)

        self.assertTrue(self.app.get_vote(vote.id).stopped)

    def test_add_option(self):
        vote = self.app.create_vote(self.user1)
        option = self.app.add_option(
            vote.id, UpdateOption(title="New Option", ordering=1)
        )
        self.assertIn(option.id, self.app.get_vote(vote.id).option_ids)

    def test_filter_in_index(self):
        filter = self.app.create_filter("creator")
        filter_title = "Test Filter"

        self.app.update_filter(
            filter_id=filter._id,
            data=UpdateFilter(
                title=filter_title, condition={"tree": {"type": "AND", "parts": []}}
            ),
        )
        self.assertEqual(self.app.get_all_filters()[filter._id], filter_title)

    def test_vote_in_index(self):
        vote = self.app.create_vote(self.user1)
        self.assertIn(vote.id, self.app.get_all_votes())
