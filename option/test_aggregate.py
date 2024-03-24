
import unittest
import uuid

from option.aggregate import InvalidEdit, Option


class TestOptionAggregate(unittest.TestCase):
    def setUp(self):
        self.creator_id = uuid.uuid4()
        self.option = Option(self.creator_id)

    def test_set_title_happy(self):
        new_title = "New Option Title"
        self.option.set_title(new_title)
        self.assertEqual(self.option.title, new_title)

    def test_set_ordering_happy(self):
        new_ordering = 5
        self.option.set_ordering(new_ordering)
        self.assertEqual(self.option.ordering, new_ordering)

    def test_update_title_unhappy(self):
        self.option.lock_editing()
        with self.assertRaises(InvalidEdit):
            self.option.set_title("New Title")

    def test_update_ordering_unhappy(self):
        self.option.lock_editing()
        with self.assertRaises(InvalidEdit):
            self.option.set_ordering(5)

    def test_count_vote_unhappy(self):
        with self.assertRaises(InvalidEdit):
            self.option.count_vote()

    def test_count_vote_happy(self):
        self.option.lock_editing()
        self.option.count_vote()
        self.assertEqual(self.option.count, 1)

    def test_count_multiple_votes_happy(self):
        self.option.lock_editing()
        self.option.count_vote()
        self.option.count_vote()
        self.assertEqual(self.option.count, 2)

    def test_lock_editing_happy(self):
        self.assertTrue(self.option.editable)
        self.option.lock_editing()
        self.assertFalse(self.option.editable)