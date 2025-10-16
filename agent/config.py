
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import os, yaml

@dataclass
class Pattern:
    name: str
    archived: Optional[bool] = None

@dataclass
class Config:
    owner: Optional[str]
    repos: List[str]
    include: List[Pattern]
    exclude: List[Pattern]
    tasks: List[str]

def load_config() -> Config:
    path = os.path.join(os.getcwd(), "repos.yaml")
    if not os.path.exists(path):
        raise SystemExit("Missing repos.yaml in project root.")
    data = yaml.safe_load(open(path, "r"))
    def _patterns(key):
        items = data.get(key, []) or []
        return [Pattern(**i) for i in items]
    return Config(
        owner=data.get("owner"),
        repos=data.get("repos", []) or [],
        include=_patterns("include"),
        exclude=_patterns("exclude"),
        tasks=data.get("tasks", []) or [],
    )
