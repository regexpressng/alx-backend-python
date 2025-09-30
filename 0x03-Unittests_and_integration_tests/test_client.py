#!/usr/bin/env python3
"""
Unittest suite for client.GithubOrgClient module.
"""

from client import GithubOrgClient
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

class TestGithubOrgClient(unittest.TestCase):
    
   
    @parameterized.expand(["google", "abc"])
    @patch("client.get_json")
    def test_org(self, org, mock_get_json):
        mock_get_json.return_value = f"https://api.github.com/orgs/{org}"


        check = GithubOrgClient(org)
        result = check.org

        mock_get_json.assert_called_once_with(check.org)
        self.assertEqual(result, f"https://api.github.com/orgs/{org}"
)
        

