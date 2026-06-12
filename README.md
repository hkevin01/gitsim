<div align="center">

# GitSim - Git Workflow Simulator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/hkevin01/gitsim)
[![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)](https://github.com/hkevin01/gitsim)
[![Standard Library](https://img.shields.io/badge/stdlib%20only-no%20pip%20needed-brightgreen)](https://docs.python.org/3/library/)
[![Scenarios](https://img.shields.io/badge/Scenarios-5-orange)](https://github.com/hkevin01/gitsim)
[![Concepts](https://img.shields.io/badge/Git%20Concepts-12-blueviolet)](https://github.com/hkevin01/gitsim)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/hkevin01/gitsim)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/hkevin01/gitsim/pulls)

> A scripted, fully in-memory Git simulator for training, onboarding, and interviews.
> No real Git commands. No real repository. Accurate Git semantics with clear, colour-coded explanations at every single step.

</div>

---

## Table of Contents

- [What Is GitSim?](#what-is-gitsim)
- [Why GitSim Exists](#why-gitsim-exists)
- [Quick Start](#quick-start)
- [Scenarios](#scenarios)
- [Architecture Overview](#architecture-overview)
- [Commit vs Rebase - Deep Dive](#commit-vs-rebase---deep-dive)
- [Never Commit Directly to Main](#never-commit-directly-to-main)
- [Syncing Before You Push - Why It Matters](#syncing-before-you-push---why-it-matters)
- [Git History and Diffs - Auto vs Manual](#git-history-and-diffs---auto-vs-manual)
- [Types of Merging](#types-of-merging)
- [The PullRequest Object](#the-pullrequest-object)
- [Corporate Branching Strategy](#corporate-branching-strategy)
- [Branch Tree in Three Dimensions](#branch-tree-in-three-dimensions)
- [Deployment Environments](#deployment-environments)
- [Developer Sprint Workflow - Step by Step](#developer-sprint-workflow---step-by-step)
- [How Documentation Is Tracked by Git](#how-documentation-is-tracked-by-git)
- [Module Reference](#module-reference)
- [Data Structures](#data-structures)
- [State Machine Flow](#state-machine-flow)
- [Algorithm and Design Decisions](#algorithm-and-design-decisions)
- [Tech Stack](#tech-stack)
- [Example Output](#example-output)
- [What the Simulator Teaches](#what-the-simulator-teaches)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Key Takeaways](#key-takeaways)

---

## What Is GitSim?

GitSim is a pure-Python, fully in-memory Git workflow simulator designed to teach, demonstrate, and reinforce professional Git practices without ever touching the filesystem or executing a single real `git` command. It reproduces the complete internal state of a Git repository - branches, commits, the staging index, the working tree, remotes, and pull requests - entirely inside Python data structures. Every simulated action prints both the equivalent Git command a developer would type in a real project and a plain-English explanation of what that command does and why it matters.

The goal is not just to show the syntax. It is to build a mental model of Git's internals - understanding that a branch is just a named pointer, that a commit is an immutable content-addressed snapshot, and that rebasing is replaying commits rather than copying files. These concepts are difficult to grasp in isolation; GitSim makes them visible and sequential, so learners can watch the state change step by step in a controlled, repeatable environment.

> [!NOTE]
> GitSim uses **zero external dependencies**. It runs with any Python 3.10+ installation and requires no `pip install`, no virtual environment, and no Git binary on the host machine. This makes it ideal for sandboxed training environments, CI pipelines, and developer onboarding kiosks.

---

## Why GitSim Exists

Most Git tutorials show commands in isolation - `git branch`, `git commit`, `git merge` - without demonstrating how they interact in a real professional workflow. New developers frequently encounter problems they cannot diagnose because they lack the mental model of what Git is actually doing. They do not understand why `git rebase` rewrites history, why `git add -p` is safer than `git add .`, or why force-pushing a shared branch is destructive to teammates.

GitSim was built to close that gap. By simulating the entire lifecycle in sequence - from repository initialisation through feature branches, pull requests, code review, conflict resolution, rebasing, and intentional bad practices - it gives learners the complete picture in a single run. Each step is annotated with the rationale, not just the mechanics. The simulator is designed so that a junior developer with no Git experience can run it once and leave with enough vocabulary and mental models to participate in a professional team workflow from day one.

> [!IMPORTANT]
> GitSim is not a replacement for hands-on Git practice. It is a **structured introduction** that gives learners the vocabulary and mental models they need before touching a real repository. Use it before onboarding sessions, in lunch-and-learn workshops, or as a live demonstration tool when explaining Git concepts to a team.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/hkevin01/gitsim.git
cd gitsim

# Run all 5 scenarios in sequence
python run.py

# Run a single scenario by number
python run.py --scenario 1    # Feature branch lifecycle
python run.py --scenario 2    # Merge conflict resolution
python run.py --scenario 3    # Rebasing onto main
python run.py -s 4            # Bad practices demonstration
python run.py -s 5            # Corporate branching strategy
```

> [!TIP]
> Pipe the output through `less -R` to preserve ANSI colours and scroll at your own pace:
> `python run.py | less -R`
> Press `q` to quit, `Space` to page down, and `/` to search for any term like `CONFLICT` or `REBASE`.

---

## Scenarios

GitSim ships with four fully scripted scenarios. Each scenario receives its own fresh `GitRepo` instance so there is zero state bleed between runs. You can run them individually or all at once.

| # | Scenario | Git Concepts Covered |
|---|----------|---------------------|
| <sub>1</sub> | <sub>**Feature Branch Workflow**</sub> | <sub>Branch creation, `git add -p` staged hunks, intentional commits, fetch+rebase sync, push to remote, PR open, change-request review cycle, final approval, squash merge, branch cleanup, commit log graph</sub> |
| <sub>2</sub> | <sub>**Merge Conflict Resolution**</sub> | <sub>Two diverging branches modifying the same line, conflict marker rendering (`<<<<<<<`, `=======`, `>>>>>>>`), manual resolution, staging the fix, completing the merge commit with two parents</sub> |
| <sub>3</sub> | <sub>**Rebasing**</sub> | <sub>Standard rebase onto main to linearise a diverged history, interactive rebase to squash multiple WIP commits into one clean commit, hash rewrite demonstration, force-push requirement after rebase</sub> |
| <sub>4</sub> | <sub>**Bad Practices**</sub> | <sub>Direct commit to main, vague commit messages, giant monolithic commits, force-push to a shared branch - all shown with explicit `[WARNING]` output and the correct alternative demonstrated immediately after each violation</sub> |
| <sub>5</sub> | <sub>**Corporate Branching Strategy**</sub> | <sub>Full enterprise branch hierarchy: `main`, `develop`, `release/x.y.z`, `feature/TICKET-description`, `bugfix/TICKET-description`, `test/sprint-description`, `hotfix/TICKET-description` - correct naming conventions, merge targets, and lifecycle rules for each tier on a large multi-developer project</sub> |

---

## Corporate Branching Strategy

On a large project with many developers working simultaneously, a flat single-branch workflow breaks down immediately. Two developers working on the same file will collide. A half-finished feature will block a critical hotfix from shipping. A poorly named branch makes it impossible to know at a glance what work is in progress. The solution is a structured branch hierarchy where every branch has a specific tier, a specific naming convention, a specific source branch it must be cut from, and a specific target it must merge back into.

GitSim Scenario 5 (`python run.py --scenario 5`) demonstrates this full hierarchy end to end, with realistic ticket-ID-based naming, multi-developer parallel work, review cycles, a release hardening phase, and an emergency hotfix. The sections below document the conventions so they can be applied directly on a real project.

> [!IMPORTANT]
> The most critical rule of corporate branching is that **the merge direction is strictly enforced**. Feature branches merge into `develop`. Release branches merge into `main` AND back into `develop`. Hotfix branches merge into `main` AND back into `develop`. Nothing except a release branch or hotfix branch ever merges directly into `main`. Violating these merge targets is the single most common cause of "lost fixes" - where a bug fix shipped in one release is accidentally missing from the next release because the fix never made it back to `develop`.

### The Branch Hierarchy

```mermaid
gitGraph
   commit id: "v1.0.0 baseline" tag: "v1.0.0"
   branch develop
   checkout develop
   commit id: "open v1.1.0 sprint"
   branch feature/PROJ-142-user-auth
   commit id: "feat: JWT login"
   commit id: "fix: expiry check"
   checkout develop
   merge feature/PROJ-142-user-auth id: "squash: PROJ-142"
   branch feature/PROJ-157-password-reset
   commit id: "feat: reset flow"
   checkout develop
   merge feature/PROJ-157-password-reset id: "squash: PROJ-157"
   branch bugfix/PROJ-163-race-condition
   commit id: "fix: login lock"
   checkout develop
   merge bugfix/PROJ-163-race-condition id: "squash: PROJ-163"
   branch release/1.1.0
   commit id: "bump v1.1.0"
   branch bugfix/PROJ-171-header-case
   commit id: "fix: header case"
   checkout release/1.1.0
   merge bugfix/PROJ-171-header-case id: "squash: PROJ-171"
   checkout main
   merge release/1.1.0 id: "ship v1.1.0" tag: "v1.1.0"
   branch hotfix/PROJ-175-null-crash
   commit id: "hotfix: null guard"
   checkout main
   merge hotfix/PROJ-175-null-crash id: "hotfix ship" tag: "v1.1.1"
```

> The diagram above shows the full corporate branch lifecycle for a single sprint. Read it left to right: `main` is the bottom rail (production), `develop` is the integration rail, feature and bugfix branches fan out from `develop` and merge back in, a `release` branch is cut from `develop` for hardening, and a `hotfix` branch fans out directly from `main` for an emergency production patch.

### Branch Naming Conventions

Consistent naming is not aesthetics - it is tooling infrastructure. CI/CD pipelines use branch name prefixes to determine what environment to deploy to. JIRA and Linear use branch names to automatically link commits to tickets. Slack and Teams integrations use branch names in notifications. GitHub Actions `on: push: branches:` filters use branch name patterns. Every convention below exists because something downstream depends on it.

| # | Branch Type | Naming Pattern | Example | Source Branch | Merge Target | Lifetime |
|---|-------------|---------------|---------|--------------|-------------|----------|
| <sub>1</sub> | <sub>**main**</sub> | <sub>`main`</sub> | <sub>`main`</sub> | <sub>n/a - permanent</sub> | <sub>n/a - only receives merges</sub> | <sub>Permanent - never deleted</sub> |
| <sub>2</sub> | <sub>**develop**</sub> | <sub>`develop`</sub> | <sub>`develop`</sub> | <sub>Cut from `main` once at project start</sub> | <sub>n/a - only receives merges from feature/bugfix/test</sub> | <sub>Permanent - never deleted</sub> |
| <sub>3</sub> | <sub>**feature**</sub> | <sub>`feature/<TICKET-ID>-<kebab-description>`</sub> | <sub>`feature/PROJ-142-user-authentication`</sub> | <sub>`develop` (always up-to-date)</sub> | <sub>`develop` via PR with squash merge</sub> | <sub>Short - delete immediately after merge</sub> |
| <sub>4</sub> | <sub>**bugfix**</sub> | <sub>`bugfix/<TICKET-ID>-<kebab-description>`</sub> | <sub>`bugfix/PROJ-163-login-race-condition`</sub> | <sub>`develop` (for dev/QA bugs) or `release/x.y.z` (for release bugs)</sub> | <sub>`develop` or `release/x.y.z` depending on source</sub> | <sub>Short - delete immediately after merge</sub> |
| <sub>5</sub> | <sub>**test / qa**</sub> | <sub>`test/<sprint-or-ticket>-<description>`</sub> | <sub>`test/PROJ-sprint-22-auth-integration`</sub> | <sub>`develop`</sub> | <sub>`develop` via PR</sub> | <sub>Short - delete after merge</sub> |
| <sub>6</sub> | <sub>**release**</sub> | <sub>`release/<semver>` or `release/<year-quarter>`</sub> | <sub>`release/1.1.0` or `release/2024-Q3`</sub> | <sub>`develop` when sprint is complete</sub> | <sub>`main` AND back-merge into `develop`</sub> | <sub>Medium - kept until after release, then archived or deleted</sub> |
| <sub>7</sub> | <sub>**hotfix**</sub> | <sub>`hotfix/<TICKET-ID>-<kebab-description>`</sub> | <sub>`hotfix/PROJ-175-null-deref-crash`</sub> | <sub>`main` (ONLY branch type that does this)</sub> | <sub>`main` AND back-merge into `develop`</sub> | <sub>Short - delete immediately after both merges</sub> |
| <sub>8</sub> | <sub>**release-candidate**</sub> | <sub>`rc/<version>-rc<n>`</sub> | <sub>`rc/1.1.0-rc1`</sub> | <sub>`release/x.y.z` when ready for staging deploy</sub> | <sub>No merge target - deployed to staging, deleted after go/no-go decision</sub> | <sub>Very short - ephemeral staging snapshot</sub> |

### What Each Branch Tier Looks Like

#### Individual Developer Branch - `feature/PROJ-142-user-authentication`

This is what a developer creates for every unit of work. The ticket ID (`PROJ-142`) comes from the sprint planning system (JIRA, Linear, GitHub Issues). The description is kebab-case, lowercase, concise - enough to understand the branch purpose without reading the ticket. The developer cuts this from the latest `develop`, does all their work here, opens a PR targeting `develop`, gets at least one approval, and squash-merges. The branch is deleted the moment the PR merges.

```
git checkout develop
git pull origin develop
git checkout -b feature/PROJ-142-user-authentication
# ... work, commit, push ...
git push -u origin feature/PROJ-142-user-authentication
# open PR: feature/PROJ-142-user-authentication -> develop
```

> [!TIP]
> Many teams configure their git client to automatically name branches from ticket IDs. In JIRA, clicking "Create branch" pre-populates the name as `feature/PROJ-142-user-authentication`. In GitHub Issues, the "Create a branch" button does the same. Use these integrations - they eliminate naming inconsistencies and automatically link commits to issues.

#### Testing / QA Branch - `test/PROJ-sprint-22-auth-integration-tests`

This is what a QA engineer or developer creates when authoring or updating test suites independently of feature work. It follows the same creation, review, and merge pattern as a feature branch. Some teams use a dedicated long-lived `qa` branch that mirrors `develop` and is auto-deployed to a QA environment - individual test branches merge into `qa` rather than `develop` directly. Other teams skip the separate `qa` branch and merge test branches directly into `develop`. Either pattern works - the key is consistency.

```
git checkout develop
git pull origin develop  
git checkout -b test/PROJ-sprint-22-auth-integration-tests
# ... write tests, commit ...
git push -u origin test/PROJ-sprint-22-auth-integration-tests
# open PR: test/PROJ-sprint-22-* -> develop
```

#### Development Integration Branch - `develop`

This is the shared integration rail. It contains everything that is done but not yet shipped. It should be deployable to a development or staging environment at all times. CI runs on every push to `develop`. If `develop` is red (failing CI), fixing it is the highest priority for the entire team - a broken integration branch blocks everyone. The `develop` branch is never deleted and is never rebased - only merged into.

> [!WARNING]
> Never rebase the `develop` branch. Rebasing a shared branch rewrites the commit hashes that every developer has already pulled. Anyone with a local copy of `develop` will have a diverged history that is extremely painful to reconcile across the entire team. `develop` only ever moves forward via merge commits.

#### Release Hardening Branch - `release/1.1.0`

This is the final gate before production. When a sprint completes and `develop` is stable, a release branch is cut from `develop`. From this point, `develop` can continue accepting feature work for the next sprint while the release branch is frozen for hardening. Only bug fixes (as `bugfix/` branches merging into the release branch) are allowed on a release branch. No new features. The release branch is deployed to a staging environment for final acceptance testing, performance testing, and security review.

Once the release is signed off, the release branch merges into `main` (which triggers the production deployment) AND back-merges into `develop` (to carry forward any last-minute fixes). This double-merge is critical - skipping the back-merge into `develop` is how fixes get lost between releases.

```
git checkout develop
git pull origin develop
git checkout -b release/1.1.0
# ... only bugfixes from here ...
# When ready:
# PR: release/1.1.0 -> main   (production ship)
# PR: release/1.1.0 -> develop  (carry fixes forward)
```

#### Emergency Production Patch - `hotfix/PROJ-175-null-deref-crash`

This is the only branch type that is cut directly from `main`. It is used when a critical bug is found in production that cannot wait for the next release cycle. The developer checks out `main`, creates the hotfix branch, makes the minimal targeted fix, gets expedited review (often two approvals required even for small changes because of the production impact), and merges into `main` for immediate deployment. The hotfix is then also merged into `develop` and into any active release branch so the fix propagates everywhere.

```
git checkout main
git pull origin main
git checkout -b hotfix/PROJ-175-null-deref-crash-on-empty-token
# ... fix, test, commit ...
git push -u origin hotfix/PROJ-175-null-deref-crash-on-empty-token
# PR: hotfix/... -> main   (emergency production fix)
# PR: hotfix/... -> develop  (prevent regression in next release)
```

> [!WARNING]
> A hotfix that merges to `main` but is NOT back-merged into `develop` will be overwritten by the next regular release. This is one of the most common and damaging Git mistakes in production systems. Always create BOTH PRs - one to `main` and one to `develop` - when shipping a hotfix.

### Merge Direction Rules Summary

```mermaid
flowchart TD
    FEAT["feature/PROJ-142-*\nDeveloper daily work"] -->|"PR + squash merge"| DEV["develop\nIntegration rail"]
    BUG["bugfix/PROJ-163-*\nNon-critical bug fix"] -->|"PR + squash merge"| DEV
    TEST["test/sprint-22-*\nQA and test suites"] -->|"PR + squash merge"| DEV
    DEV -->|"Cut when sprint complete"| REL["release/1.1.0\nHardening only"]
    REL_BUG["bugfix/PROJ-171-*\nRelease bug fix"] -->|"PR + squash merge"| REL
    REL -->|"PR after sign-off"| MAIN["main\nProduction"]
    REL -->|"Back-merge"| DEV
    MAIN -->|"Cut for emergency"| HOT["hotfix/PROJ-175-*\nEmergency patch"]
    HOT -->|"PR immediate"| MAIN
    HOT -->|"Back-merge"| DEV
    style MAIN fill:#1a3a1a,stroke:#2ea043,color:#fff
    style DEV fill:#1a2a3a,stroke:#4a9eff,color:#fff
    style REL fill:#3a2a1a,stroke:#f0a030,color:#fff
    style HOT fill:#3a1a1a,stroke:#ff4a4a,color:#fff
```

> The arrows show the **only permitted merge directions**. Feature, bugfix, and test branches all converge on `develop`. Release branches fan out from `develop` and merge into both `main` and back into `develop`. Hotfix branches fan out from `main` and merge into both `main` and `develop`. There are no shortcuts.

### Branch Protection Rules (What GitHub Enforces)

In a real corporate repository, the branch hierarchy is enforced by branch protection rules configured at the repository level. GitSim simulates the workflow you would follow under these rules. The table below shows typical protection settings for each long-lived branch tier.

| # | Branch | Require PR | Min Approvals | Require CI Pass | Allow Direct Push | Allow Force Push | Delete on Merge |
|---|--------|-----------|--------------|----------------|------------------|-----------------|----------------|
| <sub>1</sub> | <sub>`main`</sub> | <sub>Yes - required</sub> | <sub>2</sub> | <sub>Yes - all checks</sub> | <sub>No</sub> | <sub>No</sub> | <sub>n/a - permanent</sub> |
| <sub>2</sub> | <sub>`develop`</sub> | <sub>Yes - required</sub> | <sub>1</sub> | <sub>Yes - unit tests</sub> | <sub>No</sub> | <sub>No</sub> | <sub>n/a - permanent</sub> |
| <sub>3</sub> | <sub>`release/*`</sub> | <sub>Yes - required</sub> | <sub>2</sub> | <sub>Yes - full suite</sub> | <sub>No</sub> | <sub>No</sub> | <sub>After double-merge</sub> |
| <sub>4</sub> | <sub>`feature/*`</sub> | <sub>Recommended</sub> | <sub>1</sub> | <sub>Yes - unit tests</sub> | <sub>No (by policy)</sub> | <sub>Only author (own branch)</sub> | <sub>Yes - auto on merge</sub> |
| <sub>5</sub> | <sub>`bugfix/*`</sub> | <sub>Yes - required</sub> | <sub>1</sub> | <sub>Yes - unit tests</sub> | <sub>No (by policy)</sub> | <sub>Only author (own branch)</sub> | <sub>Yes - auto on merge</sub> |
| <sub>6</sub> | <sub>`hotfix/*`</sub> | <sub>Yes - URGENT flag</sub> | <sub>2</sub> | <sub>Yes - all checks</sub> | <sub>No</sub> | <sub>No</sub> | <sub>Yes - after both merges</sub> |

---

## Branch Tree in Three Dimensions

A flat diagram shows branches as lines but does not convey that they exist simultaneously in three distinct layers: **local** (your laptop), **remote** (origin on GitHub/GitLab), and **deployed** (what is running in each environment). This section shows the full picture.

### The Three Layers Every Branch Lives In

```mermaid
flowchart TB
    subgraph LOCAL ["💻 Layer 1 — Your Local Machine"]
        direction LR
        LM["main"] ~~~ LD["develop"] ~~~ LF["feature/PROJ-142"] ~~~ LH["hotfix/PROJ-175"]
    end

    subgraph REMOTE ["☁️ Layer 2 — origin (GitHub / GitLab)"]
        direction LR
        RM["origin/main"] ~~~ RD["origin/develop"] ~~~ RF["origin/feature/PROJ-142"] ~~~ RR["origin/release/1.1.0"]
    end

    subgraph DEPLOYED ["🚀 Layer 3 — Deployed Environments"]
        direction LR
        ENV_DEV["🔵 dev\n(origin/develop)"] ~~~ ENV_QA["🟡 qa / staging\n(origin/release/1.1.0)"] ~~~ ENV_PROD["🟢 production\n(origin/main @ tag v1.1.0)"]
    end

    LOCAL -- "git push" --> REMOTE
    REMOTE -- "git fetch" --> LOCAL
    REMOTE -- "CI/CD pipeline deploys on merge" --> DEPLOYED
```

> [!NOTE]
> Your local branches and `origin/*` remote-tracking refs are **two separate things**. When you run `git fetch`, Git updates `origin/develop` on your machine to match what is on GitHub — but your local `develop` branch does not move. You must `git rebase origin/develop` (or `git merge origin/develop`) to actually incorporate those changes into your local branch. This is why `git pull` = `git fetch` + `git merge`.

### The Full Branch Tree — All Tiers Simultaneously

This is what the repository looks like to a team lead watching `git log --all --graph` on a busy sprint day. All branches exist at the same time. Each developer is on their own feature branch. The `develop` branch is the integration point. The `release` branch is frozen for QA.

```mermaid
flowchart LR
    subgraph PROD ["🟢 PRODUCTION"]
        MAIN["main\nv1.0.0 ● v1.1.0 ●"]
    end

    subgraph RELEASE ["🟡 HARDENING"]
        REL["release/1.1.0"]
        RELFIX["bugfix/PROJ-171\nheader-case"]
    end

    subgraph INTEGRATION ["🔵 INTEGRATION"]
        DEV["develop"]
    end

    subgraph FEATURES ["🟣 ACTIVE WORK"]
        direction TB
        F1["feature/PROJ-142\nuser-auth\n👤 Alice"]
        F2["feature/PROJ-157\npassword-reset\n👤 Bob"]
        F3["feature/PROJ-188\nnew-dashboard\n👤 Carol"]
        B1["bugfix/PROJ-163\nrace-condition\n👤 Dave"]
        T1["test/sprint-22-auth\n👤 QA Team"]
    end

    subgraph EMERGENCY ["🔴 HOTFIX"]
        HOT["hotfix/PROJ-175\nnull-crash\n👤 Alice"]
    end

    F1 & F2 & F3 & B1 & T1 -- "PR → squash merge" --> DEV
    DEV -- "sprint complete → cut" --> REL
    RELFIX -- "PR → merge" --> REL
    REL -- "sign-off → merge" --> MAIN
    REL -- "back-merge" --> DEV
    MAIN -- "cut for emergency" --> HOT
    HOT -- "PR → merge" --> MAIN
    HOT -- "back-merge" --> DEV

    style MAIN fill:#0d3b1e,stroke:#2ea043,color:#fff
    style DEV fill:#1a2a3a,stroke:#4a9eff,color:#fff
    style REL fill:#3a2a0a,stroke:#f0a030,color:#fff
    style HOT fill:#3a0a0a,stroke:#ff4a4a,color:#fff
    style F1 fill:#1a1a3a,stroke:#8a4aff,color:#fff
    style F2 fill:#1a1a3a,stroke:#8a4aff,color:#fff
    style F3 fill:#1a1a3a,stroke:#8a4aff,color:#fff
    style B1 fill:#1a2a1a,stroke:#4aff8a,color:#fff
    style T1 fill:#2a1a2a,stroke:#ff4aaa,color:#fff
    style RELFIX fill:#2a2a0a,stroke:#f0c030,color:#fff
```

---

## Deployment Environments

Every branch tier maps to a specific deployment environment. Code does not jump straight from a developer's laptop to production — it flows through a pipeline of environments, each with a different stability requirement and audience. Understanding this pipeline explains why the branch hierarchy exists: each branch tier is the source of truth for one environment.

```mermaid
flowchart LR
    subgraph DEV_ENV ["🔵 Development Environment"]
        direction TB
        DA["Auto-deployed on every\nmerge to develop"]
        DB["Used by: developers\nfor integration testing"]
        DC["Stability bar: CI green\n(unit tests pass)"]
        DD["URL: dev.internal.company.com"]
    end

    subgraph QA_ENV ["🟡 QA / Staging Environment"]
        direction TB
        QA["Auto-deployed when\nrelease branch is cut"]
        QB["Used by: QA engineers\nfor acceptance testing"]
        QC["Stability bar: full regression\nsuite must pass"]
        QD["URL: staging.company.com"]
    end

    subgraph UAT_ENV ["🟠 UAT Environment"]
        direction TB
        UA["Deployed from release\nbranch on QA sign-off"]
        UB["Used by: product owner,\nbusiness stakeholders"]
        UC["Stability bar: business\nacceptance criteria met"]
        UD["URL: uat.company.com"]
    end

    subgraph PROD_ENV ["🟢 Production"]
        direction TB
        PA["Deployed on merge\nof release to main"]
        PB["Used by: real users"]
        PC["Stability bar: all gates\npassed + signed off"]
        PD["URL: company.com"]
    end

    BRANCH_DEV["origin/develop"] --> DEV_ENV
    BRANCH_REL["origin/release/x.y.z"] --> QA_ENV
    BRANCH_REL --> UAT_ENV
    BRANCH_MAIN["origin/main @ tag"] --> PROD_ENV

    DEV_ENV -- "QA promoted\nsprint complete" --> QA_ENV
    QA_ENV -- "QA signed off" --> UAT_ENV
    UAT_ENV -- "PO + security\nsigned off" --> PROD_ENV

    style PROD_ENV fill:#0d3b1e,stroke:#2ea043,color:#fff
    style QA_ENV fill:#3a2a0a,stroke:#f0a030,color:#fff
    style UAT_ENV fill:#3a1a0a,stroke:#ff8a00,color:#fff
    style DEV_ENV fill:#1a2a3a,stroke:#4a9eff,color:#fff
```

| # | Environment | Source Branch | Deployed By | Who Uses It | Stability Bar |
|---|-------------|--------------|-------------|------------|---------------|
| <sub>1</sub> | <sub>**Local** (your machine)</sub> | <sub>`feature/*` branch</sub> | <sub>You — `python run.py` or `npm start`</sub> | <sub>Developer only</sub> | <sub>"It works on my machine"</sub> |
| <sub>2</sub> | <sub>**Dev / Integration**</sub> | <sub>`develop`</sub> | <sub>CI/CD on every merge to develop</sub> | <sub>Developers, for integration sanity checks</sub> | <sub>Unit tests pass, no merge conflicts</sub> |
| <sub>3</sub> | <sub>**QA / Staging**</sub> | <sub>`release/x.y.z`</sub> | <sub>CI/CD when release branch is created</sub> | <sub>QA engineers running acceptance tests</sub> | <sub>Full regression suite green</sub> |
| <sub>4</sub> | <sub>**UAT**</sub> | <sub>`release/x.y.z`</sub> | <sub>Manual trigger after QA sign-off</sub> | <sub>Product owner, business stakeholders</sub> | <sub>Acceptance criteria met</sub> |
| <sub>5</sub> | <sub>**Production**</sub> | <sub>`main` @ version tag</sub> | <sub>CI/CD on merge to main</sub> | <sub>Real end users</sub> | <sub>All environments signed off</sub> |
| <sub>6</sub> | <sub>**Hotfix staging**</sub> | <sub>`hotfix/*`</sub> | <sub>Manual or automated on hotfix push</sub> | <sub>Developer + senior reviewer only</sub> | <sub>Bug fixed, no regressions on critical paths</sub> |

> [!IMPORTANT]
> Code only moves **forward** through the environment pipeline — local → dev → QA → UAT → production. It never skips an environment. A developer who deploys untested code directly to production bypasses every safety check the pipeline provides. The branch protection and environment promotion rules exist precisely to prevent this.

---

## Developer Sprint Workflow - Step by Step

This section answers the most common question a developer asks when joining a team: **"I just got assigned a ticket - what exactly do I do, in what order, and why?"** It covers the full lifecycle from sprint planning through code review, testing, documentation, and final merge to production. Every step is shown as the exact command you would type, the branch it happens on, and who is responsible for it.

Understanding this workflow end to end - not just the Git commands, but the social and quality-control contract that surrounds them - is what separates a developer who ships safely from one who breaks the build.

> [!NOTE]
> GitSim Scenario 5 (`python run.py --scenario 5`) simulates the Git operations in this workflow. The sections below describe the human process that drives those Git operations - who decides what, when documentation is written, when tests are written, and what the reviewer is actually checking.

---

### Sprint Start - What Happens Before You Write a Single Line

Before any developer writes any code, the team goes through sprint planning. In sprint planning, the product owner presents the highest-priority items from the backlog, the team estimates effort, and tasks are assigned. Every task becomes a ticket in the project management system (JIRA, Linear, GitHub Issues, Azure DevOps). Each ticket has an ID, a description, acceptance criteria, and an assignee.

As a developer, you receive a ticket number and a description. **Do not start writing code until you fully understand the acceptance criteria.** If the acceptance criteria are vague, ask now - not after you have spent two days building the wrong thing. This is the cheapest moment to clarify scope.

> [!TIP]
> Read the ticket, read the linked design document or Figma spec, and read the test cases written by QA (if your team does spec-driven development). Then look at the code area you will be touching. Pull down the latest `develop` branch and read the relevant files before creating your branch. Twenty minutes of reading saves hours of rework.

---

### The Complete Developer Task Lifecycle

```mermaid
flowchart TD
    A(["🗓️ Sprint Planning\nTicket assigned to developer"]) --> B
    B(["📖 Read ticket + acceptance criteria\nAsk questions NOW if unclear"]) --> C
    C(["⬇️ Pull latest develop\ngit checkout develop\ngit pull origin develop"]) --> D
    D(["🌿 Create feature branch\ngit checkout -b feature/PROJ-123-description"]) --> E
    E(["💻 Write code\nSmall focused commits\ngit add -p + git commit"]) --> F
    F(["🧪 Write / update tests\nUnit tests alongside the code\nNot after - alongside"]) --> G
    G(["📋 Self-review\ngit diff develop..HEAD\nRead every line you changed"]) --> H
    H(["🔄 Sync with develop\ngit fetch + git rebase origin/develop"]) --> I
    I(["🚀 Push branch\ngit push -u origin feature/PROJ-123"]) --> J
    J(["📬 Open Pull Request\nTitle + description + screenshots\nLink the ticket"]) --> K
    K(["👥 Peer Code Review\nAt least 1 approval required"]) --> L{"Changes\nrequested?"}
    L -->|"Yes"| M(["🔧 Address feedback\nnew commits + push\nReply to each comment"])
    M --> K
    L -->|"No - Approved"| N(["✅ CI passes\nAll tests green"])
    N --> O(["🔀 Merge to develop\nSquash merge via PR"])
    O --> P(["🗑️ Delete feature branch\nautomatically or manually"])
    P --> Q(["📝 Update documentation\nif public API or behaviour changed"])
    Q --> R(["📦 Release branch cut\nwhen sprint complete"])
    R --> S(["🧪 QA full regression\non release branch"])
    S --> T(["🚢 Merge release to main\nProduction deploy"])
    style A fill:#1a2a3a,stroke:#4a9eff,color:#fff
    style D fill:#1a3a1a,stroke:#2ea043,color:#fff
    style J fill:#2a1a3a,stroke:#9a4aff,color:#fff
    style K fill:#3a2a1a,stroke:#f0a030,color:#fff
    style T fill:#0d3b1e,stroke:#2ea043,color:#fff
```

---

### Step-by-Step Command Reference

The table below is the definitive checklist. Each row is one discrete action, the exact command to run, the branch it happens on, and who is responsible. Print this and keep it next to your keyboard until the workflow is muscle memory.

| # | Phase | Action | Exact Command | Branch | Who |
|---|-------|--------|--------------|--------|-----|
| <sub>1</sub> | <sub>**Sprint start**</sub> | <sub>Read the ticket, acceptance criteria, and any linked design docs. Ask questions before writing code.</sub> | <sub>*(no command - human step)*</sub> | <sub>n/a</sub> | <sub>Developer</sub> |
| <sub>2</sub> | <sub>**Sprint start**</sub> | <sub>Switch to develop and pull the absolute latest code from origin. Never branch from a stale local develop.</sub> | <sub>`git checkout develop`<br>`git pull origin develop`</sub> | <sub>`develop`</sub> | <sub>Developer</sub> |
| <sub>3</sub> | <sub>**Sprint start**</sub> | <sub>Create your feature branch from the freshly pulled develop. Use the ticket ID in the branch name.</sub> | <sub>`git checkout -b feature/PROJ-123-short-description`</sub> | <sub>new `feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>4</sub> | <sub>**Development**</sub> | <sub>Write code. Make small, frequent, focused commits. Each commit should do one thing.</sub> | <sub>`git add -p`<br>`git commit -m "feat(scope): PROJ-123 what and why"`</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>5</sub> | <sub>**Development**</sub> | <sub>Write or update unit tests alongside the code - not after. If you write tests after the code is done you will rationalise rather than verify.</sub> | <sub>`git add tests/`<br>`git commit -m "test(scope): PROJ-123 add unit tests"`</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>6</sub> | <sub>**Development**</sub> | <sub>Run all tests locally before pushing. Never push a branch with known failing tests.</sub> | <sub>`python -m pytest` or team test command</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>7</sub> | <sub>**Before PR**</sub> | <sub>Self-review your entire diff. Read every line you changed as if you are the reviewer. This is the single highest-ROI habit in software development.</sub> | <sub>`git diff develop..HEAD`<br>or open the diff in your IDE</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>8</sub> | <sub>**Before PR**</sub> | <sub>Fetch the latest develop and rebase your branch onto it. This ensures your PR is based on current code and the eventual merge will be clean.</sub> | <sub>`git fetch origin`<br>`git rebase origin/develop`</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>9</sub> | <sub>**Before PR**</sub> | <sub>Resolve any rebase conflicts, run tests again to confirm the resolved state is still correct.</sub> | <sub>*(edit conflicted files)*<br>`git add <file>`<br>`git rebase --continue`</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>10</sub> | <sub>**Before PR**</sub> | <sub>Push your branch to origin. Use `-u` the first time to set the upstream tracking reference.</sub> | <sub>`git push -u origin feature/PROJ-123-short-description`</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>11</sub> | <sub>**PR open**</sub> | <sub>Open the pull request. Write a description that explains WHAT changed, WHY it changed, how to test it, and any screenshots for UI changes. Link the ticket.</sub> | <sub>*(GitHub/GitLab web UI)*<br>Source: `feature/PROJ-123-*`<br>Target: `develop`</sub> | <sub>PR: `feature` → `develop`</sub> | <sub>Developer</sub> |
| <sub>12</sub> | <sub>**PR open**</sub> | <sub>Assign at least one reviewer. For security-sensitive or complex changes, assign two. Tag QA if acceptance testing is needed on the PR.</sub> | <sub>*(GitHub/GitLab web UI)*</sub> | <sub>PR</sub> | <sub>Developer</sub> |
| <sub>13</sub> | <sub>**Code review**</sub> | <sub>Reviewer reads the ticket, reads the diff, checks logic, security, test coverage, naming, and style. Leaves specific actionable comments on individual lines.</sub> | <sub>*(GitHub/GitLab review UI)*</sub> | <sub>PR</sub> | <sub>Reviewer (peer developer)</sub> |
| <sub>14</sub> | <sub>**Code review**</sub> | <sub>Address every comment. For each comment, either fix it (new commit + push) or reply explaining why you disagree and discuss until resolved. Do not just click "resolve".</sub> | <sub>`git add -p`<br>`git commit -m "fix: address review feedback"`<br>`git push`</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>15</sub> | <sub>**Code review**</sub> | <sub>Reviewer re-reviews after changes and approves. On GitHub, clicking Approve sets the PR to mergeable (subject to branch protection rules).</sub> | <sub>*(GitHub/GitLab review UI)*</sub> | <sub>PR</sub> | <sub>Reviewer</sub> |
| <sub>16</sub> | <sub>**Testing**</sub> | <sub>CI runs automatically on every push (unit tests, linting, security scan). All checks must be green before merge is allowed. Fix any CI failures before asking for re-review.</sub> | <sub>*(automated - watch CI status)*</sub> | <sub>PR</sub> | <sub>CI system + Developer (to fix failures)</sub> |
| <sub>17</sub> | <sub>**Testing**</sub> | <sub>QA engineer (if applicable) picks up the PR or deploys the branch to a QA environment and runs manual acceptance tests against the ticket's acceptance criteria.</sub> | <sub>*(QA environment deploy)*</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>QA Engineer</sub> |
| <sub>18</sub> | <sub>**Documentation**</sub> | <sub>If the change adds, modifies, or removes a public API, a configuration option, or user-facing behaviour: update the documentation NOW, as part of this PR, before it merges. Never leave documentation for later.</sub> | <sub>`git add docs/`<br>`git commit -m "docs: PROJ-123 update API reference"`</sub> | <sub>`feature/PROJ-123-*`</sub> | <sub>Developer</sub> |
| <sub>19</sub> | <sub>**Merge**</sub> | <sub>All conditions met: approved, CI green, QA sign-off, docs updated. Squash and merge into develop. The PR is now closed and the work is in develop.</sub> | <sub>*(GitHub/GitLab "Squash and merge" button)*</sub> | <sub>PR → `develop`</sub> | <sub>Developer (or team lead)</sub> |
| <sub>20</sub> | <sub>**Merge**</sub> | <sub>Delete the feature branch. It has served its purpose. Keeping it creates clutter and false signals about active work.</sub> | <sub>`git push origin --delete feature/PROJ-123-*`<br>or auto-deleted by GitHub setting</sub> | <sub>origin</sub> | <sub>Developer (or automation)</sub> |
| <sub>21</sub> | <sub>**Release**</sub> | <sub>When the sprint is complete and develop is stable, a release branch is cut by the team lead or release manager. No new features after this point - hardening only.</sub> | <sub>`git checkout develop`<br>`git checkout -b release/x.y.z`<br>`git push -u origin release/x.y.z`</sub> | <sub>new `release/x.y.z`</sub> | <sub>Team lead / Release manager</sub> |
| <sub>22</sub> | <sub>**Release**</sub> | <sub>QA runs full regression suite on the release branch in staging. Any bugs found are fixed via bugfix branches merging into the release branch (not into develop directly).</sub> | <sub>`git checkout -b bugfix/PROJ-171-description release/x.y.z`</sub> | <sub>`bugfix/*` → `release/x.y.z`</sub> | <sub>QA + Developer</sub> |
| <sub>23</sub> | <sub>**Release**</sub> | <sub>Release signed off by QA, product owner, and security. Merge release branch into main. This triggers the production deployment pipeline.</sub> | <sub>*(PR: `release/x.y.z` → `main`)*</sub> | <sub>`release/x.y.z` → `main`</sub> | <sub>Release manager</sub> |
| <sub>24</sub> | <sub>**Release**</sub> | <sub>Back-merge the release branch into develop to carry any release-branch bug fixes forward. CRITICAL - skipping this step means fixes are lost in the next release.</sub> | <sub>*(PR: `release/x.y.z` → `develop`)*</sub> | <sub>`release/x.y.z` → `develop`</sub> | <sub>Release manager</sub> |
| <sub>25</sub> | <sub>**Release**</sub> | <sub>Tag the release commit on main with the version number.</sub> | <sub>`git tag -a v1.1.0 -m "Release 1.1.0"`<br>`git push origin v1.1.0`</sub> | <sub>`main`</sub> | <sub>Release manager</sub> |

---

### When to Write Documentation

Documentation is part of the definition of done. A feature that works but is not documented is only partially shipped. The table below defines exactly when documentation is required and what form it should take.

> [!IMPORTANT]
> Documentation must be in the **same PR** as the code change. A PR that changes a public API endpoint but leaves the API docs for a follow-up ticket will almost certainly never get its docs written - the follow-up ticket will be deprioritised, the developer will have moved on, and future users will be confused.

| # | Change Type | Documentation Required | Where | When |
|---|------------|----------------------|-------|------|
| <sub>1</sub> | <sub>New public API endpoint or method</sub> | <sub>Full description, parameters, return values, error codes, example request/response</sub> | <sub>API reference docs + README if applicable</sub> | <sub>Same PR as the code</sub> |
| <sub>2</sub> | <sub>Modified API behaviour</sub> | <sub>Update existing docs to reflect the change. Mark deprecated parameters as deprecated.</sub> | <sub>API reference docs</sub> | <sub>Same PR as the code</sub> |
| <sub>3</sub> | <sub>New configuration option or environment variable</sub> | <sub>Name, type, default value, valid values, what it controls</sub> | <sub>Configuration reference docs</sub> | <sub>Same PR as the code</sub> |
| <sub>4</sub> | <sub>Breaking change</sub> | <sub>Migration guide: what broke, what replaces it, step-by-step upgrade instructions</sub> | <sub>CHANGELOG.md + migration guide in docs</sub> | <sub>Same PR as the code</sub> |
| <sub>5</sub> | <sub>New feature with user-visible UI</sub> | <sub>User-facing description, screenshots, usage instructions</sub> | <sub>User guide or feature documentation</sub> | <sub>Same PR as the code</sub> |
| <sub>6</sub> | <sub>Internal refactor (no behaviour change)</sub> | <sub>Update inline code comments if the logic changed. Update architecture docs if structure changed.</sub> | <sub>Code comments + architecture docs</sub> | <sub>Same PR as the code</sub> |
| <sub>7</sub> | <sub>Bug fix</sub> | <sub>Add entry to CHANGELOG.md. If the bug affected documented behaviour, correct the docs.</sub> | <sub>CHANGELOG.md</sub> | <sub>Same PR as the code</sub> |
| <sub>8</sub> | <sub>Internal tooling / CI / build change</sub> | <sub>Update the developer setup guide or contributing guide if the change affects how developers run the project.</sub> | <sub>CONTRIBUTING.md or developer setup docs</sub> | <sub>Same PR as the code</sub> |

---

QA is not a phase that happens after development is finished - it is a continuous presence throughout the sprint. The table below shows when QA participates and what they are doing at each stage.

| # | Sprint Stage | QA Activity | What QA Needs from Dev | Outcome |
|---|------------|------------|----------------------|---------|
| <sub>1</sub> | <sub>**Sprint planning**</sub> | <sub>QA writes or reviews acceptance criteria for each ticket before the sprint starts. Ambiguous acceptance criteria are flagged and resolved before development begins.</sub> | <sub>Access to requirements and design docs</sub> | <sub>Each ticket has clear, testable acceptance criteria</sub> |
| <sub>2</sub> | <sub>**During development**</sub> | <sub>QA authors automated test cases or test plans for the ticket in parallel with development. They do not wait for the code to be finished.</sub> | <sub>Ticket description and acceptance criteria</sub> | <sub>Test plan ready when the PR opens</sub> |
| <sub>3</sub> | <sub>**PR opened**</sub> | <sub>QA is tagged as a reviewer on PRs for their assigned tickets. They verify the PR description explains how to test the change and that test coverage is adequate.</sub> | <sub>PR description with test instructions</sub> | <sub>QA approves test coverage or requests more tests</sub> |
| <sub>4</sub> | <sub>**Branch deployed to QA env**</sub> | <sub>QA deploys the feature branch (or a build from it) to the QA environment and runs manual acceptance tests against the ticket's acceptance criteria.</sub> | <sub>Deployable build from the feature branch</sub> | <sub>PASS: ticket marked ready for merge. FAIL: bugs filed as new tickets.</sub> |
| <sub>5</sub> | <sub>**Release branch cut**</sub> | <sub>QA runs the full regression suite on the release branch in staging. This covers all features in the sprint plus existing functionality.</sub> | <sub>Release branch deployed to staging</sub> | <sub>Release sign-off or list of blocking bugs</sub> |
| <sub>6</sub> | <sub>**Post-release monitoring**</sub> | <sub>QA monitors error rates, performance dashboards, and user reports for the first 24-48 hours after release. Any critical issues trigger a hotfix.</sub> | <sub>Access to production monitoring dashboards</sub> | <sub>Go/no-go for hotfix if needed</sub> |

---

### Peer Code Review - What the Reviewer Is Actually Checking

Code review is not just about catching bugs. A thorough reviewer checks multiple dimensions of quality simultaneously. The table below shows what a reviewer should look for in order of priority. If you are a reviewer, work through this list. If you are an author, review your own PR against this list before assigning reviewers.

> [!TIP]
> Before approving, ask yourself: "If this code went to production tomorrow and caused an incident, would I be comfortable explaining why I approved it?" If the answer is no, request changes.

| # | Review Dimension | What to Check | Common Issues Found Here |
|---|-----------------|--------------|-------------------------|
| <sub>1</sub> | <sub>**Correctness**</sub> | <sub>Does the code do what the ticket says it should do? Does it handle all the acceptance criteria? Are edge cases (empty input, null, max values) handled?</sub> | <sub>Off-by-one errors, missing null checks, incorrect conditional logic, wrong formula</sub> |
| <sub>2</sub> | <sub>**Security**</sub> | <sub>Is user input validated and sanitised? Are there SQL injection, XSS, or command injection risks? Are secrets stored correctly (not in code)? Are permissions checked?</sub> | <sub>Unvalidated input, hardcoded credentials, missing auth checks, insecure deserialization</sub> |
| <sub>3</sub> | <sub>**Test coverage**</sub> | <sub>Are there tests for the new behaviour? Do the tests actually verify the acceptance criteria or just pass trivially? Are failure cases tested?</sub> | <sub>Missing tests for error paths, tests that only test happy path, tests that mock too aggressively</sub> |
| <sub>4</sub> | <sub>**Readability**</sub> | <sub>Can a developer who has never seen this code understand it in 5 minutes? Are names descriptive? Are complex sections commented with WHY (not what)?</sub> | <sub>Single-letter variable names, overly clever one-liners, missing comments on non-obvious logic</sub> |
| <sub>5</sub> | <sub>**Architecture**</sub> | <sub>Does the change fit the existing patterns of the codebase? Is it in the right module/layer? Does it introduce unnecessary coupling or circular dependencies?</sub> | <sub>Logic in the wrong layer, direct database access from a controller, missing abstraction</sub> |
| <sub>6</sub> | <sub>**Performance**</sub> | <sub>Are there any N+1 query problems, unnecessary loops over large datasets, or missing indexes? Will this scale to production data volumes?</sub> | <sub>N+1 queries, loading entire dataset to filter in memory, synchronous calls in hot paths</sub> |
| <sub>7</sub> | <sub>**Error handling**</sub> | <sub>Are failures handled gracefully? Are error messages useful for debugging? Are exceptions caught at the right level and not swallowed silently?</sub> | <sub>Silent catch blocks, generic error messages, exceptions caught too broadly</sub> |
| <sub>8</sub> | <sub>**Documentation**</sub> | <sub>Is the PR description complete? Are public APIs documented? Is CHANGELOG updated? Are inline comments accurate and up to date with the code they describe?</sub> | <sub>Stale comments, missing API docs, no CHANGELOG entry for user-visible changes</sub> |

---

### The Daily Developer Rhythm

Within a sprint, the daily cadence keeps your work integrated with the team and prevents large divergences from building up over multiple days. Following this rhythm means your rebase conflicts are small and your PRs are easy to review because they are focused and timely.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Origin as origin/develop
    participant CI as CI Pipeline
    participant PR as Pull Request

    Note over Dev,PR: Every morning
    Dev->>Origin: git fetch origin
    Dev->>Dev: git rebase origin/develop (on feature branch)
    Note over Dev: Resolve any conflicts immediately while context is fresh

    Note over Dev,PR: During the day
    Dev->>Dev: Write code in small increments
    Dev->>Dev: git add -p (stage only what you intend)
    Dev->>Dev: git commit -m "feat: PROJ-123 specific change"
    Dev->>Dev: Run tests locally after each commit

    Note over Dev,PR: Before end of day
    Dev->>Origin: git push origin feature/PROJ-123
    CI->>PR: Run automated checks on pushed commits
    Dev->>PR: Check CI status - fix any failures before tomorrow

    Note over Dev,PR: When ready for review
    Dev->>Origin: git fetch + git rebase origin/develop
    Dev->>Dev: git diff develop..HEAD (self-review)
    Dev->>PR: Open PR with full description
    Dev->>PR: Assign reviewers
```

---

### Do I Pull Down develop Every Day?

Yes. Every single day, first thing. Here is why this matters at scale.

On a team of ten developers, each person merges at least one PR per day. That means `develop` moves forward by at least ten commits every day. If you go two days without syncing, your branch is twenty commits behind. If you go a week, it is fifty commits behind. The further behind you fall, the larger your rebase conflict surface becomes - you are not just integrating your changes with main, you are integrating with everything your teammates shipped while you were working in isolation.

Small, frequent syncs with `develop` keep conflict surfaces tiny. A daily rebase on a branch that is one commit behind takes ten seconds to resolve. A weekly rebase on a branch that is fifty commits behind can take an hour.

> [!TIP]
> Set a reminder or alias. Some developers run `git fetch && git rebase origin/develop` as the first command every morning before their coffee is finished brewing. Some teams configure their IDE to fetch automatically on startup. Either way, make it a reflex, not a decision.

```bash
# Morning sync alias - add to your .bashrc or .zshrc
alias morning='git fetch origin && git rebase origin/develop'

# Or as a full check:
alias syncup='git fetch origin && echo "Current branch: $(git branch --show-current)" && git rebase origin/develop && echo "Synced. Run your tests."'
```

---

### PR Description Template

A well-written PR description saves reviewer time, creates a permanent record of the decision, and makes the squash commit message on `develop` meaningful. Use this template for every PR.

```markdown
## What
Brief description of what this PR changes. One to three sentences.

## Why
Why is this change needed? Link to the ticket: Closes #PROJ-123

## How to Test
1. Step-by-step instructions to verify the change works
2. Include any test credentials, feature flags, or environment setup needed
3. Describe what the expected output or behaviour is

## Screenshots (if UI change)
[attach before/after screenshots]

## Checklist
- [ ] Tests added or updated
- [ ] Documentation updated (if API or behaviour changed)
- [ ] Self-reviewed the diff line by line
- [ ] Rebased onto latest develop
- [ ] CI is passing
```

> [!NOTE]
> Most teams configure a `PULL_REQUEST_TEMPLATE.md` file in the `.github/` directory of the repository so this template auto-populates whenever a PR is opened. If your team does not have one, create it - it is a five-minute investment that pays back every PR forever.

---

## Architecture Overview

GitSim is built around a single central class, `GitRepo`, which acts as a **pure in-memory state machine**. The state machine holds every piece of information a real Git repository would store on disk inside `.git/`: the commit object graph, branch pointer map, staging index, working tree snapshot, remote tracking references, and pull request objects. Nothing is ever written to disk and no subprocess is ever spawned.

The design is deliberately layered. Low-level repository operations live in `repo.py`. Composed multi-step workflow patterns live in `actions.py`. Narrative explanations and instructor text live in `explain.py`. Terminal formatting utilities live in `utils.py`. The scenario scripts in `scenarios/` orchestrate everything by calling the layers above in the correct sequence. This separation of concerns means each layer can be understood, tested, and replaced independently.

```mermaid
graph TD
    A[run.py - CLI Entry Point] --> B[explain.py - Intro and Outro]
    A --> C[scenarios/]
    C --> D[feature_branch.py - Scenario 1]
    C --> E[merge_conflict.py - Scenario 2]
    C --> F[rebase_example.py - Scenario 3]
    C --> G[bad_practice.py - Scenario 4]
    D & E & F & G --> H[actions.py - Composed Workflow Helpers]
    H --> I[repo.py - GitRepo State Machine CORE]
    I --> J[utils.py - ANSI Output and Formatting]
    style I fill:#1a1a2e,stroke:#4a9eff,color:#fff
    style J fill:#16213e,stroke:#4a9eff,color:#aaa
    style A fill:#0d3b1e,stroke:#2ea043,color:#fff
```

> [!NOTE]
> `repo.py` is the only module with side effects on state. All other modules either read from it (scenarios, actions) or write to stdout (utils, explain). This makes the simulator deterministic and easy to reason about - you can trace any output back to a single `GitRepo` method call.

---

## Commit vs Rebase - Deep Dive

This is one of the most misunderstood distinctions in Git. Both `git commit` and `git rebase` deal with commits and history, but they do fundamentally different things at different stages of the workflow. Confusing the two is the source of many Git disasters on real teams.

### What Is a Commit?

A commit is a permanent, immutable snapshot of your entire tracked file tree at a specific point in time. When you run `git commit`, Git takes everything in the staging index, wraps it in a commit object with your message, author, timestamp, and a pointer to the parent commit, computes a SHA hash of all that data, and stores it permanently in the object database. The commit hash is derived from the content - if any byte changes, the hash changes. This is why commits are immutable: you cannot edit a commit without producing a new object with a different hash.

In GitSim, `repo.commit(message)` does exactly this: it creates a `Commit` dataclass with a random 7-character hex hash, a reference to the current HEAD as parent, a deep copy of the staged files as the tree snapshot, and advances the current branch pointer to the new hash. The commit is stored in `_commits[hash]` for O(1) retrieval.

**What exactly is stored inside one commit object:**

```mermaid
block-beta
  columns 3

  block:COMMIT["📦 Commit Object  a3f9c2b"]:3
    columns 3
    H["🔑 hash\na3f9c2b"] M["💬 message\nfeat: add storm endpoint"] A["👤 author\nAlice"]
    T["🕐 timestamp\n2024-01-01T09:00"] P["⬅️ parent\nb7e2f1a"] B["🌿 branch\nfeature/PROJ-142"]
    space:3
    TREE["🌲 tree snapshot — full copy of every tracked file at this moment"]:3
  end

  space:3

  block:PARENT["📦 Parent Commit  b7e2f1a"]:3
    columns 3
    PH["🔑 hash\nb7e2f1a"] PM["💬 message\nchore: bootstrap"] PA["👤 author\nAlice"]
    PT["🕐 timestamp\n2024-01-01T08:00"] PP["⬅️ parent\n(root - none)"] PB["🌿 branch\nmain"]
  end

  COMMIT-- "parent pointer" -->PARENT
```

> [!NOTE]
> The **parent pointer** is what makes commits form a chain. Every commit knows its parent. By following parent pointers backward from any branch tip you reconstruct the entire history of that branch. This chain is the Git commit graph (DAG).

Rebase is the operation of replaying a sequence of commits onto a different base commit. When you run `git rebase main` on a feature branch, Git finds the point where your branch diverged from main, takes every commit you made since that divergence, and re-applies each one on top of the current tip of main - one at a time, in order. Each replayed commit gets a brand-new hash because its parent has changed. The old commits are not deleted immediately, but they are no longer reachable from any branch pointer, so they eventually get garbage collected.

In GitSim, `repo.rebase(onto)` deep-copies each commit in the current branch that is not in the target branch, assigns new hashes to each one, rewires the parent pointers to form a linear chain starting from the tip of the target branch, and updates the current branch pointer to the new tip. This correctly shows that rebase rewrites history - the commits look the same but they have different hashes.

**Before rebase — diverged history (the problem):**

```mermaid
gitGraph LR:
   commit id: "A"
   commit id: "B  ← branch point"
   branch feature/my-work
   commit id: "C  feat: first change"
   commit id: "D  feat: second change"
   checkout main
   commit id: "E  teammate merged"
   commit id: "F  teammate merged"
```

**After `git rebase main` — linear history (the goal):**

```mermaid
gitGraph LR:
   commit id: "A"
   commit id: "B"
   commit id: "E  teammate merged"
   commit id: "F  teammate merged"
   branch feature/my-work
   commit id: "C' NEW HASH — replayed"
   commit id: "D' NEW HASH — replayed"
```

> [!WARNING]
> Notice that `C` became `C'` and `D` became `D'` — **these are brand new commit objects with different hashes** even though the code change inside them is identical. This is why `git push --force-with-lease` is required after a rebase: the remote still has the old `C` and `D` objects. A regular push would be rejected because the histories have diverged.

| # | Dimension | `git commit` | `git rebase` |
|---|-----------|-------------|-------------|
| <sub>1</sub> | <sub>**What it does**</sub> | <sub>Creates a new permanent snapshot and appends it to the current branch</sub> | <sub>Replays existing commits onto a new base, creating new commit objects with new hashes</sub> |
| <sub>2</sub> | <sub>**When to use**</sub> | <sub>Any time you have staged changes you want to save as a named point in history</sub> | <sub>Before pushing, to bring your branch up to date with main without a merge commit</sub> |
| <sub>3</sub> | <sub>**Rewrites history?**</sub> | <sub>No - it only adds to history</sub> | <sub>Yes - all rebased commits get new SHA hashes</sub> |
| <sub>4</sub> | <sub>**Safe on shared branches?**</sub> | <sub>Yes - always safe</sub> | <sub>No - never rebase a branch others have checked out</sub> |
| <sub>5</sub> | <sub>**Produces a merge commit?**</sub> | <sub>No (unless it is a merge commit itself)</sub> | <sub>No - rebase produces a linear history with no merge commits</sub> |
| <sub>6</sub> | <sub>**Conflict possible?**</sub> | <sub>Only if staging conflicting changes (rare)</sub> | <sub>Yes - each replayed commit can conflict with the new base one at a time</sub> |
| <sub>7</sub> | <sub>**Affects other branches?**</sub> | <sub>No - only the current branch pointer moves</sub> | <sub>Only the current branch is rewritten; target branch is untouched</sub> |
| <sub>8</sub> | <sub>**GitSim method**</sub> | <sub>`repo.commit(message)`</sub> | <sub>`repo.rebase(onto)`</sub> |

### The Rebase vs Merge Decision

When you need to integrate changes from main into your feature branch, you have two choices: `git merge main` or `git rebase main`. Both get your branch up to date. The difference is entirely in the shape of the resulting history.

Merge creates a new merge commit with two parents, preserving the exact history of how and when branches diverged. This is honest but can make `git log --graph` hard to read on busy projects. Rebase replays your commits on top of main, producing a straight line as if you had started your branch from the latest main all along. This produces a cleaner history but rewrites your commits.

> [!TIP]
> The widely-accepted professional rule is: **rebase your own feature branches onto main before pushing or opening a PR, merge (or squash merge) when integrating a completed feature back into main**. Never rebase main onto your feature branch - always rebase your feature branch onto main.

---

## Never Commit Directly to Main

The `main` branch (sometimes called `master` in older repositories) represents the production-ready, always-deployable state of your codebase. It is the source of truth. Every commit on main should be a complete, reviewed, tested feature or fix - never a half-finished change, a debug statement, or a quick experiment.

Committing directly to main bypasses every quality control your team has in place: code review, automated tests, linting, security scans. A single bad direct commit to main can break a production deployment, corrupt shared state that your teammates have already built upon, or introduce a security vulnerability that bypasses your PR-based audit trail. In GitSim, Scenario 4 demonstrates this explicitly with `[WARNING]` output every time a direct-to-main commit is made, and then shows the correct branch-based alternative immediately after.

> [!IMPORTANT]
> Most professional teams enforce branch protection rules on `main` at the repository level (GitHub branch protection, GitLab protected branches). These rules prevent direct pushes, require pull request reviews, and require CI checks to pass before a merge is allowed. GitSim simulates the workflow you would follow under these rules even though it cannot enforce them - the bad-practice scenario shows what happens when those rules are not enforced or bypassed.

### Why Direct Commits to Main Are Dangerous

| # | Risk | What Happens | How Branches Prevent It |
|---|------|-------------|------------------------|
| <sub>1</sub> | <sub>**No review**</sub> | <sub>No second pair of eyes on the change. Bugs, security holes, and logic errors go undetected.</sub> | <sub>PR-based flow requires at least one approval before merging.</sub> |
| <sub>2</sub> | <sub>**No CI gate**</sub> | <sub>Tests are not run. Broken code reaches the shared branch immediately.</sub> | <sub>PRs trigger CI pipelines. Merge is blocked until all checks pass.</sub> |
| <sub>3</sub> | <sub>**Broken shared state**</sub> | <sub>Teammates who pull main now get broken code and cannot continue working.</sub> | <sub>Feature branches isolate work-in-progress. Main stays stable.</sub> |
| <sub>4</sub> | <sub>**No revert path**</sub> | <sub>Reverting a direct commit may be complicated by subsequent commits from teammates.</sub> | <sub>A merged PR can be reverted cleanly as a single unit.</sub> |
| <sub>5</sub> | <sub>**Audit trail loss**</sub> | <sub>No PR means no record of the discussion, the rationale, or the reviewers who approved it.</sub> | <sub>PRs create a permanent, searchable record of every change decision.</sub> |
| <sub>6</sub> | <sub>**Deployment risk**</sub> | <sub>In CD pipelines, a push to main may trigger an immediate production deployment.</sub> | <sub>PRs let you control exactly when and what reaches main.</sub> |

---

## Syncing Before You Push - Why It Matters

Before you push your feature branch to the remote and open a pull request, you must always sync your branch with the latest state of main. This means running `git fetch` followed by `git rebase origin/main` (or the equivalent in GitSim: `repo.fetch()` then `repo.rebase("main")`). Skipping this step is one of the most common sources of rejected pushes, messy merge commits, and avoidable conflicts in professional teams.

### Why Fetch First, Then Rebase?

`git fetch` downloads the latest commit objects and branch pointers from the remote without modifying any of your local branches. It updates the remote-tracking references (`origin/main`, `origin/feature/X`) so your local Git knows what the remote looks like right now. It does not touch your working tree or your local branches. `git rebase origin/main` then takes those downloaded commits and replays your feature branch commits on top of them.

This two-step sequence is important because it separates the network operation (fetch) from the local history rewrite (rebase). Running `git pull --rebase` combines both steps but offers less visibility. In GitSim, `demonstrate_sync_before_commit` in `actions.py` shows this two-step pattern explicitly with a printed explanation at each step.

> [!IMPORTANT]
> **You must sync before opening a PR, not just before pushing.** If you push your branch and then main moves forward before your PR is reviewed, your PR will show as diverged and the reviewer may ask you to rebase before merging. Building the sync habit before every push means your PRs are always based on the latest main.

### Do You Need to Sync Before Every Commit?

No. You commit frequently on your own feature branch to save progress. Syncing (fetch + rebase onto main) is done before you push your branch to the remote or before you open a PR. The workflow is:

```
branch -> commit -> commit -> commit -> SYNC -> push -> open PR
                                       ^
                                       fetch + rebase here, not before each commit
```

> [!TIP]
> If your team uses long-lived feature branches (more than a day or two), consider syncing with main once a day to reduce the size of eventual rebase conflicts. Small, frequent syncs are much easier to resolve than one large sync after two weeks of divergence.

### Sync Before Rebase or After?

The question "should I sync before I rebase?" is circular - syncing IS the rebase. The correct sequence is:

1. `git fetch` - update remote-tracking refs
2. `git rebase origin/main` - replay your commits on top of the freshly fetched main
3. Resolve any conflicts that arise during the replay
4. `git push --force-with-lease` - push the rewritten branch

There is no separate "sync" step that comes before this - fetch + rebase together constitute the sync. What you should NOT do is run `git rebase origin/main` without first running `git fetch`, because `origin/main` might be stale and you would be rebasing onto an outdated base.

---

## Git History and Diffs - Auto vs Manual?

### What Is Git History?

Git history is the directed acyclic graph (DAG) of commit objects, connected by parent pointers. Every commit points to one parent (or two, for merge commits). The history of a branch is the chain of commits reachable by following parent pointers backward from the branch tip. `git log` traverses this graph and displays it. `git log --graph` renders it as an ASCII tree.

In GitSim, `repo.log()` traverses `_commits` by following parent pointers from each branch tip and renders an ASCII graph with branch labels. The commit objects in `_commits` form the same DAG structure as real Git's object store.

### What Is a Diff?

A diff is the computed difference between two versions of a file or two commits. Git stores complete snapshots in each commit - it does not store deltas. When you ask for a diff, Git computes it on the fly by comparing the file contents of two tree objects. The diff algorithm Git uses is a variant of the **Myers diff algorithm**, which finds the shortest edit script (minimum number of insertions and deletions) that transforms one version into another.

### Auto vs Manual: The Real Question

The distinction between "automatic" and "manual" in Git contexts usually refers to conflict resolution during merges and rebases.

| # | Scenario | Auto or Manual | What Git Does | What You Must Do |
|---|----------|---------------|--------------|-----------------|
| <sub>1</sub> | <sub>**Clean merge**</sub> | <sub>Automatic</sub> | <sub>Git merges files that were changed in non-overlapping locations without any human input</sub> | <sub>Nothing - the merge completes automatically</sub> |
| <sub>2</sub> | <sub>**Conflicting merge**</sub> | <sub>Manual</sub> | <sub>Git writes conflict markers into the file and stops, waiting for human resolution</sub> | <sub>Open the file, edit it to the correct final state, run `git add`, then `git commit`</sub> |
| <sub>3</sub> | <sub>**Clean rebase**</sub> | <sub>Automatic</sub> | <sub>Each commit is replayed cleanly onto the new base with no intervention needed</sub> | <sub>Nothing - the rebase completes automatically</sub> |
| <sub>4</sub> | <sub>**Conflicting rebase**</sub> | <sub>Manual</sub> | <sub>Git stops at the conflicting commit, writes markers, and waits</sub> | <sub>Resolve the conflict, `git add`, then `git rebase --continue`</sub> |
| <sub>5</sub> | <sub>**Diff generation**</sub> | <sub>Automatic (Myers algorithm)</sub> | <sub>Git computes the shortest edit script between two trees</sub> | <sub>Nothing - diffs are always computed automatically on request</sub> |
| <sub>6</sub> | <sub>**Interactive rebase squash**</sub> | <sub>Manual (you direct it)</sub> | <sub>Git opens an editor showing commits; you mark which to squash, reword, or drop</sub> | <sub>Edit the rebase-todo list to mark commits as `squash` or `fixup`, save and exit</sub> |

GitSim demonstrates both automatic and manual resolution. In Scenario 2, `conflict_block()` renders the markers visually, and then `repo.resolve_conflict()` shows the manual resolution step. In Scenario 3, the rebase happens cleanly (automatic) and then an interactive squash is demonstrated (manual direction).

> [!NOTE]
> GitSim's `diff_block()` in `utils.py` uses a simplified before/after line comparison rather than the full Myers algorithm. The Myers algorithm minimises the edit distance by finding the longest common subsequence between two sequences of lines. For training purposes, the simplified render communicates the concept of a diff perfectly well - the exact edit-distance minimisation is a detail that does not affect learning outcomes.

---

## Types of Merging

Git offers several distinct merge strategies, and choosing the right one shapes the readability and integrity of your project history. GitSim demonstrates the three most important ones. Understanding the differences between them is essential for any developer working on a team.

### 1. Regular (True) Merge

A regular merge, sometimes called a true merge or a recursive merge, takes the two branch tips and their common ancestor commit and produces a new merge commit with two parent pointers. The merge commit represents the integration of both lines of work. The history graph will show a visible fork and rejoin, honestly reflecting that two parallel development streams existed and were combined.

This approach is useful when you want to preserve the complete history of when branches diverged and were integrated. In open source projects with many contributors, a merge-heavy history can make it clear exactly which set of commits constitute a particular feature or fix.

### 2. Squash Merge

A squash merge takes all the commits on a feature branch and combines their changes into a single new commit on the target branch. The new commit has only one parent (the tip of the target branch before the merge), so no visible fork appears in the history. The feature branch's intermediate commits - all the WIP saves, "fix typo", "try again", "add missing semicolon" commits - are collapsed into one clean, meaningful commit.

GitSim implements squash merge in `repo.merge_pr(pr, squash=True)`. The entire diff of the feature branch versus main is captured and applied as a single commit. This is the default merge strategy for pull requests in many professional teams because it keeps the main branch history flat and readable.

### 3. Rebase and Merge (Fast-Forward)

In a rebase-then-merge workflow, the feature branch is first rebased onto main (linearising its history), and then merged with a fast-forward. A fast-forward merge simply moves the target branch pointer forward to the tip of the source branch without creating a merge commit. This is possible only when the target branch is a direct ancestor of the source branch - which is guaranteed after a clean rebase.

The result is a perfectly linear history where each feature commit appears directly on main as if it had always been there. This is the cleanest possible history but requires that every developer rebase before merging, and it can make it harder to identify which commits belong to which feature.

> [!TIP]
> Most teams pick one merge strategy and enforce it consistently. Mixing strategies on the same repository creates a confusing history. GitSim uses squash merge as the default for PRs because it produces the cleanest educational output - one commit on main per feature, each with a descriptive message.

### Merge Strategy Comparison

| # | Strategy | Creates Merge Commit? | History Shape | Preserves Feature Commits? | Best For |
|---|----------|--------------------|--------------|--------------------------|---------|
| <sub>1</sub> | <sub>**Regular merge**</sub> | <sub>Yes - merge commit with two parents</sub> | <sub>Non-linear, fork-and-rejoin visible in graph</sub> | <sub>Yes - all feature commits visible</sub> | <sub>Long-lived branches, open source, audit trails</sub> |
| <sub>2</sub> | <sub>**Squash merge**</sub> | <sub>No - single new commit on target</sub> | <sub>Linear - no fork visible</sub> | <sub>No - all feature commits collapsed to one</sub> | <sub>Short-lived feature branches, clean main history</sub> |
| <sub>3</sub> | <sub>**Rebase + fast-forward**</sub> | <sub>No - branch pointer moves forward</sub> | <sub>Perfectly linear</sub> | <sub>Yes but with rewritten hashes</sub> | <sub>Teams that want linear history and are disciplined about rebasing</sub> |
| <sub>4</sub> | <sub>**Cherry-pick**</sub> | <sub>No - selected commits replayed individually</sub> | <sub>Depends on usage</sub> | <sub>Selected commits only, with new hashes</sub> | <sub>Hotfixes, backports, selective integration</sub> |

The diagram below shows how the same feature branch history looks under each merge strategy when integrated back into main.

```mermaid
gitGraph
   commit id: "A - initial"
   commit id: "B - setup"
   branch feature
   commit id: "C - wip"
   commit id: "D - fix"
   commit id: "E - done"
   checkout main
   commit id: "F - hotfix"
   merge feature id: "G - merge commit" type: HIGHLIGHT
```

> The diagram above shows a regular merge. With squash merge, commits C, D, E would become a single commit on main. With rebase+FF, C, D, E would be replayed after F with new hashes and no merge commit.

---

## The PullRequest Object

The `PullRequest` dataclass in GitSim is a first-class simulation of the PR lifecycle on platforms like GitHub and GitLab. It is not just a label - it carries the full state of a real PR review cycle, including the diff context, the reviewer list, the comment thread, the approval status, and the merge result. Understanding each field and what it represents in a real platform helps developers navigate PRs confidently in production environments.

### What a PR Actually Is

A pull request is a formal request to integrate the changes from one branch (the source or head branch) into another (the target or base branch, usually main). It is a collaboration tool as much as a merge tool. The PR interface on GitHub shows the diff between the two branches, lets reviewers leave line-by-line comments, tracks which changes have been addressed, records approvals and rejections, runs CI checks, and ultimately performs the merge. The PR is also a permanent record - even after it is merged and the branch is deleted, the PR discussion, comments, and review decisions remain searchable in the repository's history.

> [!NOTE]
> In GitSim, `repo.open_pr(title, reviewers)` creates a `PullRequest` object and stores it in `repo._prs`. The `PullRequest` carries enough state to simulate the full lifecycle: creation with a title and reviewer list, review comments and change requests, approval, and squash merge into main. The object is returned so scenarios can hold a reference to it and pass it to `review_pr` and `merge_pr`.

### The PullRequest Object Fields

| # | Field | Type | Real Git/GitHub Equivalent | What GitSim Does With It |
|---|-------|------|--------------------------|-------------------------|
| <sub>1</sub> | <sub>`number`</sub> | <sub>`int`</sub> | <sub>The sequential PR number shown as `#42` in GitHub URLs and references</sub> | <sub>Auto-incremented from `_pr_counter` on each `open_pr` call</sub> |
| <sub>2</sub> | <sub>`title`</sub> | <sub>`str`</sub> | <sub>The PR title shown in the PR list and notifications</sub> | <sub>Printed in the `[PR]` step line when the PR is opened</sub> |
| <sub>3</sub> | <sub>`source`</sub> | <sub>`str`</sub> | <sub>The head branch - the branch containing the changes to be merged</sub> | <sub>Set to the current branch name when `open_pr` is called</sub> |
| <sub>4</sub> | <sub>`target`</sub> | <sub>`str`</sub> | <sub>The base branch - usually `main` - that the changes will be merged into</sub> | <sub>Always `"main"` in the simulator; configurable in a real repo</sub> |
| <sub>5</sub> | <sub>`author`</sub> | <sub>`str`</sub> | <sub>The GitHub user who opened the PR</sub> | <sub>Set from `repo.author` at the time `open_pr` is called</sub> |
| <sub>6</sub> | <sub>`reviewers`</sub> | <sub>`list[str]`</sub> | <sub>The list of requested reviewers - people tagged to review the PR</sub> | <sub>Passed directly to `open_pr`; printed in the PR summary line</sub> |
| <sub>7</sub> | <sub>`approved`</sub> | <sub>`bool`</sub> | <sub>Whether the required number of approvals has been reached</sub> | <sub>Set to `True` by `review_pr` when `approve=True` is passed</sub> |
| <sub>8</sub> | <sub>`comments`</sub> | <sub>`list[str]`</sub> | <sub>The review comment thread - all inline and general review comments</sub> | <sub>Appended to by each `review_pr` call; printed in the review summary</sub> |
| <sub>9</sub> | <sub>`merged`</sub> | <sub>`bool`</sub> | <sub>Whether the PR has been merged and closed</sub> | <sub>Set to `True` by `merge_pr`; prevents double-merge</sub> |

### The PR Lifecycle in GitSim

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Repo as GitRepo State
    participant PR as PullRequest Object
    participant Rev as Reviewer

    Dev->>Repo: checkout_new("feature/x")
    Note over Repo: _current = "feature/x"
    Dev->>Repo: write(file, content)
    Note over Repo: _working[file] = content, diff shown
    Dev->>Repo: stage_patch(file)
    Note over Repo: _staged[file] = content
    Dev->>Repo: commit("feat: add X")
    Note over Repo: new Commit hash stored in _commits
    Dev->>Repo: fetch() then rebase("main")
    Note over Repo: commits replayed with new hashes
    Dev->>Repo: push()
    Note over Repo: _remotes["origin"]["feature/x"] updated
    Dev->>PR: open_pr(title, reviewers=["Alice"])
    Note over PR: number=1, source="feature/x", approved=False, merged=False
    PR->>Rev: [PR] Opened PR number 1 - review requested
    Rev->>PR: review_pr(comment="Needs tests", approve=False)
    Note over PR: comments.append("Needs tests")
    Dev->>Repo: write(file, fixed_content)
    Dev->>Repo: commit("test: add unit tests")
    Rev->>PR: review_pr(comment="LGTM", approve=True)
    Note over PR: approved=True
    PR->>Repo: merge_pr(squash=True)
    Note over Repo: feature commits squashed to main, merged=True
    Repo->>Repo: branch cleanup
```

### What the Simulator Shows at Each PR Stage

| # | PR Stage | What GitSim Prints | What You Learn |
|---|----------|-------------------|---------------|
| <sub>1</sub> | <sub>**PR Created**</sub> | <sub>`[PR] Opened Pull Request #1: "feat: add X"` with source/target branch names and reviewer list</sub> | <sub>A PR is a named, numbered request to merge a specific branch. The title should match the feature's purpose.</sub> |
| <sub>2</sub> | <sub>**Diff shown**</sub> | <sub>The `diff_block()` output showing red removed lines and green added lines from the feature branch</sub> | <sub>Reviewers see exactly what changed. The diff is computed between the feature branch tip and the merge-base with main.</sub> |
| <sub>3</sub> | <sub>**Reviewers listed**</sub> | <sub>`[REVIEW] Review requested from: Alice, Bob` with each reviewer's name</sub> | <sub>Assigning reviewers notifies them and makes them responsible for checking the code before it reaches main.</sub> |
| <sub>4</sub> | <sub>**Comment added**</sub> | <sub>`[REVIEW] Alice commented: "This function needs error handling for null input"`</sub> | <sub>Review comments create a conversation thread. The author must address each comment before approval.</sub> |
| <sub>5</sub> | <sub>**Change requested**</sub> | <sub>`[REVIEW] Alice REQUESTED CHANGES on PR #1` with the comment reason</sub> | <sub>A change request blocks the PR from being merged until the author pushes a fix and the reviewer re-approves.</sub> |
| <sub>6</sub> | <sub>**Approval granted**</sub> | <sub>`[REVIEW] Alice APPROVED PR #1` - `pr.approved` set to `True`</sub> | <sub>Approval means the reviewer has verified the changes are correct and ready. Most teams require at least one approval.</sub> |
| <sub>7</sub> | <sub>**Merged to main**</sub> | <sub>`[MERGE] Squash merge: feature/x -> main [newHash]` - feature commits collapsed, main pointer advanced</sub> | <sub>The merge integrates the changes. With squash, all feature commits become one clean commit on main.</sub> |

---

## Module Reference

Each module has a distinct, non-overlapping responsibility. This separation of concerns keeps each file independently testable and replaceable.

| # | Module | Responsibility | Key Exports |
|---|--------|---------------|-------------|
| <sub>1</sub> | <sub>`repo.py`</sub> | <sub>Core state machine - all Git semantics live here. Maintains branches, commits, index, working tree, remotes, and PRs. Single source of truth for repo state.</sub> | <sub>`GitRepo`, `Commit`, `Branch`, `PullRequest`</sub> |
| <sub>2</sub> | <sub>`actions.py`</sub> | <sub>Composed multi-step workflow helpers. Chains repo operations into named patterns that represent complete professional workflows.</sub> | <sub>`full_feature_cycle`, `demonstrate_stash_workflow`, `demonstrate_sync_before_commit`</sub> |
| <sub>3</sub> | <sub>`explain.py`</sub> | <sub>High-level narrative text - the instructor voice. Prints section banners and summary paragraphs between simulation steps.</sub> | <sub>`intro`, `outro`, `section`, `scenario_intro`</sub> |
| <sub>4</sub> | <sub>`utils.py`</sub> | <sub>All terminal output primitives: ANSI colour constants, diff rendering, conflict block display, ASCII log graph, hash generation, fake clock.</sub> | <sub>`step`, `explain`, `diff_block`, `conflict_block`, `log_graph`, `make_hash`, `banner`, `warning`, `success`</sub> |
| <sub>5</sub> | <sub>`run.py`</sub> | <sub>CLI entry point. Parses `--scenario` flag, instantiates a fresh `GitRepo` per scenario, calls `intro` and `outro`.</sub> | <sub>`main`, `parse_args`</sub> |
| <sub>6</sub> | <sub>`scenarios/feature_branch.py`</sub> | <sub>Scenario 1 - full feature lifecycle from branch creation through squash-merged PR.</sub> | <sub>`run(repo)`</sub> |
| <sub>7</sub> | <sub>`scenarios/merge_conflict.py`</sub> | <sub>Scenario 2 - intentional conflict creation, visual marker rendering, manual resolution.</sub> | <sub>`run(repo)`</sub> |
| <sub>8</sub> | <sub>`scenarios/rebase_example.py`</sub> | <sub>Scenario 3 - standard rebase, interactive squash, force-push demonstration.</sub> | <sub>`run(repo)`</sub> |
| <sub>9</sub> | <sub>`scenarios/bad_practice.py`</sub> | <sub>Scenario 4 - anti-patterns with explicit warnings and correct alternatives shown inline.</sub> | <sub>`run(repo)`</sub> || <sub>10</sub> | <sub>`scenarios/branching_strategy.py`</sub> | <sub>Scenario 5 script - full corporate branch hierarchy: `main`, `develop`, `release/x.y.z`, `feature/PROJ-*`, `bugfix/PROJ-*`, `test/sprint-*`, `hotfix/PROJ-*` with ticket-ID naming and correct merge targets.</sub> | <sub>`run(repo)`</sub> |
---

## Data Structures

GitSim uses four Python dataclasses to model Git's core objects. These map closely to the actual objects Git stores in `.git/objects`, making the simulator an accurate mental model of real Git internals rather than an abstraction.

### Commit Object

A `Commit` is an immutable snapshot. Once created it is never mutated. This mirrors how real Git commits are content-addressed and permanently immutable once written to the object store. In real Git, the hash IS the content - changing a single character in the message, author, or file tree produces a completely different hash. GitSim simulates this immutability by never modifying an existing `Commit` object.

**How a SHA hash is computed and what it protects:**

```mermaid
flowchart LR
    subgraph INPUT ["🔢 Hash Inputs — every byte matters"]
        direction TB
        I1["tree SHA\n(all file contents)"]
        I2["parent SHA\n(previous commit)"]
        I3["author + email\n+ timestamp"]
        I4["commit message"]
    end

    subgraph HASH ["⚙️ SHA-1 / SHA-256 function"]
        direction TB
        F1["deterministic\none-way function"]
        F2["same inputs\n= same hash\nalways"]
        F3["1-bit change in input\n= completely\ndifferent hash"]
    end

    subgraph OUTPUT ["🔑 Output — the commit hash"]
        direction TB
        O1["a3f9c2b4e1d8f7...\n(40 hex chars / 160 bits)"]
        O2["shown short as\na3f9c2b (7 chars)"]
    end

    subgraph PROTECTS ["🛡️ What the hash prevents"]
        direction TB
        P1["✅ Tamper detection\nEdit one byte → hash mismatch → Git rejects it"]
        P2["✅ Silent corruption\nNetwork corruption changes bytes → caught immediately"]
        P3["✅ History rewriting\nYou cannot edit old commits without changing all\nchild hashes downstream — the whole chain breaks"]
    end

    INPUT --> HASH --> OUTPUT --> PROTECTS
```

**When and how you create a hash:**

| # | When | Command | What Gets Hashed | Result |
|---|------|---------|-----------------|--------|
| <sub>1</sub> | <sub>Every `git commit`</sub> | <sub>`git commit -m "msg"`</sub> | <sub>Tree (file snapshot) + parent hash + author + timestamp + message</sub> | <sub>New unique commit hash like `a3f9c2b`</sub> |
| <sub>2</sub> | <sub>Every `git add`</sub> | <sub>`git add file.py`</sub> | <sub>File content only</sub> | <sub>Blob hash stored in the index — deduplicates identical files across commits</sub> |
| <sub>3</sub> | <sub>Every `git rebase`</sub> | <sub>`git rebase origin/main`</sub> | <sub>Same content as original commit but with a new parent hash</sub> | <sub>Brand-new commit hash — this is why rebase "rewrites history"</sub> |
| <sub>4</sub> | <sub>Every `git tag -a`</sub> | <sub>`git tag -a v1.0.0 -m "release"`</sub> | <sub>Tag object (name + message + tagger + target commit hash)</sub> | <sub>Tag hash — permanent pointer to a specific commit</sub> |

> [!NOTE]
> You never manually create or manage hashes. Git computes them automatically every time an object is stored. The only time you interact with hashes directly is when you reference a specific commit (e.g., `git checkout a3f9c2b` or `git revert a3f9c2b`). Even then you only need the first 7 characters — Git finds the full hash from those as long as it is unambiguous.

| # | Field | Type | Description |
|---|-------|------|-------------|
| <sub>1</sub> | <sub>`hash`</sub> | <sub>`str`</sub> | <sub>7-character random hex string simulating a Git short hash. Real Git uses SHA-1 (40 hex chars) or SHA-256 (64 hex chars) of the serialised commit object content.</sub> |
| <sub>2</sub> | <sub>`message`</sub> | <sub>`str`</sub> | <sub>The commit message. Conventionally follows Conventional Commits format: `type(scope): description`. Should explain WHY the change was made, not what files changed.</sub> |
| <sub>3</sub> | <sub>`author`</sub> | <sub>`str`</sub> | <sub>Author name. In real Git this is `user.name` and `user.email` from git config, recorded as both author (who wrote the code) and committer (who applied the commit, which can differ on rebased commits).</sub> |
| <sub>4</sub> | <sub>`branch`</sub> | <sub>`str`</sub> | <sub>The branch the commit was created on. Informational only - in real Git, commits do not belong to branches; branches are pointers that reference commits.</sub> |
| <sub>5</sub> | <sub>`files`</sub> | <sub>`dict[str, str]`</sub> | <sub>Full snapshot of all tracked files at commit time. Equivalent to the tree object in real Git. Stored as a deep copy so later working-tree changes do not mutate historical snapshots.</sub> |
| <sub>6</sub> | <sub>`parent`</sub> | <sub>`Optional[str]`</sub> | <sub>Hash of the parent commit. `None` only for the root commit. A real merge commit would have two parents stored as a list; GitSim models single-parent commits for simplicity.</sub> |
| <sub>7</sub> | <sub>`ts`</sub> | <sub>`str`</sub> | <sub>ISO-8601 timestamp generated by the fake monotonic clock. Ensures commits always show sensible chronological ordering in `git log` output regardless of execution speed.</sub> |

### Supporting Structures

| # | Structure | Fields | Purpose in GitSim | Real Git Equivalent |
|---|-----------|--------|------------------|-------------------|
| <sub>1</sub> | <sub>`Branch`</sub> | <sub>`name`, `head` (hash), `upstream`</sub> | <sub>A named pointer to the tip commit. Moving a branch is O(1) - just update the hash string. Branches are not copies of files.</sub> | <sub>`.git/refs/heads/<name>` - a file containing a 40-char SHA</sub> |
| <sub>2</sub> | <sub>`PullRequest`</sub> | <sub>`number`, `title`, `source`, `target`, `author`, `reviewers`, `approved`, `comments`, `merged`</sub> | <sub>Full PR lifecycle state. Tracks the complete review cycle from creation to merge.</sub> | <sub>GitHub/GitLab PR/MR object (not in Git itself - a platform layer on top)</sub> |
| <sub>3</sub> | <sub>`_commits: dict[hash, Commit]`</sub> | <sub>-</sub> | <sub>The commit object store. O(1) lookup by hash. Commits are never removed (simulates pack files).</sub> | <sub>`.git/objects/` - pack files keyed by SHA</sub> |
| <sub>4</sub> | <sub>`_staged: dict[filename, content]`</sub> | <sub>-</sub> | <sub>The staging index. Contains files ready to be included in the next commit snapshot.</sub> | <sub>`.git/index` - binary file tracking staged content</sub> |
| <sub>5</sub> | <sub>`_working: dict[filename, content]`</sub> | <sub>-</sub> | <sub>The working tree. Represents files as they currently appear on disk. Dirty when different from `_tracked`.</sub> | <sub>Actual files on disk in the project directory</sub> |
| <sub>6</sub> | <sub>`_remotes: dict[remote, dict[branch, hash]]`</sub> | <sub>-</sub> | <sub>Remote tracking references. Updated on `fetch()`. Never modified by local commits.</sub> | <sub>`.git/refs/remotes/origin/*`</sub> |

---

## State Machine Flow

The following diagram shows how a file moves through the four zones of a Git repository. Understanding these four zones is the single most important mental model for working with Git effectively. Most Git confusion - lost changes, unexpected diffs, confusing status output - comes from not knowing which zone a change is currently in.

```mermaid
stateDiagram-v2
    [*] --> WorkingTree : write() - edit file in editor
    WorkingTree --> StagingIndex : stage_patch() - git add -p
    StagingIndex --> WorkingTree : unstage - git restore --staged
    StagingIndex --> CommitHistory : commit() - git commit -m
    CommitHistory --> WorkingTree : checkout() - switch branch restores snapshot
    WorkingTree --> StashStack : stash() - git stash push
    StashStack --> WorkingTree : stash_pop() - git stash pop
    CommitHistory --> CommitHistory : rebase() - replay commits with new hashes
    CommitHistory --> Remote : push() - git push origin branch
    Remote --> CommitHistory : fetch() updates tracking refs then rebase()
```

> [!NOTE]
> The staging index (also called the index or cache) is what makes Git uniquely powerful compared to simpler version control systems. It lets you craft commits that contain exactly the right set of changes - no more, no less - even when your working tree contains multiple unrelated edits in progress. `git add -p` is the command that makes this practical.

---

## Conflict Resolution Flow

```mermaid
flowchart TD
    A["Two branches modify the same line of the same file"] --> B{"git merge or git rebase"}
    B --> C["Git detects overlapping changes"]
    C --> D["Conflict markers written into the file and merge/rebase pauses"]
    D --> E["Developer opens the conflicted file in editor"]
    E --> F{"What is the correct resolution?"}
    F -->|"Keep our version only"| G["Remove markers, keep HEAD block, delete incoming block"]
    F -->|"Keep their version only"| H["Remove markers, delete HEAD block, keep incoming block"]
    F -->|"Combine intelligently"| I["Write the correct merged logic, remove all marker lines"]
    G & H & I --> J["git add the resolved file to staging"]
    J --> K{"What operation caused the conflict?"}
    K -->|"git merge"| L["git commit - creates merge commit with two parents"]
    K -->|"git rebase"| M["git rebase --continue - replays the next commit"]
    L & M --> N["History continues cleanly from resolved state"]
```

> [!WARNING]
> Never commit conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) into the repository. Git will happily commit a file that still contains these markers because it cannot distinguish intentional marker content from an accidental leftover. Always verify the resolved file looks syntactically and logically correct before staging it. Run your tests after resolving conflicts and before pushing.

---

## Algorithm and Design Decisions

Understanding why specific design choices were made - and what the alternatives were - is as important as understanding what the code does. Every decision in GitSim involves a deliberate trade-off between accuracy, simplicity, and educational value.

| # | Decision | Chosen Approach | Alternatives Considered | Rationale for Choice |
|---|----------|----------------|------------------------|---------------------|
| <sub>1</sub> | <sub>**Hash generation**</sub> | <sub>Random 7-char hex via `random.randint` + hex formatting</sub> | <sub>SHA-1 of content (real Git), UUID4, sequential integers, `secrets.token_hex`</sub> | <sub>Real SHA-1 would require serialising the full commit object (tree hash + parent hash + message + author + timestamp), adding significant complexity with zero training benefit. Random hex gives the correct visual appearance. Sequential integers would look obviously fake.</sub> |
| <sub>2</sub> | <sub>**Commit storage**</sub> | <sub>`dict[hash -> Commit]` for O(1) lookup by hash</sub> | <sub>List of commits, doubly-linked list, SQLite, b-tree</sub> | <sub>A dict keyed by hash exactly mirrors how Git's object store works conceptually. Parent traversal is O(depth) just like real Git's object graph walk. A list would require O(n) hash lookup, diverging from real semantics and introducing artificial performance characteristics.</sub> |
| <sub>3</sub> | <sub>**Rebase implementation**</sub> | <sub>`deepcopy` of commits with new random hashes and rewired parent pointers</sub> | <sub>Moving branch pointers only, patch application via diff, cherry-pick simulation</sub> | <sub>Real `git rebase` rewrites commit objects because the parent SHA is part of the hashed content - changing the parent changes the hash. Deep-copying with new hashes correctly teaches that rebase changes history and explains why force-push is required afterward. A pointer-move approach would hide this crucial lesson entirely.</sub> |
| <sub>4</sub> | <sub>**Fluent interface**</sub> | <sub>All `GitRepo` methods return `self` for method chaining</sub> | <sub>Void methods, separate builder class, command pattern objects</sub> | <sub>Method chaining keeps scenario scripts readable and sequential, mirroring the way a developer types commands one after another in a terminal session. The call order is visually obvious without needing variable assignments or intermediate state inspections.</sub> |
| <sub>5</sub> | <sub>**File snapshots**</sub> | <sub>Full `deepcopy` of file dict per commit</sub> | <sub>Delta compression, content-addressed blob deduplication (real Git), copy-on-write</sub> | <sub>Real Git deduplicates identical content using SHA-1 addressed blob objects in a pack file. GitSim uses full copies for simplicity. At training-data scale (a few KB per scenario) memory cost is negligible, and the implementation is trivially correct without needing a blob store.</sub> |
| <sub>6</sub> | <sub>**Diff rendering**</sub> | <sub>Simple before/after line comparison in `diff_block()`</sub> | <sub>`difflib.unified_diff` (stdlib Myers implementation), custom Myers diff, GNU diff subprocess</sub> | <sub>`difflib.unified_diff` would produce more accurate diffs for complex changes but adds four lines of import and wrapping code. For training purposes, a simple red/green render communicates the concept of a diff clearly. The goal is understanding, not byte-accurate patch generation.</sub> |
| <sub>7</sub> | <sub>**Fake monotonic clock**</sub> | <sub>Per-repo `_hour` counter incremented on each `_tick()` call</sub> | <sub>`datetime.now()` (real wall clock), Unix timestamps, UUID-based ordering, sequence numbers</sub> | <sub>Real wall clock time produces identical or reversed timestamps for rapid test runs, making the log graph confusing. A monotonic counter guarantees commits always appear in correct chronological order regardless of execution speed or test environment.</sub> |
| <sub>8</sub> | <sub>**Zero external dependencies**</sub> | <sub>Python stdlib only - `dataclasses`, `copy`, `argparse`, `random`, `datetime`</sub> | <sub>`GitPython` (full Git bindings), `pygit2` (libgit2 bindings), `click` (CLI), `rich` (terminal UI)</sub> | <sub>Zero-dependency design means GitSim runs in any Python 3.10+ environment without setup. Critical for onboarding environments, air-gapped enterprise systems, CI containers, and training kiosks where `pip install` may be unavailable, slow, or restricted.</sub> |

---

## Tech Stack

GitSim is intentionally minimal. Every technology choice was made to maximise portability, minimise the barrier to running it, and keep the implementation clear enough that a learner can read the source code and understand how it works.

| # | Component | Technology | Version | Why This and Not Something Else |
|---|-----------|-----------|---------|--------------------------------|
| <sub>1</sub> | <sub>Language</sub> | <sub>Python</sub> | <sub>3.10+</sub> | <sub>Ubiquitous in developer environments across all platforms. `dataclasses` (3.7+), `from __future__ import annotations` for forward references, and `match` readiness are all available. No compilation step.</sub> |
| <sub>2</sub> | <sub>Data modelling</sub> | <sub>`dataclasses` (stdlib)</sub> | <sub>stdlib</sub> | <sub>Provides typed, auto-`__repr__`, auto-`__init__` structs for `Commit`, `Branch`, and `PullRequest` without runtime overhead. Pydantic or `attrs` would add validation but also add an external dependency and significant complexity for simple value objects.</sub> |
| <sub>3</sub> | <sub>Deep copy</sub> | <sub>`copy.deepcopy` (stdlib)</sub> | <sub>stdlib</sub> | <sub>Required for two critical operations: snapshotting the working tree into a commit (so future edits do not mutate historical snapshots) and rebase (creating new commit objects with updated parent pointers without aliasing the originals).</sub> |
| <sub>4</sub> | <sub>CLI parsing</sub> | <sub>`argparse` (stdlib)</sub> | <sub>stdlib</sub> | <sub>Standard, zero-dependency CLI argument parsing with built-in `--help` generation. `click` or `typer` would produce slightly nicer help output but add an external dependency for a two-argument CLI that does not need it.</sub> |
| <sub>5</sub> | <sub>Terminal output</sub> | <sub>ANSI escape codes (raw strings)</sub> | <sub>-</sub> | <sub>Works on all POSIX terminals and modern Windows Terminal (Windows 10+) without any library. `rich` would produce prettier output with spinners and tables but adds a dependency. `colorama` would add Windows compatibility for older terminals but again adds a dependency.</sub> |
| <sub>6</sub> | <sub>Randomness</sub> | <sub>`random` (stdlib)</sub> | <sub>stdlib</sub> | <sub>Used only for fake commit hash generation - display-only hex strings that need to look random but carry no security requirements. `secrets` or `os.urandom` would be cryptographically secure but overkill and slower for this purpose.</sub> |
| <sub>7</sub> | <sub>Date and time</sub> | <sub>`datetime` (stdlib)</sub> | <sub>stdlib</sub> | <sub>Used for generating plausible ISO-8601 commit timestamps via a fake monotonic clock. `arrow` or `pendulum` would provide friendlier timezone handling but again add unnecessary dependencies for what is essentially just a string formatter.</sub> |

---

## Feature Branch State Machine

```mermaid
flowchart LR
    UNINIT(["Uninitialised\nrepo"]) -->|"init()"| CLEAN(["Clean\nmain branch"])
    CLEAN -->|"checkout_new(branch)"| ONBRANCH(["On feature\nbranch"])
    ONBRANCH -->|"write(file)"| DIRTY(["Working tree\ndirty"])
    DIRTY -->|"stage_patch(file)"| STAGED(["Files\nstaged"])
    STAGED -->|"commit(msg)"| COMMITTED(["Committed\nto branch"])
    COMMITTED -->|"fetch()"| FETCHED(["Remote refs\nupdated"])
    FETCHED -->|"rebase(main)"| SYNCED(["Branch synced\nwith main"])
    SYNCED -->|"push()"| PUSHED(["Branch on\nremote"])
    PUSHED -->|"open_pr(title)"| PR_OPEN(["PR open\nawaiting review"])
    PR_OPEN -->|"review change request"| CHANGES(["Changes\nrequested"])
    CHANGES -->|"write + commit fix"| PR_OPEN
    PR_OPEN -->|"review approve"| APPROVED(["PR\napproved"])
    APPROVED -->|"merge_pr(squash)"| MERGED(["Merged\nto main"])
    MERGED -->|"checkout(main)"| CLEAN
    style COMMITTED fill:#1a3a1a,stroke:#2ea043,color:#fff
    style APPROVED fill:#1a3a1a,stroke:#2ea043,color:#fff
    style MERGED fill:#0d3b1e,stroke:#2ea043,color:#fff
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
    Creating a branch is instant and cheap - it is just a named
    pointer to commit a3f9c2b. No files are copied.

[STAGE] git add -p src/weather.py -> staged selected hunks
    git add -p (patch mode) lets you review each change hunk
    individually and choose whether to stage it.

[COMMIT] "feat(api): add storm endpoint with severity scoring"  [b7d1e4f]
    git commit saves the staged snapshot permanently into history.

--- a/src/weather.py
+++ b/src/weather.py
@@ -1,2 +1,5 @@
-def forecast(): pass
+def forecast(): return {}
+
+def storm_severity(data):
+    return data.get("intensity", 0) * 1.5

[FETCH] Fetching from origin... remote refs updated
    git fetch downloads new commits from the remote without changing
    your local branches. Always fetch before rebasing.

[REBASE] git rebase origin/main -> replaying commits on top of main
    Rebase replays your commits onto the latest main. Your commit
    hashes change because the parent has changed.

[PUSH] git push origin feature/add-storm-endpoint
    Your branch is now on the remote and a PR can be opened.

[PR] Opened Pull Request #1: "feat: add storm endpoint"
    source: feature/add-storm-endpoint -> target: main
    reviewers: Hemmer, Priya

[REVIEW] Hemmer commented: "Add docstring and type hints please"
[REVIEW] Hemmer REQUESTED CHANGES on PR #1

[COMMIT] "docs: add docstring and type hints to storm_severity"  [f1a2b3c]

[REVIEW] Hemmer APPROVED PR #1
[MERGE] Squash merge: feature/add-storm-endpoint -> main  [c8e2f5a]
    All feature commits squashed into one clean commit on main.

[CONFLICT] Merge conflict in src/parser.py
<<<<<<< HEAD
def parse(data): raise TypeError('str required')
=======
def parse(data): if data is None: return ''
>>>>>>> incoming

[RESOLVE] Conflict in src/parser.py resolved and staged
[REBASE] git rebase origin/main -> replaying commits on top of main
[WARNING] You are committing DIRECTLY to main!
[WARNING] This bypasses review and CI. Use a feature branch instead.
```

---

## What the Simulator Teaches

Each concept is not just named - it is demonstrated with visible state changes, coloured diffs, and explicit plain-English explanations. The table below maps each concept to how GitSim makes it visible and tangible, and explains why each concept matters in a professional team context.

| # | Concept | How GitSim Shows It | Why It Matters |
|---|---------|--------------------|--------------:|
| <sub>1</sub> | <sub>**Branching strategy**</sub> | <sub>Every feature starts with `checkout_new` from an up-to-date main. Branch pointer shown as a hash. Cost of branching is shown as instant (pointer assignment, not file copy).</sub> | <sub>Branches isolate work in progress from the stable main branch. Without branches, every half-finished feature risks breaking the shared codebase for the entire team.</sub> |
| <sub>2</sub> | <sub>**Staging vs committing**</sub> | <sub>WRITE -> STAGE -> COMMIT shown sequentially with diffs and `git status` output at each transition. `_working`, `_staged`, and `_commits` shown as distinct zones.</sub> | <sub>Staging is Git's superpower. It lets you craft atomic, single-purpose commits even when your working tree contains multiple unrelated edits - a capability no other mainstream VCS had before Git.</sub> |
| <sub>3</sub> | <sub>**Pull Requests**</sub> | <sub>Full PR lifecycle: open with title and reviewers, diff shown, comment thread, change-request, fix push, re-review, approval, squash merge. `PullRequest` object state shown at each step.</sub> | <sub>PRs are the primary code quality gate in every professional team. They enforce review, trigger CI, create an audit trail, and prevent unreviewed code from reaching production.</sub> |
| <sub>4</sub> | <sub>**Code review**</sub> | <sub>Reviewer requests changes with a comment; developer addresses feedback with a new commit; reviewer re-approves. The comment thread in `pr.comments` grows visibly.</sub> | <sub>Code review catches bugs, enforces standards, spreads knowledge across the team, and creates shared ownership of the codebase. It is not bureaucracy - it is the primary quality mechanism of professional software development.</sub> |
| <sub>5</sub> | <sub>**Merge conflicts**</sub> | <sub>Two branches modify the same line; conflict markers rendered in colour with `conflict_block()`; resolution staged and committed. Scenario 2 is dedicated entirely to this.</sub> | <sub>Conflicts are inevitable in any active team project. Knowing how to read conflict markers, understand what each side represents, and produce a correct resolution is a core professional skill.</sub> |
| <sub>6</sub> | <sub>**Rebasing**</sub> | <sub>Standard rebase + interactive squash rebase in Scenario 3. Old hashes and new hashes shown side by side to make the history rewrite visible. Force-push requirement explained.</sub> | <sub>Rebase produces a linear, readable history. Understanding that it rewrites commit hashes explains why force-push is required afterward and why you must never rebase shared branches.</sub> |
| <sub>7</sub> | <sub>**Stashing**</sub> | <sub>Mid-task `stash()`, branch switch for hotfix, `stash_pop()` to resume. `git status` shown before and after each stash operation to make the state change clear.</sub> | <sub>Stash is a temporary shelf for incomplete work. Without it, half-finished changes would either prevent branch switches or contaminate the hotfix branch with unrelated work.</sub> |
| <sub>8</sub> | <sub>**Bad practices**</sub> | <sub>Direct main commit, force push, giant commits, vague messages - each shown with a red `[WARNING]` tag followed immediately by the correct alternative. Scenario 4 is entirely dedicated to this.</sub> | <sub>Seeing what goes wrong - and exactly why - is more memorable than abstract rules. Negative examples with explicit consequence explanations create stronger mental models than positive examples alone.</sub> |
| <sub>9</sub> | <sub>**Commit graph**</sub> | <sub>ASCII log graph printed after each scenario showing branch topology, commit hashes, messages, and parent relationships as a rendered DAG.</sub> | <sub>Visualising the commit graph makes abstract concepts like diverged histories, rebase linearisation, and merge commits concrete and understandable rather than theoretical.</sub> |

---

## Project Structure

```
gitsim/
├── run.py                         <- CLI entry point, argparse, scenario dispatch
├── README.md                      <- This file
└── gitsim/
    ├── __init__.py
    ├── repo.py                    <- GitRepo state machine (the core engine)
    ├── actions.py                 <- Composed workflow helpers (feature cycle, stash demo)
    ├── explain.py                 <- Narrator / instructor voice (intro, outro, section)
    ├── utils.py                   <- ANSI colours, diff blocks, log graph, hash gen
    └── scenarios/
        ├── __init__.py
        ├── feature_branch.py      <- Scenario 1: full feature lifecycle
        ├── merge_conflict.py      <- Scenario 2: conflict creation and resolution
        ├── rebase_example.py      <- Scenario 3: standard + interactive rebase
        ├── bad_practice.py        <- Scenario 4: anti-patterns with consequences
        └── branching_strategy.py  <- Scenario 5: corporate branch hierarchy
```

---

## API Reference

<details>
<summary><strong>GitRepo - Core State Machine (click to expand)</strong></summary>

`GitRepo` is the central class. All methods return `self` for fluent chaining unless otherwise noted. Construct with `GitRepo(name, author)` and call `init()` before any other method.

**Lifecycle Methods**

| Method | Signature | Description |
|--------|-----------|-------------|
| <sub>`__init__`</sub> | <sub>`(name: str, author: str = "Dev")`</sub> | <sub>Create an uninitialised repo with empty state. All internal dicts are empty. Must call `init()` before using any other method.</sub> |
| <sub>`init`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Create the root empty commit, create the `main` branch pointing to it, set `_current = "main"`, mark `_initialised = True`.</sub> |
| <sub>`add_remote`</sub> | <sub>`(name: str = "origin") -> GitRepo`</sub> | <sub>Register a simulated remote by snapshotting all current branch heads into `_remotes[name]`. Simulates `git remote add`.</sub> |

**Working Tree and Staging**

| Method | Signature | Description |
|--------|-----------|-------------|
| <sub>`write`</sub> | <sub>`(filename: str, content: str) -> GitRepo`</sub> | <sub>Write a file to `_working` (the working tree). Simulates editing a file in an editor. Prints a coloured diff between the old and new content.</sub> |
| <sub>`stage_patch`</sub> | <sub>`(filename: str) -> GitRepo`</sub> | <sub>Move a file from `_working` into `_staged` (the index). Simulates `git add -p`. Prints the staged content.</sub> |
| <sub>`commit`</sub> | <sub>`(message: str) -> GitRepo`</sub> | <sub>Create a new `Commit` object from `_staged`, store it in `_commits`, advance the current branch pointer. Clears `_staged`. Prints commit hash and message.</sub> |
| <sub>`status`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Compare `_working`, `_staged`, and `_tracked` (last commit snapshot) and print a `git status`-style summary of modified, staged, and untracked files.</sub> |
| <sub>`stash`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Push `_working` dirty state onto an internal stash stack. Resets `_working` to match `_tracked`. Simulates `git stash push`.</sub> |
| <sub>`stash_pop`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Pop the most recent entry from the stash stack back into `_working`. Simulates `git stash pop`.</sub> |

**Branching and History**

| Method | Signature | Description |
|--------|-----------|-------------|
| <sub>`checkout`</sub> | <sub>`(branch: str) -> GitRepo`</sub> | <sub>Switch `_current` to an existing branch. Updates `_tracked` to the HEAD commit's file snapshot. Simulates `git checkout` / `git switch`.</sub> |
| <sub>`checkout_new`</sub> | <sub>`(branch: str) -> GitRepo`</sub> | <sub>Create a new `Branch` object pointing to the current HEAD hash, switch to it. Simulates `git checkout -b` / `git switch -c`.</sub> |
| <sub>`merge`</sub> | <sub>`(source: str) -> GitRepo`</sub> | <sub>Merge `source` branch into `_current`. Detects overlapping file edits and calls `conflict_block()` for each. Requires manual `resolve_conflict()` if conflicts exist.</sub> |
| <sub>`rebase`</sub> | <sub>`(onto: str) -> GitRepo`</sub> | <sub>Deep-copy all commits on `_current` that are not on `onto`, assign new random hashes, rewire parent pointers to form a linear chain from the tip of `onto`, update `_current` branch pointer.</sub> |
| <sub>`log`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Traverse `_commits` by following parent pointers from each branch tip and render an ASCII DAG with branch labels, short hashes, timestamps, and commit messages.</sub> |

**Remote Operations**

| Method | Signature | Description |
|--------|-----------|-------------|
| <sub>`fetch`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Snapshot current branch heads into `_remotes["origin"]`. Does NOT modify local branches. Simulates `git fetch` - download only, no local changes.</sub> |
| <sub>`pull`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Call `fetch()` then merge remote changes into the current branch. Simulates `git pull` (merge strategy). Use `fetch` + `rebase` for the rebase strategy.</sub> |
| <sub>`push`</sub> | <sub>`() -> GitRepo`</sub> | <sub>Update `_remotes["origin"][current_branch]` to the current HEAD hash. Simulates `git push origin <branch>`.</sub> |

**Pull Requests**

| Method | Signature | Description |
|--------|-----------|-------------|
| <sub>`open_pr`</sub> | <sub>`(title: str, reviewers: list[str]) -> PullRequest`</sub> | <sub>Create a `PullRequest` object, auto-increment `_pr_counter`, append to `_prs`, print PR summary with diff. Returns the object for passing to `review_pr` and `merge_pr`.</sub> |
| <sub>`review_pr`</sub> | <sub>`(pr: PullRequest, reviewer: str, approve: bool, comment: str) -> GitRepo`</sub> | <sub>Append `comment` to `pr.comments`, set `pr.approved = approve`. Prints reviewer name, comment, and APPROVED or REQUESTED CHANGES status.</sub> |
| <sub>`merge_pr`</sub> | <sub>`(pr: PullRequest, squash: bool = True) -> GitRepo`</sub> | <sub>Assert `pr.approved`. If `squash=True`, create one new commit on main containing the combined diff of the feature branch. Set `pr.merged = True`. Prints merge summary.</sub> |

</details>

<details>
<summary><strong>actions.py - Composed Workflow Helpers (click to expand)</strong></summary>

The `actions` module provides reusable multi-step workflow patterns built on top of `GitRepo`. Each function chains multiple repo operations into a named, self-contained workflow that represents a complete professional pattern. Using these functions in scenarios keeps the scenario scripts short and readable.

| Function | Signature | What It Does Step by Step |
|----------|-----------|--------------------------|
| <sub>`full_feature_cycle`</sub> | <sub>`(repo, branch_name, filename, content, commit_msg, pr_title, reviewer) -> PullRequest`</sub> | <sub>1. checkout main, 2. pull latest, 3. checkout_new branch, 4. write file, 5. stage_patch, 6. commit, 7. fetch, 8. rebase main, 9. push, 10. open_pr, 11. review (change request), 12. fix + commit, 13. review (approve), 14. merge_pr squash, 15. log. Returns the merged PR object.</sub> |
| <sub>`demonstrate_sync_before_commit`</sub> | <sub>`(repo) -> None`</sub> | <sub>Prints a `[SYNC]` step, calls `repo.fetch()`, calls `repo.rebase("main")`, prints a multi-sentence explanation of why fetch+rebase before push prevents diverged histories and makes merges trivial.</sub> |
| <sub>`demonstrate_stash_workflow`</sub> | <sub>`(repo, filename) -> None`</sub> | <sub>1. write dirty content to filename, 2. print status (dirty), 3. stash, 4. print status (clean), 5. stash_pop, 6. print status (dirty again). Demonstrates the complete save/switch/restore stash pattern.</sub> |

</details>

<details>
<summary><strong>utils.py - Terminal Output Primitives (click to expand)</strong></summary>

All terminal output in GitSim flows through `utils.py`. Nothing else in the codebase calls `print()` directly except through these functions. This centralises formatting decisions and makes it easy to redirect or suppress output for testing.

**ANSI Colour Constants**

| Constant | Code | Usage |
|----------|------|-------|
| <sub>`RESET`</sub> | <sub>`\033[0m`</sub> | <sub>End all formatting</sub> |
| <sub>`BOLD`</sub> | <sub>`\033[1m`</sub> | <sub>Section headers and tags</sub> |
| <sub>`DIM`</sub> | <sub>`\033[2m`</sub> | <sub>Explanation text (instructor voice)</sub> |
| <sub>`RED`</sub> | <sub>`\033[91m`</sub> | <sub>Removed diff lines, conflict markers, warnings</sub> |
| <sub>`GREEN`</sub> | <sub>`\033[92m`</sub> | <sub>Added diff lines, success messages, normal steps</sub> |
| <sub>`YELLOW`</sub> | <sub>`\033[93m`</sub> | <sub>Section banners, conflict separator, sync steps</sub> |
| <sub>`BLUE`</sub> | <sub>`\033[94m`</sub> | <sub>Remote and fetch operations</sub> |
| <sub>`CYAN`</sub> | <sub>`\033[96m`</sub> | <sub>Top-level banners and intro/outro</sub> |

**Output Functions**

| Function | Signature | Description |
|----------|-----------|-------------|
| <sub>`banner`</sub> | <sub>`(text: str, colour: str) -> None`</sub> | <sub>Print a bold 66-character wide `===` box with centred title. Used for scenario section breaks.</sub> |
| <sub>`step`</sub> | <sub>`(tag: str, message: str, colour: str) -> None`</sub> | <sub>Print `[TAG] message` in the specified colour. Every simulated Git command goes through this function.</sub> |
| <sub>`explain`</sub> | <sub>`(text: str, indent: int = 4) -> None`</sub> | <sub>Word-wrap `text` to 70 columns, indent by `indent` spaces, print in DIM colour. This is the instructor voice that follows each `step()` call.</sub> |
| <sub>`diff_block`</sub> | <sub>`(filename: str, before: list[str], after: list[str]) -> None`</sub> | <sub>Print a unified-diff-style header then before lines in RED and after lines in GREEN.</sub> |
| <sub>`conflict_block`</sub> | <sub>`(filename: str, ours: str, theirs: str) -> None`</sub> | <sub>Print Git-style conflict markers: `<<<<<<< HEAD` in RED, `=======` in YELLOW, `>>>>>>> incoming` in GREEN.</sub> |
| <sub>`log_graph`</sub> | <sub>`(commits: dict, branches: dict) -> None`</sub> | <sub>Walk the commit DAG from all branch tips, render ASCII graph lines with branch labels.</sub> |
| <sub>`make_hash`</sub> | <sub>`() -> str`</sub> | <sub>Return a random 7-character lowercase hex string. Called once per commit, once per rebase replay.</sub> |
| <sub>`fake_timestamp`</sub> | <sub>`(hour: int) -> str`</sub> | <sub>Return `2024-01-01T{hour:02d}:00:00` as a deterministic, sortable ISO-8601 string.</sub> |
| <sub>`warning`</sub> | <sub>`(text: str) -> None`</sub> | <sub>Print a bold RED `[WARNING]` tagged line. Used exclusively in Scenario 4 for bad-practice demonstrations.</sub> |
| <sub>`success`</sub> | <sub>`(text: str) -> None`</sub> | <sub>Print a bold GREEN `[OK]` tagged line. Used for successful merge, push, and resolve confirmations.</sub> |
| <sub>`hr`</sub> | <sub>`(char: str = "-") -> None`</sub> | <sub>Print a 66-character horizontal rule using the given character. Used as a visual section separator.</sub> |

</details>

<details>
<summary><strong>run.py - CLI Entry Point (click to expand)</strong></summary>

`run.py` is the only executable entry point. It is intentionally thin - its only job is to parse arguments, set up the scenario map, instantiate a fresh `GitRepo` per scenario, and call the scenario function. All logic lives in the modules it calls.

```python
# Usage
python run.py                  # Run all 5 scenarios
python run.py --scenario 1     # Run only scenario 1
python run.py -s 5             # Corporate branching strategy
```

**Error handling:** Each scenario is wrapped in a `try/except`. If a scenario raises an unhandled exception, the error is printed with the scenario number and the exception is re-raised so the exit code is non-zero. This allows CI pipelines to detect failures.

**Fresh repo per scenario:** `GitRepo("GalacticWeather", author="Dev")` is instantiated inside the loop for each selected scenario. This guarantees zero state leakage between scenarios, making each one fully self-contained and independently runnable.

```python
# Scenario map in run.py
scenarios = {
    1: ("Feature Branch Workflow",        feature_branch.run),
    2: ("Merge Conflict Resolution",      merge_conflict.run),
    3: ("Rebasing",                        rebase_example.run),
    4: ("Bad Practices",                   bad_practice.run),
    5: ("Corporate Branching Strategy",    branching_strategy.run),
}
```

</details>

---

## Key Takeaways

> [!IMPORTANT]
> These eight rules represent the professional Git workflow that GitSim demonstrates across all five scenarios. They are not arbitrary conventions - each one exists to solve a specific, recurring problem in team software development. Internalising all eight will make you a significantly more effective and less error-prone collaborator on any team.

1. **Every task gets its own branch, branched from up-to-date main.** Working directly on main bypasses every quality control your team has in place - code review, automated tests, security scans - and risks destabilising the shared codebase for every teammate the moment you push.

2. **Stage intentionally with `git add -p`.** Staging individual hunks rather than entire files or directories (`git add .`) ensures each commit contains exactly one logical change. This makes history bisectable, reverts clean, and code reviews focused.

3. **Commit messages explain WHY, not what.** The diff already shows exactly what changed. The message should explain the reason for the change, the business context, the bug being fixed, or the requirement being met - information that cannot be inferred from reading the code alone.

4. **Always fetch and rebase before pushing.** Running `git fetch` followed by `git rebase origin/main` ensures your branch is built on top of the latest remote state, prevents diverged histories, makes the eventual PR merge trivial, and avoids the embarrassing "rejected push" error from a remote that has moved ahead.

5. **PRs require review and CI pass before merging.** No developer, regardless of experience level, is immune to bugs, logic errors, or security oversights. A second pair of eyes and an automated test suite are the primary defences against regressions reaching production.

6. **Squash merge keeps main history clean.** A feature may require dozens of WIP commits, fixups, and "try again" commits to develop. Squashing collapses them into a single meaningful commit on main, making `git log` on the main branch a useful, readable audit trail rather than an archaeological dig through development noise.

7. **Delete feature branches after merging.** Stale branches create confusion about what work is active, clutter the branch list, and can cause accidental checkouts. A branch that has been merged to main has served its purpose and should be deleted immediately.

8. **Never force-push to shared branches.** Force-pushing rewrites history. Any teammate who has already pulled or based work on the old commits will have a diverged history that is painful and time-consuming to reconcile. Force-push (`--force-with-lease`) is only safe on branches that only you are using and that have not been reviewed or depended upon by anyone else.

---

## No Dependencies

GitSim uses only the Python standard library. There is nothing to install, no version conflicts to manage, no virtual environment required, and no network access needed. This is a deliberate architectural decision to maximise portability and eliminate setup friction for training environments, air-gapped systems, and developer onboarding sessions where time and network access may be limited.

```bash
python --version   # >= 3.10 recommended
python run.py      # that is all that is needed
```

> [!TIP]
> To run a specific scenario in isolation - for example when running a focused workshop on conflict resolution - use the `--scenario` flag: `python run.py --scenario 2`. This runs only the merge conflict scenario and produces about 60 lines of output, making it easy to walk through live with a group without scrolling through unrelated material.

---

## How Documentation Is Tracked by Git

Documentation files are tracked by Git in exactly the same way as code files. To Git, a `.md` file, a `.rst` file, a `.txt` file, and a `.py` file are all just sequences of bytes. Git does not treat them differently. The `git add`, `git commit`, `git diff`, `git log`, and `git blame` commands all work identically on documentation as they do on source code. This is one of Git's most important properties for professional teams — the history of *why* the docs changed is preserved alongside the history of why the code changed.

> [!NOTE]
> Many teams store documentation in the same repository as the code (`docs-as-code`). This is the recommended approach because it keeps docs in sync with the code that describes. When a developer changes an API and updates the docs in the same commit or PR, reviewers can see both changes together. If docs live in a separate repository, this linkage is lost.

---

### What Branch Name Should Documentation Changes Use?

The branch name depends entirely on **why** the documentation is being written. There is no special "docs branch type" — documentation follows the same branch naming rules as everything else, because documentation *is* part of the work, not a separate activity.

```mermaid
flowchart TD
    Q{Why are you\nwriting docs?}

    Q -->|"New feature or API\nalready has a ticket"| A
    Q -->|"Bug in the docs —\nwrong information, outdated"| B
    Q -->|"Docs-only work —\nno code change involved"| C
    Q -->|"Release notes /\nCHANGELOG for this sprint"| D
    Q -->|"Emergency — docs describe\nbroken production behaviour"| E

    A["Use the same feature branch\nfeature/PROJ-123-description\nDocs go in the same PR as the code"]
    B["bugfix/PROJ-188-fix-auth-api-docs\nSame rules as a code bugfix\nTarget: develop"]
    C["docs/PROJ-201-add-deployment-guide\nDocs-only branch with docs/ prefix\nTarget: develop"]
    D["Use the release branch\nrelease/1.1.0\nCHANGELOG committed directly here"]
    E["hotfix/PROJ-202-correct-critical-doc-error\nSame rules as a code hotfix\nTarget: main + back-merge to develop"]

    style A fill:#1a3a1a,stroke:#2ea043,color:#fff
    style B fill:#1a2a3a,stroke:#4a9eff,color:#fff
    style C fill:#2a1a3a,stroke:#9a4aff,color:#fff
    style D fill:#3a2a0a,stroke:#f0a030,color:#fff
    style E fill:#3a0a0a,stroke:#ff4a4a,color:#fff
```

---

### Branch Naming for Documentation — Full Reference

| # | Situation | Branch Name Pattern | Example | Target Branch | Ticket Required? |
|---|-----------|-------------------|---------|--------------|-----------------|
| <sub>1</sub> | <sub>**Docs bundled with a feature**</sub> | <sub>`feature/<TICKET-ID>-<description>`</sub> | <sub>`feature/PROJ-123-user-auth`</sub> | <sub>`develop`</sub> | <sub>Yes — same ticket as the feature</sub> |
| <sub>2</sub> | <sub>**Docs-only new content** (new guide, new tutorial, new architecture doc)</sub> | <sub>`docs/<TICKET-ID>-<description>`</sub> | <sub>`docs/PROJ-201-add-deployment-guide`</sub> | <sub>`develop`</sub> | <sub>Yes — create a docs ticket in the sprint</sub> |
| <sub>3</sub> | <sub>**Fix incorrect or outdated docs**</sub> | <sub>`bugfix/<TICKET-ID>-<description>`</sub> | <sub>`bugfix/PROJ-188-fix-stale-api-reference`</sub> | <sub>`develop`</sub> | <sub>Yes — file a bug ticket for the bad docs</sub> |
| <sub>4</sub> | <sub>**Improve or expand existing docs** (no bug, just better explanation)</sub> | <sub>`docs/<TICKET-ID>-<description>`</sub> | <sub>`docs/PROJ-215-expand-rebase-section`</sub> | <sub>`develop`</sub> | <sub>Yes — improvement tickets keep work visible and prioritised</sub> |
| <sub>5</sub> | <sub>**CHANGELOG / release notes**</sub> | <sub>Written directly on `release/<version>`</sub> | <sub>Committed on `release/1.1.0`</sub> | <sub>`main` + back-merge `develop`</sub> | <sub>No separate ticket — part of the release process</sub> |
| <sub>6</sub> | <sub>**Docs describe broken production behaviour** (emergency)</sub> | <sub>`hotfix/<TICKET-ID>-<description>`</sub> | <sub>`hotfix/PROJ-202-correct-critical-api-error`</sub> | <sub>`main` + back-merge `develop`</sub> | <sub>Yes — P1 ticket, treated as a production incident</sub> |
| <sub>7</sub> | <sub>**Inline code comments only** (no separate file)</sub> | <sub>Same branch as the code being commented</sub> | <sub>`feature/PROJ-123-user-auth`</sub> | <sub>Same as code change</sub> | <sub>Same ticket as the code</sub> |

> [!TIP]
> The `docs/` prefix (e.g. `docs/PROJ-201-add-deployment-guide`) is a widely-used convention that signals to CI/CD pipelines that this branch contains no runnable code changes. Many teams configure their CI to skip the full test suite for `docs/*` branches and only run a documentation linting step (e.g. checking for broken links, spell checking, markdown syntax). This makes docs-only PRs faster to merge.

---

### What Goes Inside a Documentation Commit

The commit message for a documentation change follows the same **Conventional Commits** format as a code change. The `type` is `docs`. The `scope` (optional) identifies which part of the documentation changed. The description explains what changed and why — not just "update docs", which tells a future reader nothing.

```
docs(api): PROJ-201 add deployment guide for Kubernetes environments

Previously there was no documentation for deploying to K8s. New
developers had to ask a senior engineer every time. This guide
covers namespace setup, secret injection, health check configuration,
and the rollout strategy.

Closes #PROJ-201
```

**The anatomy of a docs commit message:**

```
docs(scope): TICKET-ID what changed and why
│    │       │          │
│    │       │          └─ One sentence. WHY it changed, not just "update docs"
│    │       └─ Ticket ID so the commit is traceable to a sprint item
│    └─ Optional: which section changed (api, auth, deployment, changelog)
└─ Always "docs" for documentation-only changes
```

| # | Bad commit message | Why it's bad | Good commit message |
|---|-------------------|-------------|---------------------|
| <sub>1</sub> | <sub>`update readme`</sub> | <sub>Zero information. What was updated? Why?</sub> | <sub>`docs(readme): PROJ-201 add K8s deployment section`</sub> |
| <sub>2</sub> | <sub>`fix docs`</sub> | <sub>What was wrong? What did you fix?</sub> | <sub>`docs(api): PROJ-188 correct stale auth endpoint parameters`</sub> |
| <sub>3</sub> | <sub>`documentation changes`</sub> | <sub>Plural, vague, untraceable to any requirement</sub> | <sub>`docs(changelog): add v1.1.0 release notes for sprint 22`</sub> |
| <sub>4</sub> | <sub>`wip`</sub> | <sub>Never acceptable in a PR — squash before opening</sub> | <sub>`docs(guide): PROJ-215 draft initial rebase tutorial`</sub> |

---

### How Git Tracks a New Documentation File — Step by Step

When you create a brand-new documentation file, Git does not automatically know about it. A new file starts as **untracked** — Git sees it exists on disk but has no record of it and will not include it in any commit until you explicitly stage it. This is the same behaviour as any new source file.

```mermaid
sequenceDiagram
    participant FS as File System
    participant WT as Working Tree (untracked)
    participant IDX as Staging Index
    participant HIST as Commit History

    Note over FS,HIST: You create a new file: docs/deployment-guide.md

    FS->>WT: docs/deployment-guide.md created
    Note over WT: git status shows:<br/>Untracked files:<br/>  docs/deployment-guide.md

    WT->>IDX: git add docs/deployment-guide.md
    Note over IDX: git status shows:<br/>Changes to be committed:<br/>  new file: docs/deployment-guide.md

    Note over IDX: You continue editing —<br/>git add again to stage latest version

    IDX->>HIST: git commit -m "docs(api): PROJ-201 add deployment guide"
    Note over HIST: File is now permanently in history.<br/>git log shows the commit.<br/>git blame docs/deployment-guide.md<br/>shows who wrote each line and when.
```

> [!NOTE]
> If you have a `docs/` directory that does not exist yet, Git will track the files inside it but not the directory itself — Git tracks files, not folders. An empty directory cannot be committed. The convention for "I need this directory to exist but it has no files yet" is to place a `.gitkeep` placeholder file inside it: `touch docs/.gitkeep && git add docs/.gitkeep`.

---

### What Files Live Where — Standard Documentation Layout

Most professional projects follow a consistent layout for documentation files. Knowing where things live means you know exactly which file to edit without hunting around.\

```
project-root/
├── README.md                    <- Project overview, quick start, badges
│                                   Audience: anyone landing on the repo
│
├── CHANGELOG.md                 <- Version history, what changed in each release
│                                   Written on: release branches
│                                   Format: https://keepachangelog.com
│
├── CONTRIBUTING.md              <- How to contribute, dev setup, PR process
│                                   Audience: external contributors and new team members
│
├── docs/                        <- Deeper documentation beyond the README
│   ├── architecture/
│   │   ├── overview.md          <- System design, component diagrams
│   │   └── decisions/
│   │       └── ADR-001-use-jwt.md  <- Architecture Decision Records (ADRs)
│   │                               Why a technical decision was made
│   │                               Written at: decision time, never deleted
│   │
│   ├── api/
│   │   ├── reference.md         <- Complete API reference (auto-generated or hand-written)
│   │   └── authentication.md    <- Topic-specific deep dives
│   │
│   ├── guides/
│   │   ├── getting-started.md   <- New developer onboarding walkthrough
│   │   ├── deployment.md        <- How to deploy to each environment
│   │   └── troubleshooting.md   <- Common problems and solutions
│   │
│   └── runbooks/
│       ├── incident-response.md <- What to do when production is on fire
│       └── database-backup.md   <- Operational procedures
│
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md <- Auto-populates when a PR is opened
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md        <- Structured template for bug reports
    │   └── feature_request.md   <- Structured template for feature requests
    └── CODEOWNERS               <- Who is automatically assigned to review
                                    changes in specific directories
```

> [!TIP]
> **Architecture Decision Records (ADRs)** in `docs/architecture/decisions/` are one of the highest-value documentation types that most teams neglect. An ADR is a short document that captures: the context of a decision, the options considered, the decision made, and the consequences. They are never deleted or edited — only superseded by a new ADR. Six months later when someone asks "why do we use JWT instead of sessions?" the ADR has the answer, with the original reasoning intact.

---

### What git blame and git log Tell You About Documentation

Once documentation is committed, Git's history tools give you a complete audit trail — you can see exactly who wrote every line of a doc, when, in which PR, and why (from the commit message). This is one of the most underused features of treating documentation as code.

| # | Command | What It Shows | Example Use Case |
|---|---------|--------------|-----------------|
| <sub>1</sub> | <sub>`git log docs/`</sub> | <sub>All commits that touched any file in the `docs/` directory, with messages, authors, and dates</sub> | <sub>See the full history of documentation changes for a release audit</sub> |
| <sub>2</sub> | <sub>`git log --follow docs/api/reference.md`</sub> | <sub>All commits to a specific doc file, even if the file was renamed or moved</sub> | <sub>Find when a specific API parameter was documented or changed</sub> |
| <sub>3</sub> | <sub>`git blame docs/api/reference.md`</sub> | <sub>Every line of the file annotated with: the commit hash that last changed it, the author, the date, and the line number</sub> | <sub>Find who wrote a specific claim in the docs and in which PR it was added</sub> |
| <sub>4</sub> | <sub>`git diff develop..feature/PROJ-123 -- docs/`</sub> | <sub>All documentation changes introduced by a feature branch compared to develop</sub> | <sub>Review exactly what docs a PR adds or changes before approving</sub> |
| <sub>5</sub> | <sub>`git log --grep="docs(api)"` </sub> | <sub>All commits whose message matches the search pattern</sub> | <sub>Find all API documentation commits across the entire project history</sub> |

```bash
# See every line of a doc and who last changed it:
git blame docs/api/reference.md

# See all changes to docs in the last sprint:
git log --since="2 weeks ago" -- docs/

# See exactly what a docs PR changed:
git diff develop..docs/PROJ-201-deployment-guide -- docs/

# Find when a specific word was added to or removed from docs:
git log -S "kubernetes" -- docs/
```

---

<div align="center">

Built for developers, by developers.
No real Git commands harmed in the making of this simulator.

**[Report an Issue](https://github.com/hkevin01/gitsim/issues)** - **[Open a PR](https://github.com/hkevin01/gitsim/pulls)** - **[Star the repo](https://github.com/hkevin01/gitsim)**

</div>
