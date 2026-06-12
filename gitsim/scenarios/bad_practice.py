"""
File: gitsim/scenarios/bad_practice.py

ID: SCN-007
Purpose: Demonstrate bad Git practices with clear explanations of why each
         is dangerous and what the correct alternative is.
Rationale: Understanding what NOT to do is as important as knowing best practice.
"""

from gitsim.repo import GitRepo
from gitsim.explain import section
from gitsim.utils import hr, explain, step, warning, success, CYAN, RED, GREEN


def run(repo: GitRepo) -> None:
    """
    ID: SCN-008
    Purpose: Execute the bad practices scenario.
    Inputs:  repo - GitRepo, with existing commits on main
    Postconditions: All bad practices demonstrated with correct alternatives shown.
    """
    section("SCENARIO 4 - Bad Practices (What NOT To Do)")
    explain(
        "This scenario deliberately shows dangerous anti-patterns. "
        "Each bad practice is immediately followed by the correct alternative "
        "and an explanation of the real-world consequences."
    )

    # ------------------------------------------------------------------
    # Bad Practice 1: Committing directly to main
    # ------------------------------------------------------------------
    step("BAD", "Developer commits directly to main", colour=RED)
    repo.checkout("main")
    repo.direct_main_commit()

    # What should have happened
    step("GOOD", "Correct approach: create a branch first", colour=GREEN)
    explain(
        "CORRECT: git checkout -b fix/whatever && git commit ... && open PR\n"
        "Direct commits to main bypass ALL safety checks. On a real repo, "
        "branch protection rules will REJECT the push with: "
        "'error: remote: refusing to allow a force-push to a protected branch'"
    )

    hr()

    # ------------------------------------------------------------------
    # Bad Practice 2: Force push to shared branch
    # ------------------------------------------------------------------
    step("BAD", "Developer force-pushes to a shared branch", colour=RED)
    repo.checkout_new("feature/shared-work")
    repo.write("src/shared.py", "# teammate's work")
    repo.stage("src/shared.py")
    repo.commit("feat: shared feature")
    repo.push()

    repo.force_push()

    step("GOOD", "Correct approach: git push --force-with-lease (own branch only)", colour=GREEN)
    explain(
        "git push --force-with-lease is safer than --force because it checks "
        "that you have seen the latest remote commits before overwriting. "
        "Even so, never force-push to a branch other developers are working on."
    )

    hr()

    # ------------------------------------------------------------------
    # Bad Practice 3: Giant commit with everything
    # ------------------------------------------------------------------
    step("BAD", "Developer stages every file and makes one giant commit", colour=RED)
    repo.checkout("main")
    repo.pull()
    repo.checkout_new("feature/too-much-in-one-commit")

    repo.write("src/a.py", "feature A")
    repo.write("src/b.py", "feature B - unrelated")
    repo.write("src/c.py", "fix for bug C - also unrelated")

    # Stage all three - bad practice
    for f in ["src/a.py", "src/b.py", "src/c.py"]:
        repo._staged[f] = repo._working[f]

    warning("Staging EVERYTHING with 'git add .' - this is usually wrong")
    explain(
        "Staging all files indiscriminately with 'git add .' creates commits "
        "that mix unrelated concerns. This makes code review harder, makes "
        "git bisect less useful, and pollutes the history. "
        "Stage each logical change separately."
    )

    step("GOOD", "Correct approach: one logical change per commit", colour=GREEN)
    explain(
        "CORRECT:\n"
        "  git add src/a.py && git commit -m 'feat: add feature A'\n"
        "  git add src/b.py && git commit -m 'feat: add feature B'\n"
        "  (open separate PR for bug C)\n"
        "Each commit should represent one atomic, reviewable change."
    )

    hr()

    # ------------------------------------------------------------------
    # Bad Practice 4: Vague commit messages
    # ------------------------------------------------------------------
    step("BAD", "Vague commit messages that explain nothing", colour=RED)
    warning("Examples of terrible commit messages:")
    print("  - 'fix'")
    print("  - 'stuff'")
    print("  - 'changes'")
    print("  - 'wip'")
    print("  - 'asdfghjk'")
    print()
    explain(
        "Vague messages make git log, git blame, and git bisect useless. "
        "When a bug is found 6 months from now, nobody can tell which commit "
        "introduced it or why any change was made."
    )

    step("GOOD", "Correct approach: descriptive conventional commits", colour=GREEN)
    print("  + feat(api): add storm severity endpoint with 1-5 scoring")
    print("  + fix(parser): handle None input - prevents NullPointerError")
    print("  + refactor(service): extract severity logic to WeatherService")
    print("  + chore(deps): upgrade pytest 7.x -> 8.x")
    print()
    explain(
        "Use Conventional Commits format: type(scope): description\n"
        "Types: feat, fix, refactor, docs, test, chore, perf, ci\n"
        "Subject: imperative mood, max 72 chars, no period at end\n"
        "Body (optional): explain WHY, reference issue numbers"
    )

    hr()

    # ------------------------------------------------------------------
    # Bad Practice 5: Never syncing with remote
    # ------------------------------------------------------------------
    step("BAD", "Developer pushes without fetching first - diverged history", colour=RED)
    warning("Your branch and 'origin/main' have diverged.")
    warning("2 and 3 different commits each, respectively.")
    explain(
        "If you never run 'git fetch' + 'git rebase', your branch diverges "
        "from main. The PR will show unnecessary noise, conflict risk grows, "
        "and the merge becomes painful. This is preventable."
    )

    step("GOOD", "Correct approach: always fetch+rebase before pushing", colour=GREEN)
    explain(
        "CORRECT workflow before EVERY push:\n"
        "  git fetch origin\n"
        "  git rebase origin/main\n"
        "  git push\n"
        "This keeps your branch always up to date with zero divergence."
    )

    hr()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    section("Bad Practices Summary")
    print(f"  {RED}BAD{GREEN}  ->  GOOD{' '*30}{chr(27)}[0m")
    hr()
    pairs = [
        ("Commit to main directly", "Branch + PR + review"),
        ("git push --force on shared", "git push --force-with-lease (own branch only)"),
        ("git add . (everything)", "git add -p (intentional staging)"),
        ("Vague commit messages", "Conventional Commits: type(scope): desc"),
        ("Never fetch/rebase",      "fetch + rebase before every push"),
        ("Long-lived feature branches", "Small, short-lived branches merged often"),
    ]
    for bad, good in pairs:
        print(f"  {RED}[-]{chr(27)}[0m {bad:<40} {GREEN}[+]{chr(27)}[0m {good}")
    print()
