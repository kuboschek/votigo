import unittest

from jsonpointer import JsonPointer, JsonPointerException

from filter.data_models import (
    AndCondition,
    BasicDict,
    Condition,
    EqCondition,
    OrCondition,
)


class TestConditionTree(unittest.TestCase):
    def test_json_pointer_int(self):
        r1 = JsonPointer("/a").get({"a": 1})
        self.assertEqual(r1, 1)

    def test_json_pointer_nested_dict(self):
        r2 = JsonPointer("/a/b").get({"a": {"b": 2}})
        self.assertEqual(r2, 2)

    def test_json_pointer_list(self):
        r3 = JsonPointer("/a/0").get({"a": [1, 2, 3]})
        self.assertEqual(r3, 1)

    def test_json_pointer_float(self):
        r4 = JsonPointer("/a/1").get({"a": [1, 2.4, 3]})
        self.assertEqual(r4, 2.4)

    def test_json_pointer_str_num(self):
        r5 = JsonPointer("/a/2").get({"a": [1, 2, "3"]})
        self.assertEqual(r5, "3")

    def test_json_pointer_bool(self):
        r6 = JsonPointer("/a/2/0").get({"a": [1, 2, [True, 4]]})
        self.assertEqual(r6, True)

    def test_json_pointer_not_found(self):
        with self.assertRaises(JsonPointerException):
            JsonPointer("/a").get({"b": 1})

    def test_eq_condition(self):
        user_attributes: BasicDict = {
            "a": 1
        }

        self.assertTrue(EqCondition(type="EQ", pointer="/a", target_value=1).test(user_attributes))
        self.assertFalse(EqCondition(type="EQ", pointer="/a", target_value=2).test(user_attributes))

    def test_and_condition(self):
        user_attributes: BasicDict = {
            "a": 1,
            "b": 2,
        }

        self.assertTrue(AndCondition(parts=[
            EqCondition(type="EQ", pointer="/a", target_value=1),
            EqCondition(type="EQ", pointer="/b", target_value=2),
        ]).test(user_attributes))

        self.assertFalse(AndCondition(parts=[
            EqCondition(type="EQ", pointer="/a", target_value=1),
            EqCondition(type="EQ", pointer="/b", target_value=3),
        ]).test(user_attributes))

    def test_and_condition_empty(self):
        user_attributes: BasicDict = {
            "a": 1,
            "b": 2,
        }

        self.assertTrue(AndCondition(parts=[]).test(user_attributes))

    def test_or_condition(self):
        user_attributes: BasicDict = {
            "a": 1,
            "b": 3,
        }

        self.assertTrue(OrCondition(parts=[
            EqCondition(type="EQ", pointer="/a", target_value=1),
            EqCondition(type="EQ", pointer="/b", target_value=2),
        ]).test(user_attributes))

        self.assertFalse(OrCondition(parts=[
            EqCondition(type="EQ", pointer="/a", target_value=2),
            EqCondition(type="EQ", pointer="/b", target_value=4),
        ]).test(user_attributes))

    def test_or_condition_empty(self):
        user_attributes: BasicDict = {
            "a": 1,
            "b": 2,
        }

        self.assertFalse(OrCondition(parts=[]).test(user_attributes))


    def test_complex_tree(self):
        user_attributes: BasicDict = {
            "a": 1,
            "b": 2,
            "c": 1,
            "d": 2,
        }

        complex_tree = Condition(
            tree=AndCondition(
                parts=[
                    AndCondition(
                        parts=[
                            EqCondition(type="EQ", pointer="/a", target_value=1),
                            EqCondition(type="EQ", pointer="/b", target_value=2),
                        ],
                    ),
                    OrCondition(
                        parts=[
                            EqCondition(type="EQ", pointer="/c", target_value=1),
                            EqCondition(type="EQ", pointer="/d", target_value=2),
                        ],
                    ),
                ],
            )
        )
        
        self.assertTrue(complex_tree.test(user_attributes))

    def test_eq_with_not_found_raises(self):
        with self.assertRaises(JsonPointerException):
            simple_condition = EqCondition(type="EQ", pointer="/a", target_value=1)
            self.assertFalse(simple_condition.test({}))

    def test_and_with_not_found_raises(self):
        with self.assertRaises(JsonPointerException):
            and_condition = AndCondition(parts=[
                EqCondition(type="EQ", pointer="/a", target_value=1),
                EqCondition(type="EQ", pointer="/b", target_value=2),
            ])
            self.assertFalse(and_condition.test({}))

    def test_or_with_not_found_raises(self):
        with self.assertRaises(JsonPointerException):
            or_condition = OrCondition(parts=[
                EqCondition(type="EQ", pointer="/a", target_value=1),
                EqCondition(type="EQ", pointer="/b", target_value=2),
            ])
            self.assertFalse(or_condition.test({}))

    def test_complex_tree_with_not_found(self):
        complex_tree = Condition(
            tree=AndCondition(
                parts=[
                    AndCondition(
                        parts=[
                            EqCondition(type="EQ", pointer="/a", target_value=1),
                            EqCondition(type="EQ", pointer="/b", target_value=2),
                        ],
                    ),
                    OrCondition(
                        parts=[
                            EqCondition(type="EQ", pointer="/c", target_value=1),
                            EqCondition(type="EQ", pointer="/d", target_value=2),
                        ],
                    ),
                ],
            )
        )

        self.assertFalse(complex_tree.test({}))