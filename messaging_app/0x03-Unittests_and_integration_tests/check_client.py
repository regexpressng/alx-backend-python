#!/usr/bin/env python3
"""
just a test module
"""
from client import GithubOrgClient

client = GithubOrgClient("google")
result = client.org
print(client._public_repos_url)
