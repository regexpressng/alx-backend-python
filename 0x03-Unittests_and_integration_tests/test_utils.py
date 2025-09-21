#!/usr/bin/env python3

from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) :
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
        Test get_json function with mocked requests.get."""
        mock_response = Mock()
        
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
        
class TestMemoize(unittest.TestCase) :

    def test_memoize(self):
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
                
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # Call twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Check results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was only called once
            mock_method.assert_called_once()
            
                