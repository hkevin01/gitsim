"""
File: gitsim/scenarios/feature_branch.py

ID: SCN-001
Purpose: Demonstrate the complete feature branch workflow from branch creation
         through PR merge, including staging, committing, syncing, and review.
"""

from gitsim.repo import GitRepo
from gitsim.explain import section, scenario_intro
from gitsim.utils import hr, explain, step, CYAN


def run(repo: GitRepo) -> None:
    """
    ID: SCN-002
    Purpose: Execute the feature branch scenario.
    Inputs:  repo - GitRepo, already initialised with at least one commit on main
    Postconditions: Two features merged into main via PRs.
    """
    section("SCENARIO 1 - Feature Branch Workflow")
    explain(
        "A developer starts a new feature. They branch from main, make "
        "intentional commits, sync with remote, open a PR, get reviewed, "
        "and squash-merge. This is the gold-standard workflow."
    )

    # ------------------------------------------------------------------
    # Setup: put some initial content on main
    # ------------------------------------------------------------------
    repo.write("src/weather.py", "def get_weather(planet): return None")
    repo.stage("src/weather.py")
    repo.commit("chore: bootstrap weather module")
    repo.add_remote("origin")
    repo.push("main")

    hr()

    # ------------------------------------------------------------------
    # Feature 1: add storm endpoint
    # ------------------------------------------------------------------
    step("STEP", "Developer starts feature/add-storm-endpoint", colour=CYAN)

    repo.checkout("main")
    repo.pull()
    repo.checkout_new("feature/add-storm-endpoint")

    repo.write(
        "src/weather.py",
        "def get_weather(planet): return None\n"
        "def get_storm(planet): return {'severity': 3, 'wind': 120}",
    )
    repo.stage_patch("src/weather.py")
    repo.commit("feat(api): add storm endpoint with severity scoring")

    # Write a second file - unstaged intentionally to show status
    repo.write("src/notes.txt", "TODO: add tests for storm endpoint")
    repo.status()

    explain(
        "Notice 'notes.txt' is NOT staged. The developer chose not to include "
        "it in this commit. Intentional staging means your commit contains "
        "exactly what you intend - nothing more, nothing less."
    )

    repo.fetch()
    repo.rebase("main")
    repo.push()

    pr1 = repo.open_pr(
        "feat: add storm endpoint with severity scoring",
        reviewers=["Hemmer", "Zara"],
    )
    repo.review_pr(pr1, "Hemmer", approve=False,
                   comment="Please add input validation for planet name.")
    repo.write(
        "src/weather.py",
        "def get_weather(planet):\n"
        "    if not planet: raise ValueError('planet required')\n"
        "    return None\n"
        "def get_storm(planet):\n"
        "    if not planet: raise ValueError('planet required')\n"
        "    return {'severity': 3, 'wind': 120}",
    )
    repo.stage("src/weather.py")
    repo.commit("fix: add input validation per review feedback")
    repo.push()

    repo.review_pr(pr1, "Hemmer", approve=True,
                   comment="Validation added. LGTM.")
    repo.review_pr(pr1, "Zara", approve=True)
    repo.merge_pr(pr1, squash=True)
    repo.log()

    hr()

    # ------------------------------------------------------------------
    # Feature 2: stash demo mid-task
    # ------------------------------------------------------------------
    step("STEP", "Developer interrupts work to fix urgent bug - uses git stash", colour=CYAN)

    repo.checkout("main")
    repo.pull()
    repo.checkout_new("feature/add-forecast-endpoint")

    repo.write("src/forecast.py", "# forecast WIP\ndef forecast(planet, days): pass")
    repo.status()

    explain(
        "Urgent bug report comes in! The developer needs to switch branches "
        "but has uncommitted work. Instead of committing a WIP state, they stash."
    )

    repo.stash()
    repo.checkout("main")

    # Hotfix on separate branch
    repo.checkout_new("hotfix/fix-null-planet")
    repo.write("src/weather.py",
               "def get_weather(planet):\n    assert planet, 'planet required'\n    return {}")
    repo.stage("src/weather.py")
    repo.commit("fix: guard null planet in get_weather")
    pr_hot = repo.open_pr("hotfix: null planet guard", reviewers=["Zara"])
    repo.review_pr(pr_hot, "Zara", approve=True)
    repo.merge_pr(pr_hot, squash=True)

    # Back to forecast feature
    repo.checkout("feature/add-forecast-endpoint")
    repo.stash_pop()
    repo.stage_patch("src/forecast.py")
    repo.commit("feat(api): add forecast endpoint skeleton")
    repo.push()

    pr2 = repo.open_pr("feat: add forecast endpoint", reviewers=["Hemmer"])
    repo.review_pr(pr2, "Hemmer", approve=True)
    repo.merge_pr(pr2, squash=True)
    repo.log(limit=12)
