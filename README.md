# GitSim - Git Workflow Simulator

> A scripted, fully in-memory Git simulator for training, onboarding, and interviews.
> No real Git commands. No real repository. Accurate Git semantics with clear explanations.

---

## What It Does

GitSim builds a fake Git repository in memory, then walks through every important Git concept with coloured terminal output and plain-English explanations at every step.

| # | Scenario |
|---|---------|
| <sub>1</sub> | <sub>Feature branch lifecycle - branch, stage, commit, PR, review, squash merge</sub> |
| <sub>2</sub> | <sub>Merge conflicts - how they arise, conflict markers, resolution workflow</sub> |
| <sub>3</sub> | <sub>Rebasing - rebase onto main, interactive rebase to clean commits</sub> |
| <sub>4</sub> | <sub>Bad practices - direct commits to main, force push, vague messages</sub> |

---

## Project Structure

```
gitsim/
├── run.py                         <- entry point
├── README.md
└── gitsim/
    ├── __init__.py
    ├── repo.py                    <- GitRepo state machine (the core)
    ├── actions.py                 <- composed workflow helpers
    ├── explain.py                 <- narrator / instructor voice
    ├── utils.py                   <- ANSI colours, diff blocks, log graph
    └── scenarios/
        ├── __init__.py
        ├── feature_branch.py      <- Scenario 1
        ├── merge_conflict.py      <- Scenario 2
        ├── rebase_example.py      <- Scenario 3
        └── bad_practice.py        <- Scenario 4
```

---

## Quick Start

```bash
cd /home/kevin/Projects/gitsim

# Run all 4 scenarios
python run.py

# Run a single scenario
python run.py --scenario 1    # feature branch
python run.py --scenario 2    # merge conflict
python run.py --scenario 3    # rebasing
python run.py -s 4            # bad practices
```

---

## Example Output

```
==================================================================
  GitSim - Git Workflow Simulator
==================================================================

[INIT] Initialised repository 'GalacticWeather' on branch main
    git init creates a hidden .git directory that stores all version
    history, configuration, and metadata.

[BRANCH] git branch feature/add-storm-endpoint -> created at a3f9c2b
    Creating a branch is instant and cheap - it's just a named
    pointer to commit a3f9c2b. No files are copied.

[STAGE] git add -p src/weather.py -> staged selected hunks
    git add -p (patch mode) lets you review each change hunk
    individually and choose whether to stage it.

[COMMIT] "feat(api): add storm endpoint with severity scoring"  [b7d1e4f]
    git commit saves the staged snapshot permanently into history.

[PR] Opened Pull Request #1: "feat: add storm endpoint"
[REVIEW] Hemmer APPROVED PR #1
[MERGE] Squash merge: feature/add-storm-endpoint -> main  [c8e2f5a]

[CONFLICT] Merge conflict in src/parser.py
<<<<<<< HEAD
def parse(data): raise TypeError('str required')
=======
def parse(data): if data is None: return ''
>>>>>>> incoming

[RESOLVE] Conflict in src/parser.py resolved and staged
[REBASE] git rebase origin/main -> replaying commits on top of main
[WARNING] You are committing DIRECTLY to main!
```

---

## What the Simulator Teaches

| Concept | How It Is Shown |
|---------|----------------|
| <sub>Branching strategy</sub> | <sub>Every feature gets its own branch from up-to-date main</sub> |
| <sub>Staging vs committing</sub> | <sub>WRITE -> STAGE -> COMMIT shown with diffs and git status</sub> |
| <sub>Pull Requests</sub> | <sub>Full PR lifecycle: open, comment, change-request, approve, merge</sub> |
| <sub>Code review</sub> | <sub>Reviewer requests changes; developer addresses feedback; re-approves</sub> |
| <sub>Merge conflicts</sub> | <sub>Two branches modify same line; conflict markers shown; resolution demonstrated</sub> |
| <sub>Rebasing</sub> | <sub>Standard rebase + interactive rebase to squash messy WIP commits</sub> |
| <sub>Stashing</sub> | <sub>Mid-task stash, switch branch, do hotfix, pop stash and continue</sub> |
| <sub>Bad practices</sub> | <sub>Direct main commit, force push, giant commits, vague messages - all shown with consequences</sub> |
| <sub>Commit graph</sub> | <sub>ASCII log graph printed after each scenario</sub> |

---

## Architecture

`GitRepo` is a pure in-memory state machine with:

- `_commits: dict[hash -> Commit]` - full history
- `_branches: dict[name -> Branch]` - branch pointers
- `_staged: dict[filename -> content]` - index
- `_working: dict[filename -> content]` - working tree
- `_tracked: dict[filename -> content]` - last commit snapshot
- `_remotes: dict[name -> {branch -> hash}]` - remote state
- `_prs: list[PullRequest]` - PR objects

All methods return `self` for fluent chaining. No side effects beyond stdout.

---

## No Dependencies

GitSim uses only the Python standard library. No pip install needed.

```bash
python --version   # >= 3.10 recommended
python run.py
```
