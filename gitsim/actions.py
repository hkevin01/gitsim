"""
File: gitsim/actions.py

ID: ACT-001
Purpose: Reusable composed action sequences that combine multiple GitRepo
         operations into named workflow patterns.
Requirement: Each action must be self-contained and produce clear output.
Rationale: Separates scenario orchestration from low-level repo mechanics.
"""

from gitsim.repo import GitRepo, PullRequest
from gitsim.utils import step, explain, hr, warning, success, CYAN, GREEN, YELLOW, RED


def full_feature_cycle(
    repo: GitRepo,
    branch_name: str,
    filename: str,
    content: str,
    commit_msg: str,
    pr_title: str,
    reviewer: str,
) -> PullRequest:
    """
    ID: ACT-002
    Purpose: Execute the complete feature branch lifecycle end-to-end.
    Inputs:
        repo        - GitRepo, the repository to operate on
        branch_name - str, name for the new feature branch
        filename    - str, file to create/modify
        content     - str, file content to write
        commit_msg  - str, commit message
        pr_title    - str, pull request title
        reviewer    - str, reviewer name
    Outputs: PullRequest (merged)
    Postconditions: Feature is merged into main via squash; branch still exists.
    """
    # 1. Start from clean main
    repo.checkout("main")
    repo.pull()

    # 2. Create feature branch
    repo.checkout_new(branch_name)

    # 3. Write, stage, commit
    repo.write(filename, content)
    repo.stage_patch(filename)
    repo.commit(commit_msg)

    # 4. Sync before push
    repo.fetch()
    repo.rebase("main")
    repo.push()

    # 5. Open PR
    pr = repo.open_pr(pr_title, reviewers=[reviewer])

    # 6. Review & approve
    repo.review_pr(
        pr, reviewer,
        approve=True,
        comment="Looks good - tests pass, logic is clean.",
    )

    # 7. Merge
    repo.merge_pr(pr, squash=True)

    # 8. Show updated history
    repo.log()

    return pr


def demonstrate_sync_before_commit(repo: GitRepo) -> None:
    """
    ID: ACT-003
    Purpose: Show the correct sync-before-push pattern.
    Inputs:  repo - GitRepo, currently on a feature branch
    """
    step("SYNC", "Syncing with remote before pushing...", colour=YELLOW)
    repo.fetch()
    repo.rebase("main")
    explain(
        "Always fetch the latest remote state and rebase your branch onto "
        "origin/main before pushing. This avoids diverged histories and "
        "makes the eventual merge trivial."
    )


def demonstrate_stash_workflow(repo: GitRepo, filename: str) -> None:
    """
    ID: ACT-004
    Purpose: Show stash save/switch/restore pattern.
    Inputs:
        repo     - GitRepo
        filename - str, file to dirty before stashing
    """
    repo.write(filename, "# work in progress - not ready to commit")
    repo.status()
    repo.stash()
    repo.status()
    repo.stash_pop()
    repo.status()
