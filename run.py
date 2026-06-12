"""
File: run.py

ID: RUN-001
Purpose: Main entry point for the GitSim simulator.
         Instantiates a GitRepo and runs all four scenarios in sequence.
Requirement: Runnable with `python run.py` from the project root.
Usage:
    python run.py              # run all scenarios
    python run.py --scenario 1 # run only scenario 1 (1=feature, 2=conflict, 3=rebase, 4=bad)
Side Effects: Writes to stdout only. No filesystem mutations. No git commands.
"""

import sys
import argparse

from gitsim.repo import GitRepo
from gitsim.explain import intro, outro
from gitsim.scenarios import feature_branch, merge_conflict, rebase_example, bad_practice
from gitsim.utils import banner, explain, CYAN, GREEN


def parse_args() -> argparse.Namespace:
    """
    ID: RUN-002
    Purpose: Parse CLI arguments.
    Outputs: Namespace with .scenario (int or None) and .pause (bool)
    """
    p = argparse.ArgumentParser(
        description="GitSim - Git workflow simulator (no real git required)"
    )
    p.add_argument(
        "--scenario", "-s",
        type=int,
        choices=[1, 2, 3, 4],
        default=None,
        help="Run a single scenario: 1=feature, 2=conflict, 3=rebase, 4=bad-practice",
    )
    return p.parse_args()


def main() -> int:
    """
    ID: RUN-003
    Purpose: Orchestrate the full simulation run.
    Inputs:  CLI args via parse_args()
    Outputs: int exit code (0 = success)
    Preconditions: Python >= 3.10 (dataclasses, match syntax not used but annotations need it).
    Postconditions: All selected scenarios have run; output written to stdout.
    Failure Modes: Any unhandled exception returns exit code 1.
    """
    args = parse_args()

    intro()

    # Each scenario gets its own fresh repo to avoid state leakage
    scenarios = {
        1: ("Feature Branch Workflow",   feature_branch.run),
        2: ("Merge Conflict Resolution", merge_conflict.run),
        3: ("Rebasing",                  rebase_example.run),
        4: ("Bad Practices",             bad_practice.run),
    }

    selected = [args.scenario] if args.scenario else [1, 2, 3, 4]

    for num in selected:
        name, fn = scenarios[num]
        repo = GitRepo("GalacticWeather", author="Dev")
        repo.init()
        try:
            fn(repo)
        except Exception as exc:
            print(f"\n[ERROR] Scenario {num} failed: {exc}")
            raise

    outro()
    return 0


if __name__ == "__main__":
    sys.exit(main())
