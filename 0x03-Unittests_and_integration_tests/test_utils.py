#!/usr/bin/env python3

from parameterized import parameterized
import unittest
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({}, ("a"), 1),
        ({"a": 1}, ("a", "b"), 3)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    
    def test_access_nested_map_exception(self):
        with self.assertRaises(KeyError) :
            access_nested_map({}, "a")