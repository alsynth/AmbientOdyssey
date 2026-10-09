> **9 October 2026:** This historical initial-upload guide is superseded. The repaired `main` branch stores Tan's Huge Trees `#main.zip` as a **regular 73.5 MB Git blob**, not Git LFS. For current setup use `README.md` and `docs/handoff/START_HERE.md`.

# Upload this repository to GitHub

## Prerequisites

- A GitHub account and a new **private** repository named `Ambient-Odyssey` (recommended initially), created **empty** (no GitHub-generated README or .gitignore).
- Git and Git LFS installed on the machine doing the initial push. The archive includes `.gitattributes` but that file alone does not upload LFS objects.
- If using a GitHub-connected coding agent, verify its large-file/LFS upload capability; some APIs can commit only regular files.

## Command-line instructions (PowerShell, Git Bash or terminal)

From the extracted `Ambient_Odyssey_GitHub_Ready/` directory:

```bash
git lfs install
git init -b main
git add .
git lfs ls-files
git status --short
git commit -m "Initialize Ambient Odyssey Test 5 Audit1 source and Test 6 handoff"
git remote add origin https://github.com/YOUR_USERNAME/Ambient-Odyssey.git
git push -u origin main
```

Use your GitHub username or organization in place of `YOUR_USERNAME`. Authenticate with a credential manager, SSH, or an approved GitHub account connection. Do **not** paste personal access tokens into files or chat.

Before the first commit, `git lfs ls-files` should show the `#main.zip` worldgen asset. If it does not, fix Git LFS setup before committing. After pushing, verify the README, `AGENTS.md`, reports and `release_030/` appear remotely and that a fresh clone with `git lfs pull` can build.

### Branch workflow

```bash
git checkout -b structure/test6
# Implement and validate changes here
git add .
git commit -m "Implement Structure Test 6 changes"
git push -u origin structure/test6
```

Open a pull request from `structure/test6` into `main`. Tag `v0.3.1-test5-audit1` on the baseline commit if desired; add previous build/source ZIPs as **Release assets**, not source history, and preserve SHA checksums.

### Why not GitHub's browser upload?

The Tan's Huge Trees asset exceeds GitHub's 25 MiB browser upload limit, and standard Git history is ill-suited to repeatedly changing large binary ZIPs. Git LFS + Git commands (or GitHub Desktop with LFS) is required for the exact source tree here.
