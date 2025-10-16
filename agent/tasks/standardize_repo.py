
from __future__ import annotations
import datetime as dt
from agent.utils import log
from github.Repository import Repository

TEMPLATES = {
    "CODEOWNERS": "* @{owner}\n",
    "LICENSE": None,  # processed separately (MIT)
    ".github/PULL_REQUEST_TEMPLATE.md": """## TL;DR
<!-- One sentence value prop -->

## What changed
- Bullet 1
- Bullet 2

## Validation
- [ ] CI green
- [ ] Manual sanity check
""",
    ".github/ISSUE_TEMPLATE/bug_report.yml": """name: Bug report
description: File a bug/issue
labels: [\"type:bug\"]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Tell us what you expected vs what you observed.
      placeholder: It broke when I...
      render: markdown
    validations:
      required: true
""",
    ".github/ISSUE_TEMPLATE/feature_request.yml": """name: Feature request
description: Propose a feature
labels: [\"type:feature\"]
body:
  - type: textarea
    id: value-prop
    attributes:
      label: Value proposition
      description: Who benefits and how?
      placeholder: Users can...
      render: markdown
    validations:
      required: true
""",
    ".github/config.yml": """blank_issues_enabled: false
contact_links:
  - name: Questions
    url: https://github.com/${owner}/${repo}/discussions
    about: Ask and answer questions here.
""",
    ".github/dependabot.yml": """version: 2
updates:
  - package-ecosystem: \"pip\"
    directory: \"/\"
    schedule:
      interval: \"weekly\"
  - package-ecosystem: \"github-actions\"
    directory: \"/\"
    schedule:
      interval: \"weekly\"
""",
}

def _ensure_branch(repo: Repository, name: str, base: str) -> None:
    refs = [ref.ref for ref in repo.get_git_refs()]
    if f"refs/heads/{name}" in refs:
        return
    sha = repo.get_branch(base).commit.sha
    repo.create_git_ref(ref=f"refs/heads/{name}", sha=sha)

def _create_or_update(repo: Repository, path: str, content: str, branch: str, dry: bool) -> None:
    try:
        existing = repo.get_contents(path, ref=branch)
        if existing.decoded_content.decode("utf-8") == content:
            return
        if dry:
            log(f"      ~ would update {path}")
            return
        repo.update_file(path, f"chore: refresh {path}", content, existing.sha, branch=branch)
        log(f"      ✓ updated {path}")
    except Exception:
        if dry:
            log(f"      + would create {path}")
            return
        repo.create_file(path, f"chore: add {path}", content, branch=branch)
        log(f"      ✓ created {path}")

def run(repo: Repository, gh, cfg, dry_run: bool) -> None:
    feature_branch = "chore/bootstrap-standards"
    base = repo.default_branch
    _ensure_branch(repo, feature_branch, base)

    owner = repo.owner.login
    year = str(dt.datetime.utcnow().year)

    # CODEOWNERS & standard files
    for path, raw in TEMPLATES.items():
        if path == "LICENSE":
            content = (
                "MIT License\n\n"
                f"Copyright (c) {year} {owner}\n\n"
                "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
                "of this software and associated documentation files (the \"Software\"), to deal\n"
                "in the Software without restriction, including without limitation the rights\n"
                "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
                "copies of the Software, and to permit persons to do so, subject to the\n"
                "following conditions:\n\n"
                "The above copyright notice and this permission notice shall be included in all\n"
                "copies or substantial portions of the Software.\n\n"
                "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
                "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
                "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
                "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
                "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
                "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
                "SOFTWARE.\n"
            )
        else:
            content = raw.replace("{owner}", owner).replace("{year}", year)
        _create_or_update(repo, path, content, feature_branch, dry_run)

    # open PR if diff exists
    prs = list(repo.get_pulls(state="open", head=f"{repo.owner.login}:{feature_branch}"))
    if prs:
        log(f"      PR already open: {prs[0].html_url}")
        return
    try:
        compare = repo.compare(base, feature_branch)
        if compare.total_commits == 0 and len(compare.files) == 0:
            log("      Nothing to PR.")
            return
    except Exception:
        pass

    title = "chore: bootstrap repo standards (.github, license)"
    body = "Automated PR from Repo Agent to standardize core scaffolding."
    if dry_run:
        log("      ~ would open PR for bootstrap branch")
        return
    pr = repo.create_pull(title=title, body=body, base=base, head=feature_branch, maintainer_can_modify=True)
    log(f"      ✓ opened PR: {pr.html_url}")
