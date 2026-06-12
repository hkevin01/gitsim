"""
File: gitsim/scenarios/rebase_example.py

ID: SCN-005
Purpose: Demonstrate rebasing - standard rebase onto main and interactive
         rebase to clean up messy commit history.
"""

from gitsim.repo import GitRepo
from gitsim.explain import section
from gitsim.utils import hr, explain, step, CYAN, YELLOW


def run(repo: GitRepo) -> None:
    """
    ID: SCN-006
    Purpose: Execute the rebase scenario.
    Inputs:  repo - GitRepo, with existing commits on main
    Postconditions: Feature branch rebased onto main; history cleaned up.
    """
    section("SCENARIO 3 - Rebasing")
    explain(
        "Rebase is the tool that keeps history linear. Instead of creating "
        "merge bubbles, rebase replays your commits on top of the latest main. "
        "The result is a clean, readable history as if you had branched today."
    )

    # ------------------------------------------------------------------
    # Setup: main advances while developer works
    # ------------------------------------------------------------------
    repo.checkout("main")
    repo.write("src/config.py", "DEBUG = False\nVERSION = '1.0.0'")
    repo.stage("src/config.py")
    repo.commit("chore: add config module")

    # Developer branches and starts working
    repo.checkout_new("feature/wind-chill-calculator")
    repo.write("src/wind_chill.py", "def wind_chill(temp, wind): return temp - wind * 0.1")
    repo.stage("src/wind_chill.py")
    repo.commit("feat: add wind chill calculation")

    hr()

    # Meanwhile main gets a new commit (teammate merged their PR)
    step("STEP", "Teammate merges their PR - main has advanced", colour=YELLOW)
    repo.checkout("main")
    repo.write("src/config.py", "DEBUG = False\nVERSION = '1.1.0'\nMAX_PLANETS = 100")
    repo.stage("src/config.py")
    repo.commit("chore: bump version to 1.1.0")

    hr()

    # Developer's branch is now behind main
    step("STEP", "Developer's branch is now 1 commit behind main", colour=YELLOW)
    explain(
        "The developer's feature branch was created from commit X on main. "
        "Now main has moved to commit X+1. If the developer pushes and opens "
        "a PR now, the diff will include an outdated base. Rebase fixes this."
    )

    # Rebase onto main
    repo.checkout("feature/wind-chill-calculator")
    repo.fetch()
    repo.rebase("main")

    explain(
        "After rebasing, the feature branch commits are replayed on top of "
        "the latest main commit. The feature branch now includes ALL recent "
        "main changes AND the new feature work - perfectly linear."
    )

    repo.push()
    pr = repo.open_pr(
        "feat: add wind chill calculator",
        reviewers=["Zara"],
    )
    repo.review_pr(pr, "Zara", approve=True)
    repo.merge_pr(pr, squash=True)

    hr()

    # ------------------------------------------------------------------
    # Interactive rebase: clean up messy commits before PR
    # ------------------------------------------------------------------
    section("SCENARIO 3b - Interactive Rebase (Cleaning Commits)")
    explain(
        "A developer made several small, messy commits while exploring. "
        "Before opening a PR, they use interactive rebase to squash and "
        "reword the commits into clean, professional history."
    )

    repo.checkout("main")
    repo.pull()
    repo.checkout_new("feature/refactor-weather")

    # Messy commits
    repo.write("src/weather.py", "# v1 draft")
    repo.stage("src/weather.py")
    repo.commit("wip: first attempt")

    repo.write("src/weather.py", "# v2 draft - better")
    repo.stage("src/weather.py")
    repo.commit("fix: oops forgot something")

    repo.write("src/weather.py", "def weather(p): return {'planet': p}")
    repo.stage("src/weather.py")
    repo.commit("finally works")

    step("STEP", "Before opening PR - cleaning up 3 messy commits", colour=YELLOW)
    repo.log(limit=5)
    repo.interactive_rebase(n=3)
    explain(
        "After interactive rebase the 3 messy commits become 1 clean commit: "
        "'refactor(api): simplify weather module'. The PR reviewer sees a "
        "professional, readable history instead of development noise."
    )

    repo.push()
    pr2 = repo.open_pr("refactor: simplify weather module", reviewers=["Hemmer"])
    repo.review_pr(pr2, "Hemmer", approve=True,
                   comment="Clean commit history - easy to review.")
    repo.merge_pr(pr2, squash=True)
    repo.log(limit=8)
