
from __future__ import annotations

import os
import time
import typer
from dotenv import load_dotenv
from agent.config import load_config
from agent.github_client import GH
from agent.utils import log, banner, resolve_repos

app = typer.Typer(add_completion=False, help="Codespace Repo Agent CLI")

@app.command()
def doctor() -> None:
    """Sanity checks: token, owner, and repo discovery."""
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("No GITHUB_TOKEN found in env.")
    gh = GH(token=token)
    me = gh.me().login
    cfg = load_config()
    owner = cfg.owner or os.environ.get("GITHUB_OWNER") or me
    log(f"👤 Authenticated as: {me}")
    log(f"🏷  Owner in scope: {owner}")
    repos = resolve_repos(gh, cfg, owner)
    log(f"📦 Target repos: {len(repos)}")
    for r in repos[:15]:
        log(f" - {r.full_name}")
    if len(repos) > 15:
        log(f" ...and {len(repos)-15} more")
    log("✅ Doctor looks good")

@app.command()
def run(dry: bool = typer.Option(False, "--dry", help="Preview changes only")) -> None:
    """Run tasks across targeted repos."""
    t0 = time.time()
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("No GITHUB_TOKEN found in env.")
    gh = GH(token=token)
    me = gh.me().login
    cfg = load_config()
    owner = cfg.owner or os.environ.get("GITHUB_OWNER") or me
    repos = resolve_repos(gh, cfg, owner)

    banner(f"Repo Agent: {len(repos)} repos | tasks={cfg.tasks} | dry={dry}")
    for repo in repos:
        log(f"🔧 {repo.full_name}")
        for task_name in cfg.tasks:
            mod = __import__(f"agent.tasks.{task_name}", fromlist=["run"])
            log(f"   • Task: {task_name}")
            mod.run(repo=repo, gh=gh, cfg=cfg, dry_run=dry)
    log(f"🏁 Done in {time.time()-t0:.1f}s")

if __name__ == "__main__":
    app()
