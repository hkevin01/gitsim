"""
File: gitsim/scenarios/branching_strategy.py

ID: SCN-009
Purpose: Demonstrate the full corporate Git branching strategy used on large
         multi-developer projects. Shows the complete branch hierarchy:
         main -> release -> develop -> feature, hotfix, bugfix, test, and
         release-candidate branches - each with correct naming conventions
         and merge targets.

Requirement: Reproduce the branch lifecycle a developer would encounter on
             a real enterprise project with 10-100+ contributors.
Rationale:   Single-developer workflows hide the complexity of branch
             management. This scenario shows the full picture so learners
             understand why the naming conventions exist and what each
             branch tier's rules are.
Side Effects: Writes to stdout only. No filesystem mutations.
"""

from gitsim.repo import GitRepo
from gitsim.explain import section
from gitsim.utils import hr, explain, step, warning, success, CYAN, YELLOW, GREEN, BLUE, RED


def run(repo: GitRepo) -> None:
    """
    ID: SCN-010
    Purpose: Execute the corporate branching strategy scenario.
    Inputs:  repo - GitRepo, already initialised with root commit on main
    Postconditions: Full branch hierarchy demonstrated with correct naming,
                    merge targets, and lifecycle rules shown for each tier.
    Failure Modes: Raises if repo is uninitialised.
    Verification: Run with python run.py --scenario 5
    """
    section("SCENARIO 5 - Corporate Branching Strategy")
    explain(
        "Large engineering teams use a structured branch hierarchy so that "
        "dozens of developers can work simultaneously without stepping on each "
        "other. This scenario walks through the full branch tree: the permanent "
        "long-lived branches (main, develop, release) and the short-lived "
        "work branches (feature, bugfix, hotfix, test, release-candidate). "
        "Every branch name follows a convention so the purpose is clear at a "
        "glance in any git log or pull request list."
    )

    # ------------------------------------------------------------------
    # TIER 0 - main (production)
    # ------------------------------------------------------------------
    step("BRANCH-TIER-0", "main  ->  production-ready, always deployable", colour=CYAN)
    explain(
        "The 'main' branch (sometimes called 'master' in older repos) "
        "represents the exact code that is running in production right now. "
        "It is ALWAYS in a deployable state. Direct pushes are blocked by "
        "branch protection rules. The ONLY way code reaches main is via a "
        "fully approved, CI-green pull request from a release branch or a "
        "hotfix branch. Nothing else ever merges to main."
    )

    repo.checkout("main")
    repo.write("src/app.py", "# v1.0.0 - production release\nVERSION = '1.0.0'")
    repo.stage("src/app.py")
    repo.commit("chore: bootstrap v1.0.0 production baseline")
    repo.add_remote("origin")
    repo.push("main")

    hr()

    # ------------------------------------------------------------------
    # TIER 1 - develop (integration)
    # ------------------------------------------------------------------
    step("BRANCH-TIER-1", "develop  ->  integration branch, next release assembles here", colour=CYAN)
    explain(
        "The 'develop' branch is the main integration target for all completed "
        "feature work. It represents the state of the next release - everything "
        "that is done but not yet shipped to production. Feature branches are "
        "merged into develop via PRs. Develop should pass all automated tests "
        "at all times, but it is NOT the same stability bar as main. When a "
        "sprint or milestone is complete, develop is merged into a release "
        "branch for final hardening."
    )

    repo.checkout("main")
    repo.checkout_new("develop")
    repo.write("src/app.py", "# v1.1.0-dev\nVERSION = '1.1.0-dev'")
    repo.stage("src/app.py")
    repo.commit("chore: open develop branch for v1.1.0 sprint")
    repo.push()

    hr()

    # ------------------------------------------------------------------
    # TIER 2 - Individual developer feature branches
    # Naming: feature/<ticket-id>-<short-description>
    # ------------------------------------------------------------------
    step("BRANCH-TIER-2", "Individual developer feature branches", colour=CYAN)
    explain(
        "Every unit of work - no matter how small - gets its own branch. "
        "The naming convention is: feature/<ticket-id>-<short-kebab-description>. "
        "Including the ticket ID makes it trivial to find the branch from a "
        "JIRA/Linear/GitHub issue and vice versa. The description makes it "
        "readable in a branch list without having to look up the ticket. "
        "Feature branches are always created FROM develop (not main) and "
        "always merged BACK INTO develop via a pull request."
    )

    # Developer 1 - Alice - working on ticket PROJ-142
    step("DEV", "Alice: git checkout -b feature/PROJ-142-user-authentication develop", colour=GREEN)
    repo.checkout("develop")
    repo.checkout_new("feature/PROJ-142-user-authentication")
    repo.write("src/auth.py",
               "# PROJ-142: JWT-based user authentication\n"
               "def login(username, password): ...\n"
               "def logout(token): ...\n"
               "def verify_token(token): ...")
    repo.stage_patch("src/auth.py")
    repo.commit("feat(auth): PROJ-142 add JWT login and token verification")
    repo.push()

    pr_alice = repo.open_pr(
        "feat(auth): PROJ-142 user authentication with JWT",
        reviewers=["Bob", "Carol"],
    )
    repo.review_pr(pr_alice, "Bob", approve=False,
                   comment="PROJ-142: token expiry not handled - add exp claim check")
    repo.write("src/auth.py",
               "# PROJ-142: JWT-based user authentication\n"
               "import time\n"
               "def login(username, password): ...\n"
               "def logout(token): ...\n"
               "def verify_token(token):\n"
               "    if token.get('exp', 0) < time.time(): raise PermissionError('expired')")
    repo.stage("src/auth.py")
    repo.commit("fix(auth): PROJ-142 add token expiry check per review")
    repo.push()
    repo.review_pr(pr_alice, "Bob", approve=True, comment="Expiry handled. LGTM.")
    repo.review_pr(pr_alice, "Carol", approve=True)
    repo.merge_pr(pr_alice, squash=True)

    explain(
        "Alice's feature/PROJ-142-user-authentication branch is now merged "
        "into develop via a squash merge. The feature branch is deleted. "
        "The single squash commit on develop carries the ticket ID so it is "
        "traceable back to the original requirement."
    )

    hr()

    # Developer 2 - Bob - working on ticket PROJ-157 in parallel
    step("DEV", "Bob: git checkout -b feature/PROJ-157-password-reset develop", colour=GREEN)
    repo.checkout("develop")
    repo.checkout_new("feature/PROJ-157-password-reset")
    repo.write("src/auth.py",
               "# PROJ-157: password reset flow\n"
               "def request_reset(email): ...\n"
               "def confirm_reset(token, new_password): ...")
    repo.stage_patch("src/auth.py")
    repo.commit("feat(auth): PROJ-157 add password reset request and confirm")
    repo.push()
    pr_bob = repo.open_pr(
        "feat(auth): PROJ-157 password reset via email token",
        reviewers=["Alice"],
    )
    repo.review_pr(pr_bob, "Alice", approve=True, comment="Clean. LGTM.")
    repo.merge_pr(pr_bob, squash=True)

    hr()

    # ------------------------------------------------------------------
    # TIER 2 - bugfix branches
    # Naming: bugfix/<ticket-id>-<short-description>
    # ------------------------------------------------------------------
    step("BRANCH-TIER-2", "bugfix branches - non-critical bugs found in develop", colour=CYAN)
    explain(
        "A bugfix branch is used for non-critical bugs discovered during "
        "development or QA testing - bugs that exist in develop but have NOT "
        "yet reached production (main). The naming convention is: "
        "bugfix/<ticket-id>-<short-description>. Like feature branches, "
        "bugfix branches are created FROM develop and merged BACK INTO develop. "
        "They are different from hotfix branches, which target production bugs."
    )

    repo.checkout("develop")
    repo.checkout_new("bugfix/PROJ-163-login-race-condition")
    repo.write("src/auth.py",
               "# bugfix PROJ-163: login race condition under concurrent requests\n"
               "import threading\n"
               "_lock = threading.Lock()\n"
               "def login(username, password):\n"
               "    with _lock:\n"
               "        pass  # serialise concurrent login attempts")
    repo.stage("src/auth.py")
    repo.commit("fix(auth): PROJ-163 serialise concurrent login with threading.Lock")
    repo.push()
    pr_bug = repo.open_pr(
        "bugfix: PROJ-163 login race condition under load",
        reviewers=["Alice", "Bob"],
    )
    repo.review_pr(pr_bug, "Alice", approve=True)
    repo.merge_pr(pr_bug, squash=True)

    hr()

    # ------------------------------------------------------------------
    # TIER 2 - test / qa branches
    # Naming: test/<ticket-or-sprint>-<description>
    # ------------------------------------------------------------------
    step("BRANCH-TIER-2", "test/qa branches - integration and regression test suites", colour=CYAN)
    explain(
        "Test branches (also called qa/ branches in some teams) are created "
        "when QA engineers or developers need to author or update test suites "
        "independently of feature work. They follow the same naming pattern: "
        "test/<sprint-or-ticket>-<description>. Test branches target develop "
        "as their merge destination. Some teams also use a dedicated 'qa' "
        "long-lived branch that mirrors develop and is deployed to a QA "
        "environment automatically on every merge."
    )

    repo.checkout("develop")
    repo.checkout_new("test/PROJ-sprint-22-auth-integration-tests")
    repo.write("tests/test_auth.py",
               "# Sprint 22 integration tests for authentication module\n"
               "def test_login_returns_token(): ...\n"
               "def test_expired_token_rejected(): ...\n"
               "def test_reset_flow_end_to_end(): ...")
    repo.stage("tests/test_auth.py")
    repo.commit("test(auth): PROJ-sprint-22 add integration tests for auth module")
    repo.push()
    pr_test = repo.open_pr(
        "test: PROJ-sprint-22 auth integration test suite",
        reviewers=["Carol"],
    )
    repo.review_pr(pr_test, "Carol", approve=True)
    repo.merge_pr(pr_test, squash=True)

    hr()

    # ------------------------------------------------------------------
    # TIER 1 - release branch (final hardening before production)
    # Naming: release/<version>
    # ------------------------------------------------------------------
    step("BRANCH-TIER-1", "release/1.1.0  ->  final hardening, last gate before main", colour=YELLOW)
    explain(
        "When develop is stable and the sprint is complete, a release branch "
        "is cut from develop. The naming convention is release/<version-number>, "
        "for example release/1.1.0 or release/2024-Q3. On the release branch, "
        "ONLY bug fixes are allowed - no new features. The release branch is "
        "deployed to a staging environment for final acceptance testing. Once "
        "the release is signed off, it is merged into BOTH main (to ship to "
        "production) AND back into develop (to carry the fixes forward). This "
        "double-merge ensures develop never diverges from what is in production."
    )

    repo.checkout("develop")
    repo.checkout_new("release/1.1.0")
    repo.write("src/app.py", "# v1.1.0 release candidate\nVERSION = '1.1.0'")
    repo.stage("src/app.py")
    repo.commit("chore(release): bump version to 1.1.0 for release branch")
    repo.push()

    # Last-minute bug found during acceptance testing
    step("FIX", "Acceptance test finds a bug - fix directly on release branch", colour=YELLOW)
    repo.checkout_new("bugfix/PROJ-171-token-header-case")
    repo.write("src/auth.py",
               "# bugfix PROJ-171: accept both 'Authorization' and 'authorization' headers\n"
               "def get_token(headers):\n"
               "    return headers.get('Authorization') or headers.get('authorization')")
    repo.stage("src/auth.py")
    repo.commit("fix(auth): PROJ-171 normalise Authorization header case")
    repo.push()
    pr_rel_fix = repo.open_pr(
        "bugfix: PROJ-171 header case normalisation for release/1.1.0",
        reviewers=["Bob"],
    )
    repo.review_pr(pr_rel_fix, "Bob", approve=True)
    repo.merge_pr(pr_rel_fix, squash=True)

    explain(
        "The bug fix is merged into the release branch. After final sign-off, "
        "the release branch is merged to main (ships to production) and also "
        "back-merged into develop so the fix is not lost. In GitSim we show "
        "the merge to main via a PR - in practice this is often automated by "
        "the CD pipeline on release branch approval."
    )

    # Merge release to main
    repo.checkout("release/1.1.0")
    pr_to_main = repo.open_pr(
        "release: merge release/1.1.0 into main - v1.1.0 ship",
        reviewers=["Carol", "Alice"],
    )
    repo.review_pr(pr_to_main, "Carol", approve=True)
    repo.merge_pr(pr_to_main, squash=False)

    hr()

    # ------------------------------------------------------------------
    # TIER 0 - hotfix (emergency production patch)
    # Naming: hotfix/<ticket-id>-<short-description>
    # ------------------------------------------------------------------
    step("BRANCH-TIER-0", "hotfix/PROJ-175-null-deref-crash  ->  emergency production patch", colour=RED)
    explain(
        "A hotfix branch is the ONLY branch type that branches directly from "
        "main. It is used when a critical bug is discovered in production that "
        "cannot wait for the next release cycle. The naming convention is: "
        "hotfix/<ticket-id>-<short-description>. Hotfix branches are merged "
        "into BOTH main (to fix production immediately) AND develop (to ensure "
        "the fix is not overwritten by the next release). They are treated with "
        "the highest urgency and require the fastest possible review turnaround."
    )

    repo.checkout("main")
    repo.checkout_new("hotfix/PROJ-175-null-deref-crash-on-empty-token")
    repo.write("src/auth.py",
               "# HOTFIX PROJ-175: NullPointerException when token is None\n"
               "def verify_token(token):\n"
               "    if token is None: raise ValueError('token must not be None')\n"
               "    if token.get('exp', 0) < 0: raise PermissionError('expired')")
    repo.stage("src/auth.py")
    repo.commit("hotfix(auth): PROJ-175 guard None token in verify_token - prevents crash")
    repo.push()

    pr_hotfix = repo.open_pr(
        "HOTFIX: PROJ-175 null deref crash on empty token - URGENT",
        reviewers=["Carol", "Bob"],
    )
    repo.review_pr(pr_hotfix, "Carol", approve=True,
                   comment="Confirmed fix. This was causing 500s in prod. Approve.")
    repo.review_pr(pr_hotfix, "Bob", approve=True)
    repo.merge_pr(pr_hotfix, squash=True)

    success("Hotfix merged to main - production patch deployed")
    explain(
        "The hotfix is now on main and will be deployed immediately. The next "
        "step (not shown here) is to also merge this hotfix into develop so "
        "the fix is included in the next regular release. This is the only "
        "scenario where a branch from main bypasses the develop integration branch."
    )

    # ------------------------------------------------------------------
    # Final log - show the full branch tree
    # ------------------------------------------------------------------
    hr()
    step("LOG", "Full repository branch tree after all operations", colour=CYAN)
    repo.log(limit=20)

    explain(
        "The commit graph above shows the complete branch hierarchy. You can "
        "see: main (production), develop (integration), release/1.1.0 (final "
        "hardening), individual feature branches (feature/PROJ-*), bugfix "
        "branches (bugfix/PROJ-*), test branches (test/PROJ-sprint-*), and "
        "the emergency hotfix branch (hotfix/PROJ-175-*). Each branch tier "
        "has a clear purpose, a clear source, and a clear merge target. "
        "This structure scales to hundreds of developers because the rules "
        "are simple and enforced consistently."
    )
