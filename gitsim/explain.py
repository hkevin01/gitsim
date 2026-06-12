"""
File: gitsim/explain.py

ID: EXP-001
Purpose: High-level narrative explanations printed between simulation steps.
         Provides the "instructor voice" that contextualises each Git concept.
Requirement: Each explanation must be accurate, concise, and self-contained.
"""

from gitsim.utils import banner, explain, hr, CYAN, YELLOW, RED, GREEN


def intro() -> None:
    """ID: EXP-002 - Print the overall simulator introduction."""
    banner("GitSim - Git Workflow Simulator", colour=CYAN)
    explain(
        "Welcome to GitSim. This simulator reproduces real Git behaviour "
        "entirely in-memory - no actual git commands are run. Every step "
        "prints the equivalent Git command and explains WHY it is used. "
        "By the end you will have seen: branches, staging, commits, PRs, "
        "merge conflicts, rebasing, bad practices, and full history views."
    )


def section(title: str) -> None:
    """ID: EXP-003 - Print a scenario section header."""
    banner(title, colour=YELLOW)


def scenario_intro(name: str, description: str) -> None:
    """ID: EXP-004 - Introduce a named scenario with a description."""
    print()
    hr("=")
    explain(f"SCENARIO: {name}")
    explain(description)
    hr()


def outro() -> None:
    """ID: EXP-005 - Print the closing summary."""
    banner("Simulation Complete", colour=GREEN)
    explain(
        "You have now seen the complete professional Git workflow: "
        "feature branches, intentional staging, meaningful commits, "
        "pull requests, code review, squash merges, conflict resolution, "
        "rebasing, and why direct commits to main are forbidden. "
        "Apply these practices on every project."
    )
    print("  Key takeaways:")
    print("  1. Every task = its own branch, branched from up-to-date main")
    print("  2. Stage intentionally with git add -p")
    print("  3. Commit messages explain WHY, not what")
    print("  4. Always fetch + rebase before pushing")
    print("  5. PRs require review + CI pass before merging")
    print("  6. Squash merge keeps main history clean")
    print("  7. Delete branches after merging")
    print("  8. Never force-push to shared branches")
    print()
