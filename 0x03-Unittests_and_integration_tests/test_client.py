#!/usr/bin/env python3
"""
Unittest suite for client.GithubOrgClient module.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
import client
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

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
            public repos test
        """
        mock_get_json.return_value = "https://api.github.com/orgs/google/repos"

        with patch.object(GithubOrgClient,
                          "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = "https://api.github.com/orgs/google/repos"


    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with different license keys"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)



@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up patchers and mock requests.get for all tests in the class"""

        # Patch 'requests.get' used internally by get_json
        cls.get_patcher = patch('utils.requests.get')

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

        # Define a side_effect function to return correct payload depending on URL
        @parameterized.expand([
        ("all_repos", None, expected_repos),
        ("apache2_repos", "apache-2.0", apache2_repos)
    ])
        def get_json_side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url.endswith(cls.org_payload["repos_url"].split('/')[-1]):
                # URL matches repos_url
                mock_response.json.return_value = cls.repos_payload
            elif url.endswith(cls.org_payload["url"].split('/')[-1]):
                # URL matches org URL
                mock_response.json.return_value = cls.org_payload
            else:
                # Default empty
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos integration using mocked HTTP requests"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
