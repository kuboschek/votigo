import unittest
from datetime import datetime
from uuid import UUID

from filter.aggregate import Filter, FilterIndex
from filter.data_models import Condition


class TestFilterIndexAggregate(unittest.TestCase):
    def setUp(self):
        self.filter_index = FilterIndex()

    def test_update_filter(self):
        filter_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        filter_title = "Test Filter"

        self.filter_index.update_filter(filter_id, filter_title)
        self.assertEqual(self.filter_index.titles_by_id[filter_id], filter_title)

    def test_remove_filter(self):
        filter_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        filter_title = "Test Filter"
        self.filter_index._filter_titles_by_id[filter_id] = filter_title

        self.filter_index.remove_filter(filter_id)
        self.assertNotIn(filter_id, self.filter_index._filter_titles_by_id)

    def test_titles(self):
        filter_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        filter_title = "Test Filter"
        self.filter_index._filter_titles_by_id[filter_id] = filter_title

        titles = self.filter_index.titles_by_id

        self.assertEqual(titles, {filter_id: filter_title})


class TestFilterAggregate(unittest.TestCase):
    def setUp(self):
        self.creator_id = "test_creator_id"
        self.filter = Filter(
            self.creator_id, Condition(tree={"type": "AND", "parts": []})
        )

    def test_change_condition(self):
        condition = Condition(tree={"type": "OR", "parts": []})
        self.filter.change_condition(condition)
        self.assertEqual(self.filter.condition, condition)

    def test_change_title(self):
        title = "Test Filter"
        self.filter.change_title(title)
        self.assertEqual(self.filter.title, title)

    def test_evaluate(self):
        condition = Condition(tree={"type": "AND", "parts": []})
        self.filter.condition = condition

        self.assertTrue(self.filter.evaluate({}))
