
from __future__ import annotations
from github import Github
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser
from typing import Iterable

class GH:
    def __init__(self, token: str | None):
        if not token:
            raise SystemExit("No GITHUB_TOKEN found in env. Set it or provide GH_TOKEN.")
        self.g = Github(login_or_token=token, per_page=100)

    def me(self) -> AuthenticatedUser:
        return self.g.get_user()

    def user_repos(self, owner: str):
        u = self.g.get_user(owner) if self.me().login != owner else self.me()
        return u.get_repos(visibility="all")
