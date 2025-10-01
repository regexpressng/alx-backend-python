#!/usr/bin/env python3
"""
Unittest suite for client.GithubOrgClient module.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient.

    This class contains unit tests that verify the correct behavior of the
    GithubOrgClient by mocking API calls and checking the resulting output.
    """

    @parameterized.expand([("google", {"id": 7697149}),
                           ("abc", {"message": "Not Found"})])
    @patch("client.get_json")
    def test_org(self, org, payload, mock_get_json):
        """Implements the org method"""
        mock_response = Mock()
        mock_response.return_value = payload
        mock_get_json.return_value = payload

        client = GithubOrgClient(org)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}")
        self.assertEqual(result, payload)

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"})])
    def test_public_repos_url(self, org, test_payload):
        """
        Tests  that it returns public repos
        """
        with patch.object(GithubOrgClient,
                          "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient(org)
            self.assertEqual(client._public_repos_url,
                             test_payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        testing public repos
        """
        mock_get_json.return_value = "https://api.github.com/orgs/google/repos"

        with patch.object(GithubOrgClient,
                          "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = "https://api.github.com/orgs/google/repos"

        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with different license keys"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
