
# Codespace Repo Agent

A plug-and-play GitHub Codespaces agent that bulk-manages your repositories.

## Quick start
1. Create a new repo named `codespace-repo-agent` and upload this folder.
2. Open in **Codespaces**.
3. Provide auth: set Codespaces secret `GITHUB_TOKEN` (preferred) *or* copy `.env.example` to `.env`.
4. Edit `repos.yaml` (defaults target all your personal, non-archived repos).
5. Run:
   ```bash
   make doctor   # verify token & targets
   make dry      # preview changes
   make run      # apply changes
   ```

## Out-of-the-box tasks
- **standardize_repo**: creates a PR adding core scaffolding (.github templates, CODEOWNERS, Dependabot, MIT license).
- **sync_labels**: creates/updates a standard label set.

## Add tasks
Drop a module in `agent/tasks/` that exposes `run(repo, gh, cfg, dry_run)` and list it in `repos.yaml` under `tasks:`.
