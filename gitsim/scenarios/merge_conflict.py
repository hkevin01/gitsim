"""
File: gitsim/scenarios/merge_conflict.py

ID: SCN-003
Purpose: Demonstrate merge conflicts - how they arise, what they look like,
         and the correct resolution workflow.
"""

from gitsim.repo import GitRepo
from gitsim.explain import section
from gitsim.utils import hr, explain, step, warning, CYAN, RED


def run(repo: GitRepo) -> None:
    """
    ID: SCN-004
    Purpose: Execute the merge conflict scenario.
    Inputs:  repo - GitRepo, initialised with content on main
    Postconditions: Conflict demonstrated and resolved; merged into main.
    """
    section("SCENARIO 2 - Merge Conflicts")
    explain(
        "Two developers work on the same file simultaneously. When both try "
        "to merge, Git detects a conflict because it cannot decide which "
        "version of the overlapping lines to keep."
    )

    # ------------------------------------------------------------------
    # Common base: both branches start from the same main commit
    # ------------------------------------------------------------------
    repo.checkout("main")
    repo.write("src/parser.py", "def parse(data):\n    return data.strip()")
    repo.stage("src/parser.py")
    repo.commit("chore: add parser module")

    hr()

    # ------------------------------------------------------------------
    # Branch A: Developer Hemmer adds null check
    # ------------------------------------------------------------------
    step("STEP", "Hemmer creates feature/a - adds null check to parse()", colour=CYAN)
    repo.checkout_new("feature/parser-null-check")
    repo.write(
        "src/parser.py",
        "def parse(data):\n    if data is None: return ''\n    return data.strip()",
    )
    repo.stage("src/parser.py")
    repo.commit("fix: handle None input in parse()")

    hr()

    # ------------------------------------------------------------------
    # Branch B: Developer Zara adds type validation
    # ------------------------------------------------------------------
    step("STEP", "Zara creates feature/b - adds type check to parse()", colour=CYAN)
    repo.checkout("main")
    repo.checkout_new("feature/parser-type-check")
    repo.write(
        "src/parser.py",
        "def parse(data):\n    if not isinstance(data, str): raise TypeError('str required')\n    return data.strip()",
    )
    repo.stage("src/parser.py")
    repo.commit("feat: add type validation to parse()")

    hr()

    # ------------------------------------------------------------------
    # Feature A merges first (no conflict)
    # ------------------------------------------------------------------
    step("STEP", "Hemmer's PR merges first - no conflict", colour=CYAN)
    pr_a = repo.open_pr(
        "fix: null check in parse()",
        reviewers=["Zara"],
        source="feature/parser-null-check",
    )
    repo.review_pr(pr_a, "Zara", approve=True)
    repo.merge_pr(pr_a, squash=True)

    hr()

    # ------------------------------------------------------------------
    # Feature B now conflicts with main
    # ------------------------------------------------------------------
    step("STEP", "Zara tries to merge - CONFLICT DETECTED", colour=RED)
    warning(
        "Zara's branch diverged from main after Hemmer's merge. "
        "The same lines in parser.py were changed differently."
    )

    repo.checkout("feature/parser-type-check")
    repo.simulate_conflict(
        "src/parser.py",
        ours="def parse(data):\n    if not isinstance(data, str): raise TypeError('str required')\n    return data.strip()",
        theirs="def parse(data):\n    if data is None: return ''\n    return data.strip()",
    )

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------
    step("STEP", "Zara resolves the conflict - combines both checks", colour=CYAN)
    resolved = (
        "def parse(data):\n"
        "    if data is None: return ''\n"
        "    if not isinstance(data, str): raise TypeError('str required')\n"
        "    return data.strip()"
    )
    repo.resolve_conflict("src/parser.py", resolved)
    repo.commit("fix: resolve conflict - combine null + type checks in parse()")
    repo.push()

    pr_b = repo.open_pr(
        "feat: type validation in parse() - conflict resolved",
        reviewers=["Hemmer"],
        source="feature/parser-type-check",
    )
    repo.review_pr(pr_b, "Hemmer", approve=True,
                   comment="Good resolution - both checks preserved.")
    repo.merge_pr(pr_b, squash=True)

    explain(
        "The resolved version combines BOTH developers' intent: null guard "
        "from Hemmer and type validation from Zara. Neither change was lost. "
        "Always communicate with teammates when resolving conflicts."
    )
    repo.log()
