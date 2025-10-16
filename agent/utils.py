
from __future__ import annotations
import re
from typing import List
from agent.config import Config, Pattern
from agent.github_client import GH
from github.Repository import Repository

def log(msg: str) -> None:
    print(msg, flush=True)

def banner(msg: str) -> None:
    log("="*80)
    log(msg)
    log("="*80)

def _match(name: str, pat: Pattern) -> bool:
    regex = '^' + pat.name.replace('*', '.*') + '$'
    return re.match(regex, name) is not None

def resolve_repos(gh: GH, cfg: Config, owner: str) -> List[Repository]:
    if cfg.repos:
        return [gh.g.get_repo(f"{owner}/{r}") for r in cfg.repos]

    result = []
    for r in gh.user_repos(owner):
        # include filters
        if cfg.include:
            if not any(_match(r.name, p) and _archived_ok(r, p) for p in cfg.include):
                continue
        # exclude filters
        if cfg.exclude:
            if any(_match(r.name, p) and _archived_ok(r, p) for p in cfg.exclude):
                continue
        result.append(r)
    return result

def _archived_ok(repo: Repository, pat: Pattern) -> bool:
    if pat.archived is None:
        return True
    return repo.archived == pat.archived
