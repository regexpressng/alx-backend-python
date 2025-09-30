#!/usr/bin/env python3
"""
Unittest suite for utils module.

This file contains tests for:
- access_nested_map
- get_json
- memoize
"""

from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the access_nested_map function from utils.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected value
        when given a valid map and path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
        

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Tests for the get_json function from utils.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test get_json returns expected payload when requests.get is mocked.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        # Ensure requests.get was called with the right URL
        mock_get.assert_called_once_with(test_url)

        # Ensure result matches mocked payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Tests for the memoize decorator from utils.
    """

    def test_memoize(self):
        """
        Test that memoize caches the result of a method
        so the wrapped function is only called once.
        """

        class TestClass:
            """
            Example class with a simple method and a memoized property.
            """

            def a_method(self):
                """Return a fixed integer value."""
                return 42

            @memoize
            def a_property(self):
                """
                Memoized method that calls a_method.
                First call executes a_method,
                subsequent calls return cached value.
                """
                return self.a_method()

        # Patch a_method to track number of calls
        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            obj = TestClass()

            # Call memoized method twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Verify results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Verify a_method was only executed once
            mock_method.assert_called_once()
