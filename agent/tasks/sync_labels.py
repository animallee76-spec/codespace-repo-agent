
from __future__ import annotations
import yaml
from agent.utils import log
from github.Repository import Repository

def run(repo: Repository, gh, cfg, dry_run: bool) -> None:
    data = yaml.safe_load(open("config/labels.yml", "r"))
    existing = {lbl.name: lbl for lbl in repo.get_labels()}

    for spec in data:
        name = spec["name"]
        color = spec.get("color", "ededed")
        desc = spec.get("description", "")

        if name in existing:
            lbl = existing[name]
            if (lbl.color.lower() != color.lower()) or ((lbl.description or "") != desc):
                if dry_run:
                    log(f"      ~ would update label {name}")
                else:
                    lbl.edit(name=name, color=color, description=desc)
                    log(f"      ✓ updated label {name}")
        else:
            if dry_run:
                log(f"      + would create label {name}")
            else:
                repo.create_label(name=name, color=color, description=desc)
                log(f"      ✓ created label {name}")
