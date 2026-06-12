"""
File: gitsim/repo.py

ID: REPO-001
Purpose: In-memory Git repository simulator.
         Maintains complete simulated state - branches, commits, staged files,
         working tree modifications, remotes - without touching the filesystem
         or invoking any real Git commands.
Requirement: Accurately represent Git semantics for training purposes.
Rationale:   A pure-Python state machine means zero environment dependencies
             and reproducible behaviour across all platforms.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from copy import deepcopy

from gitsim.utils import (
    step, explain, diff_block, conflict_block, log_graph,
    make_hash, fake_timestamp, warning, success, hr,
    GREEN, YELLOW, RED, CYAN, BLUE, BOLD, RESET, DIM, WHITE
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Commit:
    """
    ID: REPO-002
    Purpose: Represents a single commit snapshot.
    Fields:
        hash    - str, 40-char hex
        message - str, commit message
        author  - str, author name
        branch  - str, branch the commit was made on
        files   - dict[filename -> content], snapshot of tracked files
        parent  - Optional[str], parent commit hash
        ts      - str, ISO timestamp
    """
    hash:    str
    message: str
    author:  str
    branch:  str
    files:   dict
    parent:  Optional[str] = None
    ts:      str = ""


@dataclass
class Branch:
    """
    ID: REPO-003
    Purpose: Represents a named branch pointer.
    Fields:
        name     - str, branch name
        head     - str, hash of latest commit on this branch
        upstream - Optional[str], remote tracking branch name
    """
    name:     str
    head:     str
    upstream: Optional[str] = None


@dataclass
class PullRequest:
    """
    ID: REPO-004
    Purpose: Represents a simulated Pull Request.
    Fields:
        number    - int, PR number
        title     - str
        source    - str, source branch
        target    - str, target branch (usually main)
        author    - str
        reviewers - list[str]
        approved  - bool
        comments  - list[str]
        merged    - bool
    """
    number:    int
    title:     str
    source:    str
    target:    str
    author:    str
    reviewers: list = field(default_factory=list)
    approved:  bool = False
    comments:  list = field(default_factory=list)
    merged:    bool = False


# ---------------------------------------------------------------------------
# Core repository class
# ---------------------------------------------------------------------------

class GitRepo:
    """
    ID: REPO-005
    Purpose: Simulated Git repository maintaining full state machine.
    Rationale: Provides a safe sandbox for teaching Git concepts without
               requiring a real Git installation or filesystem mutations.
    Side Effects: All output goes to stdout via utils module.
    Verification: Exercised by all scenario modules.
    """

    def __init__(self, name: str, author: str = "Dev"):
        """
        ID: REPO-006
        Purpose: Initialise a clean, uninitialised repository.
        Inputs:
            name   - str, repository name (non-empty)
            author - str, default commit author
        Preconditions: name must be non-empty.
        Postconditions: Repo exists but is not yet initialised (call init()).
        """
        if not name:
            raise ValueError("Repository name must not be empty")
        self.name         = name
        self.author       = author
        self._commits:    dict[str, Commit] = {}
        self._branches:   dict[str, Branch] = {}
        self._current:    str = "main"
        self._staged:     dict[str, str] = {}       # filename -> content
        self._working:    dict[str, str] = {}       # filename -> content
        self._tracked:    dict[str, str] = {}       # HEAD snapshot
        self._remotes:    dict[str, dict] = {}      # remote name -> branch dict
        self._prs:        list[PullRequest] = []
        self._pr_counter: int = 1
        self._hour:       int = 0                   # monotonic fake clock
        self._initialised = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def init(self) -> "GitRepo":
        """
        ID: REPO-007
        Purpose: Initialise the repository and create the first empty commit.
        Postconditions: main branch exists; repo is ready for commits.
        """
        root_hash = make_hash()
        root = Commit(
            hash=root_hash,
            message="Initial empty commit",
            author=self.author,
            branch="main",
            files={},
            ts=fake_timestamp(self._tick()),
        )
        self._commits[root_hash] = root
        self._branches["main"] = Branch("main", root_hash)
        self._current = "main"
        self._initialised = True

        step("INIT", f"Initialised repository '{self.name}' on branch main")
        explain(
            "git init creates a hidden .git directory that stores all version "
            "history, configuration, and metadata. The main branch is created "
            "automatically with an empty root commit."
        )
        return self

    def add_remote(self, name: str = "origin") -> "GitRepo":
        """
        ID: REPO-008
        Purpose: Add a named remote (simulated).
        Inputs:  name - str, remote alias (default 'origin')
        """
        self._remotes[name] = deepcopy({
            b: br.head for b, br in self._branches.items()
        })
        step("REMOTE", f"Added remote '{name}' (simulated)")
        explain(
            f"git remote add {name} <url> links your local repo to a remote "
            "server (GitHub, GitLab, etc.). 'origin' is the conventional name."
        )
        return self

    # ------------------------------------------------------------------
    # Working tree & staging
    # ------------------------------------------------------------------

    def write(self, filename: str, content: str) -> "GitRepo":
        """
        ID: REPO-009
        Purpose: Simulate writing a file to the working tree (unstaged).
        Inputs:
            filename - str, relative path
            content  - str, file content
        Postconditions: File is dirty (modified but not staged).
        """
        old = self._working.get(filename, self._tracked.get(filename, ""))
        self._working[filename] = content

        before = old.splitlines() if old else []
        after  = content.splitlines()

        step("WRITE", f"Modified {filename} (unstaged)", colour=YELLOW)
        explain(
            "The file is now dirty - it exists in your working tree with "
            "changes, but those changes are NOT yet in the staging area. "
            "Running 'git status' would show it under 'Changes not staged'."
        )
        diff_block(filename, before, after)
        return self

    def stage(self, filename: str) -> "GitRepo":
        """
        ID: REPO-010
        Purpose: Move a working-tree file into the staging area (index).
        Inputs:  filename - str, must exist in working tree
        Failure Modes: KeyError if file not in working tree.
        """
        if filename not in self._working:
            raise KeyError(f"'{filename}' not in working tree - nothing to stage")

        self._staged[filename] = self._working[filename]
        step("STAGE", f"git add {filename} -> added to staging area", colour=CYAN)
        explain(
            "git add moves changes into the staging area (index). Staging "
            "lets you craft precise commits - you can stage one file, review "
            "it, stage another, and commit exactly what you want."
        )
        return self

    def stage_patch(self, filename: str) -> "GitRepo":
        """
        ID: REPO-011
        Purpose: Simulate interactive hunk-level staging (git add -p).
        Inputs:  filename - str
        """
        if filename not in self._working:
            raise KeyError(f"'{filename}' not found in working tree")

        self._staged[filename] = self._working[filename]
        step("STAGE", f"git add -p {filename} -> staged selected hunks", colour=CYAN)
        explain(
            "git add -p (patch mode) lets you review each change hunk "
            "individually and choose whether to stage it. This is the most "
            "precise way to build commits and prevents accidental inclusions."
        )
        return self

    def unstage(self, filename: str) -> "GitRepo":
        """
        ID: REPO-012
        Purpose: Remove a file from the staging area back to working tree only.
        """
        if filename in self._staged:
            del self._staged[filename]
            step("UNSTAGE", f"git restore --staged {filename}", colour=YELLOW)
            explain(
                "git restore --staged removes a file from the staging area "
                "without discarding the working-tree changes. Use this if "
                "you staged something by mistake."
            )
        return self

    def status(self) -> "GitRepo":
        """
        ID: REPO-013
        Purpose: Print the simulated output of 'git status'.
        """
        print(f"\n{BOLD}On branch {self._current}{RESET}")
        if self._staged:
            print(f"\n{GREEN}Changes to be committed:{RESET}")
            for f in self._staged:
                print(f"  {GREEN}modified: {f}{RESET}")
        dirty = {k for k in self._working if k not in self._staged}
        if dirty:
            print(f"\n{RED}Changes not staged for commit:{RESET}")
            for f in dirty:
                print(f"  {RED}modified: {f}{RESET}")
        if not self._staged and not dirty:
            print(f"\n{DIM}nothing to commit, working tree clean{RESET}")
        print()
        return self

    # ------------------------------------------------------------------
    # Commits
    # ------------------------------------------------------------------

    def commit(self, message: str) -> "GitRepo":
        """
        ID: REPO-014
        Purpose: Create a new commit from the current staging area.
        Inputs:  message - str, commit message (non-empty)
        Preconditions: Staging area must not be empty.
        Postconditions: New commit is HEAD; staging area is cleared.
        Failure Modes: ValueError if nothing staged.
        """
        if not message:
            raise ValueError("Commit message must not be empty")
        if not self._staged and self._commits:
            # Allow empty initial commit silently
            raise ValueError("Nothing staged to commit - use stage() first")

        parent_hash = self._branches[self._current].head
        snap = deepcopy(self._tracked)
        snap.update(self._staged)

        h = make_hash()
        c = Commit(
            hash=h,
            message=message,
            author=self.author,
            branch=self._current,
            files=snap,
            parent=parent_hash,
            ts=fake_timestamp(self._tick()),
        )
        self._commits[h] = c
        self._branches[self._current].head = h
        self._tracked = snap
        self._staged.clear()

        step("COMMIT", f'"{message}"  {DIM}[{h[:7]}]{RESET}')
        explain(
            f"git commit saves the staged snapshot permanently into history. "
            f"Each commit gets a unique SHA-1 hash. This commit is on branch "
            f"'{self._current}' and its parent is {parent_hash[:7]}."
        )
        return self

    def amend(self, message: str) -> "GitRepo":
        """
        ID: REPO-015
        Purpose: Amend the most recent commit (changes hash - never do on shared branches).
        """
        old_hash = self._branches[self._current].head
        old_c    = self._commits[old_hash]

        snap = deepcopy(old_c.files)
        snap.update(self._staged)

        new_h = make_hash()
        new_c = Commit(
            hash=new_h, message=message, author=self.author,
            branch=self._current, files=snap,
            parent=old_c.parent, ts=fake_timestamp(self._tick()),
        )
        del self._commits[old_hash]
        self._commits[new_h] = new_c
        self._branches[self._current].head = new_h
        self._staged.clear()

        warning(
            f"git commit --amend rewrites history. "
            f"OLD={old_hash[:7]} -> NEW={new_h[:7]}. "
            "Never amend commits already pushed to a shared branch."
        )
        return self

    # ------------------------------------------------------------------
    # Branching
    # ------------------------------------------------------------------

    def branch(self, name: str) -> "GitRepo":
        """
        ID: REPO-016
        Purpose: Create a new branch pointing at the current HEAD.
        Inputs:  name - str, new branch name (must not already exist)
        Failure Modes: ValueError if branch already exists.
        """
        if name in self._branches:
            raise ValueError(f"Branch '{name}' already exists")

        head = self._branches[self._current].head
        self._branches[name] = Branch(name, head)

        step("BRANCH", f"git branch {name}  ->  created at {head[:7]}", colour=BLUE)
        explain(
            f"Creating a branch is instant and cheap - it's just a named "
            f"pointer to commit {head[:7]}. No files are copied. The branch "
            f"diverges only when new commits are added to it."
        )
        return self

    def checkout(self, name: str) -> "GitRepo":
        """
        ID: REPO-017
        Purpose: Switch to an existing branch.
        Inputs:  name - str, target branch name
        Preconditions: Branch must exist; staging area must be clean.
        Failure Modes: KeyError if branch not found; ValueError if dirty index.
        """
        if self._staged:
            raise ValueError(
                f"Cannot checkout '{name}': staging area has uncommitted changes. "
                "Commit or stash first."
            )
        if name not in self._branches:
            raise KeyError(f"Branch '{name}' does not exist")

        self._current = name
        head_commit   = self._commits[self._branches[name].head]
        self._tracked = deepcopy(head_commit.files)

        step("CHECKOUT", f"git checkout {name}  (HEAD -> {self._branches[name].head[:7]})")
        explain(
            f"Switching to '{name}' updates your working tree to match the "
            "snapshot of that branch's latest commit. Any uncommitted staged "
            "changes would block this operation in real Git."
        )
        return self

    def checkout_new(self, name: str) -> "GitRepo":
        """
        ID: REPO-018
        Purpose: Create a new branch and immediately check it out (git checkout -b).
        """
        self.branch(name)
        self.checkout(name)
        explain(
            "git checkout -b is a shortcut: create + switch in one command. "
            "Always branch from an up-to-date main to minimise future conflicts."
        )
        return self

    # ------------------------------------------------------------------
    # Remote operations
    # ------------------------------------------------------------------

    def fetch(self) -> "GitRepo":
        """
        ID: REPO-019
        Purpose: Simulate 'git fetch origin' - updates remote tracking refs.
        Side Effects: _remotes['origin'] is updated to current branch state.
        """
        self._remotes["origin"] = deepcopy({
            b: br.head for b, br in self._branches.items()
        })
        step("FETCH", "git fetch origin  ->  remote tracking refs updated", colour=CYAN)
        explain(
            "git fetch downloads objects and refs from the remote but does NOT "
            "modify your local branches. It is always safe to run. After fetch "
            "you can inspect origin/main before deciding to merge or rebase."
        )
        return self

    def push(self, branch: str = None) -> "GitRepo":
        """
        ID: REPO-020
        Purpose: Simulate pushing a branch to origin.
        Inputs:  branch - str, branch to push (defaults to current)
        """
        branch = branch or self._current
        if "origin" not in self._remotes:
            self.add_remote("origin")
        self._remotes["origin"][branch] = self._branches[branch].head
        self._branches[branch].upstream = f"origin/{branch}"

        step("PUSH", f"git push -u origin {branch}", colour=CYAN)
        explain(
            "git push uploads your local branch commits to the remote. "
            "The -u flag sets the upstream tracking reference so future "
            "'git pull' and 'git push' know which remote branch to use."
        )
        return self

    def pull(self) -> "GitRepo":
        """
        ID: REPO-021
        Purpose: Simulate 'git pull' (fetch + fast-forward merge).
        """
        self.fetch()
        step("PULL", f"git pull  ->  fast-forwarded '{self._current}'")
        explain(
            "git pull = git fetch + git merge. If the remote has new commits "
            "your local branch doesn't, Git fast-forwards your branch pointer. "
            "Prefer 'git pull --rebase' to keep history linear."
        )
        return self

    # ------------------------------------------------------------------
    # Merge & Rebase
    # ------------------------------------------------------------------

    def merge(self, source: str, squash: bool = False) -> "GitRepo":
        """
        ID: REPO-022
        Purpose: Merge source branch into current branch.
        Inputs:
            source - str, branch to merge from
            squash - bool, if True simulate squash merge
        Failure Modes: KeyError if source branch not found.
        """
        if source not in self._branches:
            raise KeyError(f"Branch '{source}' not found")

        src_commit = self._commits[self._branches[source].head]
        merge_msg  = f"Merge branch '{source}' into {self._current}"
        if squash:
            merge_msg = f"feat: squash merge '{source}' -> {self._current}"

        # Combine file snapshots (simple non-conflicting merge)
        merged_files = deepcopy(self._tracked)
        merged_files.update(src_commit.files)

        h = make_hash()
        c = Commit(
            hash=h, message=merge_msg, author=self.author,
            branch=self._current, files=merged_files,
            parent=self._branches[self._current].head,
            ts=fake_timestamp(self._tick()),
        )
        self._commits[h] = c
        self._branches[self._current].head = h
        self._tracked = merged_files

        kind = "Squash merge" if squash else "Merge commit"
        step("MERGE", f"{kind}: {source} -> {self._current}  [{h[:7]}]", colour=CYAN)
        if squash:
            explain(
                "Squash merge collapses all commits from the feature branch "
                "into a single commit on main. This keeps the main history "
                "clean and readable - one commit per feature."
            )
        else:
            explain(
                "A merge commit preserves the full branch history. "
                "The resulting commit has two parents. Use this only when "
                "you want to preserve the full context of the feature work."
            )
        return self

    def rebase(self, onto: str) -> "GitRepo":
        """
        ID: REPO-023
        Purpose: Simulate rebasing current branch onto target branch.
        Inputs:  onto - str, branch or ref to rebase onto (e.g. 'main')
        Rationale: Rebase replays commits on top of the target, producing
                   a linear history. Simulated by updating branch pointer.
        """
        if onto not in self._branches and onto not in (
            f"origin/{b}" for b in self._branches
        ):
            raise KeyError(f"Branch '{onto}' not found for rebase")

        # Resolve target hash
        clean = onto.replace("origin/", "")
        target_head = self._branches.get(clean, self._branches.get(onto))
        if target_head is None:
            raise KeyError(f"Cannot resolve '{onto}'")

        step("REBASE", f"git rebase {onto}  ->  replaying commits on top of {onto[:20]}", colour=YELLOW)
        explain(
            f"Rebasing rewrites your branch commits so they appear to start "
            f"from the latest commit on '{onto}'. This produces a perfectly "
            f"linear history with no merge bubbles. Each commit gets a NEW "
            f"hash because its parent changes. Never rebase shared branches."
        )
        return self

    def interactive_rebase(self, n: int = 3) -> "GitRepo":
        """
        ID: REPO-024
        Purpose: Simulate 'git rebase -i HEAD~N'.
        Inputs:  n - int, number of commits to rewrite
        """
        step("REBASE", f"git rebase -i HEAD~{n}  ->  interactive editor opened", colour=YELLOW)
        print(f"{DIM}")
        print("  pick  a1b2c3d  feat: add storm endpoint")
        print("  squash b2c3d4e  fix: typo in storm endpoint")
        print("  reword c3d4e5f  chore: formatting")
        print(f"{RESET}")
        explain(
            "Interactive rebase opens an editor listing your recent commits. "
            "You can 'pick' (keep), 'squash' (combine), 'reword' (rename), "
            "or 'drop' (delete) each commit before they are replayed."
        )
        return self

    # ------------------------------------------------------------------
    # Conflict simulation
    # ------------------------------------------------------------------

    def simulate_conflict(self, filename: str, ours: str, theirs: str) -> "GitRepo":
        """
        ID: REPO-025
        Purpose: Print a merge conflict scenario for training.
        Inputs:
            filename - str, the conflicting file
            ours     - str, content from current branch
            theirs   - str, content from incoming branch
        Postconditions: Prints conflict markers and explanation.
        """
        step("CONFLICT", f"Merge conflict in {filename}", colour=RED)
        conflict_block(filename, ours, theirs)
        explain(
            "Git cannot automatically merge because BOTH branches modified the "
            "same lines. You must manually edit the file, remove the conflict "
            "markers (<<<<<<<, =======, >>>>>>>), choose the correct content, "
            "then run: git add <file> && git rebase --continue"
        )
        return self

    def resolve_conflict(self, filename: str, resolved: str) -> "GitRepo":
        """
        ID: REPO-026
        Purpose: Simulate resolving a merge conflict and staging the result.
        Inputs:
            filename - str
            resolved - str, final content after manual resolution
        """
        self._staged[filename] = resolved
        step("RESOLVE", f"Conflict in {filename} resolved and staged", colour=GREEN)
        explain(
            "After manually resolving conflict markers you stage the file with "
            "'git add <file>' to tell Git the conflict is resolved, then "
            "continue the rebase/merge with 'git rebase --continue' or "
            "'git merge --continue'."
        )
        return self

    # ------------------------------------------------------------------
    # Stash
    # ------------------------------------------------------------------

    def stash(self) -> "GitRepo":
        """
        ID: REPO-027
        Purpose: Simulate 'git stash' - temporarily shelve dirty changes.
        Postconditions: Working tree is clean; stash holds the changes.
        """
        self._stash = deepcopy(self._working)
        self._working.clear()

        step("STASH", "git stash  ->  WIP saved to stash stack", colour=YELLOW)
        explain(
            "git stash saves your uncommitted changes to a temporary stack "
            "and restores a clean working tree. Useful when you need to "
            "switch branches mid-task. Use 'git stash pop' to restore."
        )
        return self

    def stash_pop(self) -> "GitRepo":
        """
        ID: REPO-028
        Purpose: Restore the most recent stash entry.
        Preconditions: A stash must exist.
        Failure Modes: AttributeError if no stash was created.
        """
        if not hasattr(self, "_stash") or not self._stash:
            raise AttributeError("No stash to pop")

        self._working.update(self._stash)
        self._stash = {}

        step("STASH", "git stash pop  ->  WIP restored from stash", colour=GREEN)
        explain(
            "git stash pop re-applies the most recent stash and removes it "
            "from the stash list. Your changes are back in the working tree."
        )
        return self

    # ------------------------------------------------------------------
    # Pull Requests (simulated)
    # ------------------------------------------------------------------

    def open_pr(self, title: str, reviewers: list[str] = None,
                source: str = None, target: str = "main") -> PullRequest:
        """
        ID: REPO-029
        Purpose: Create a simulated Pull Request.
        Inputs:
            title     - str, PR title
            reviewers - list[str], reviewer names
            source    - str, source branch (defaults to current)
            target    - str, target branch (default 'main')
        Outputs: PullRequest instance
        """
        source = source or self._current
        pr = PullRequest(
            number=self._pr_counter,
            title=title,
            source=source,
            target=target,
            author=self.author,
            reviewers=reviewers or [],
        )
        self._prs.append(pr)
        self._pr_counter += 1

        step("PR", f"Opened Pull Request #{pr.number}: \"{title}\"", colour=CYAN)
        print(f"  {DIM}Source : {source}{RESET}")
        print(f"  {DIM}Target : {target}{RESET}")
        print(f"  {DIM}Author : {self.author}{RESET}")
        if reviewers:
            print(f"  {DIM}Reviewers: {', '.join(reviewers)}{RESET}")
        print()
        explain(
            "A Pull Request is a formal request to merge your branch into "
            "main. It gives reviewers a chance to read the diff, run tests, "
            "leave inline comments, request changes, and finally approve. "
            "No code enters main without a reviewed and approved PR."
        )
        return pr

    def review_pr(self, pr: PullRequest, reviewer: str,
                  approve: bool = True, comment: str = "") -> "GitRepo":
        """
        ID: REPO-030
        Purpose: Simulate a code review action on a PR.
        Inputs:
            pr       - PullRequest instance
            reviewer - str, reviewer name
            approve  - bool, True = approved, False = changes requested
            comment  - str, optional inline comment
        """
        if comment:
            pr.comments.append(f"{reviewer}: {comment}")
            step("REVIEW", f"{reviewer} left a comment: \"{comment}\"", colour=YELLOW)
        if approve:
            pr.approved = True
            step("REVIEW", f"{reviewer} APPROVED PR #{pr.number}", colour=GREEN)
            explain(
                "An approval means the reviewer is satisfied with the code "
                "quality, logic, tests, and security. Only after approval can "
                "the PR be merged."
            )
        else:
            step("REVIEW", f"{reviewer} requested changes on PR #{pr.number}", colour=RED)
            explain(
                "Changes requested means the reviewer found issues that must "
                "be addressed before the PR can be merged. Push additional "
                "commits to the same branch to address feedback."
            )
        return self

    def merge_pr(self, pr: PullRequest, squash: bool = True) -> "GitRepo":
        """
        ID: REPO-031
        Purpose: Merge a PR into its target branch.
        Inputs:
            pr     - PullRequest instance
            squash - bool, use squash merge (recommended)
        Preconditions: PR must be approved.
        Failure Modes: PermissionError if PR not approved.
        """
        if not pr.approved:
            raise PermissionError(
                f"PR #{pr.number} is not approved. Cannot merge."
            )

        saved = self._current
        self.checkout(pr.target)
        self.merge(pr.source, squash=squash)
        pr.merged = True

        step("MERGE", f"PR #{pr.number} merged into {pr.target}", colour=GREEN)
        explain(
            f"PR #{pr.number} has been squash-merged into {pr.target}. "
            "The feature branch should now be deleted. main is updated "
            "and the CI pipeline will run on the new commit."
        )
        return self

    # ------------------------------------------------------------------
    # History & diffs
    # ------------------------------------------------------------------

    def log(self, limit: int = 10) -> "GitRepo":
        """
        ID: REPO-032
        Purpose: Print the simulated commit graph for all branches.
        Inputs:  limit - int, max commits to show
        """
        step("LOG", "git log --oneline --graph --decorate --all")
        commits = list(self._commits.values())[-limit:]
        commits.reverse()
        log_graph([
            {"hash": c.hash, "branch": c.branch, "message": c.message,
             "author": c.author}
            for c in commits
        ])
        return self

    def diff(self, branch_a: str, branch_b: str) -> "GitRepo":
        """
        ID: REPO-033
        Purpose: Show a simulated diff between two branches.
        Inputs:  branch_a, branch_b - str, branch names
        """
        if branch_a not in self._branches or branch_b not in self._branches:
            raise KeyError("One or both branches not found")

        files_a = self._commits[self._branches[branch_a].head].files
        files_b = self._commits[self._branches[branch_b].head].files

        all_files = set(files_a) | set(files_b)
        step("DIFF", f"git diff {branch_a}..{branch_b}")

        found = False
        for f in sorted(all_files):
            a_lines = files_a.get(f, "").splitlines()
            b_lines = files_b.get(f, "").splitlines()
            if a_lines != b_lines:
                diff_block(f, a_lines, b_lines)
                found = True

        if not found:
            print(f"  {DIM}No differences between {branch_a} and {branch_b}{RESET}\n")
        return self

    # ------------------------------------------------------------------
    # Tags & bisect
    # ------------------------------------------------------------------

    def tag(self, name: str, message: str = "") -> "GitRepo":
        """
        ID: REPO-034
        Purpose: Create an annotated tag at the current HEAD.
        Inputs:  name - str, tag name; message - str, tag annotation
        """
        head = self._branches[self._current].head
        step("TAG", f"git tag -a {name} -m \"{message}\"  [{head[:7]}]", colour=CYAN)
        explain(
            f"Tags mark specific commits as significant - typically a release. "
            f"Annotated tags (the -a flag) store the tagger, date, and message. "
            f"Push tags with: git push origin {name}"
        )
        return self

    def bisect(self, good_tag: str) -> "GitRepo":
        """
        ID: REPO-035
        Purpose: Simulate 'git bisect' bug-hunt workflow.
        Inputs:  good_tag - str, last known-good commit/tag reference
        """
        step("BISECT", "git bisect start", colour=YELLOW)
        step("BISECT", "git bisect bad   (current HEAD is broken)", colour=RED)
        step("BISECT", f"git bisect good {good_tag}", colour=GREEN)
        explain(
            "git bisect performs a binary search through commit history to "
            "find the exact commit that introduced a bug. Git checks out the "
            "midpoint between good and bad; you test it, mark it good or bad, "
            "and repeat until the culprit commit is isolated."
        )
        return self

    # ------------------------------------------------------------------
    # Bad practice demonstrations
    # ------------------------------------------------------------------

    def force_push(self) -> "GitRepo":
        """
        ID: REPO-036
        Purpose: Demonstrate why force-push is dangerous.
        """
        warning(
            "git push --force  ->  THIS OVERWRITES REMOTE HISTORY"
        )
        explain(
            "Force-pushing rewrites the remote branch pointer, discarding "
            "commits that teammates have already based work on. This causes "
            "diverged histories and data loss. Only use --force-with-lease "
            "and only on personal branches you own exclusively."
        )
        return self

    def direct_main_commit(self) -> "GitRepo":
        """
        ID: REPO-037
        Purpose: Demonstrate and explain why committing directly to main is bad.
        """
        warning("You are committing DIRECTLY to main!")
        warning("Branch protection should prevent this on a real repository.")
        explain(
            "Committing directly to main bypasses code review, CI checks, "
            "and the PR process. Any mistake immediately affects production. "
            "Protected branches enforce that all changes go through a PR with "
            "at least one review and a passing CI build."
        )
        return self

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tick(self) -> int:
        """Advance and return the monotonic fake clock hour."""
        self._hour += 1
        return self._hour

    def __repr__(self) -> str:
        return (
            f"GitRepo(name={self.name!r}, "
            f"branch={self._current!r}, "
            f"commits={len(self._commits)}, "
            f"branches={list(self._branches)!r})"
        )
