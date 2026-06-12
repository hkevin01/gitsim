"""
File: gitsim/utils.py

ID: UTIL-001
Purpose: Terminal formatting helpers for the GitSim simulator.
         Provides coloured output, ASCII diff rendering, and log graph drawing.
Requirement: All output must be human-readable on a standard 80-col terminal.
Side Effects: Writes to stdout only.
"""

import textwrap
from datetime import datetime, timedelta
import random


# ---------------------------------------------------------------------------
# ANSI colour codes
# ---------------------------------------------------------------------------
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
ORANGE = "\033[38;5;208m"


def banner(text: str, colour: str = CYAN) -> None:
    """
    ID: UTIL-002
    Purpose: Print a bold section banner surrounded by a box.
    Inputs:  text - str, title; colour - ANSI colour code
    Outputs: None (prints to stdout)
    """
    width = 66
    line  = "=" * width
    print(f"\n{colour}{BOLD}{line}{RESET}")
    print(f"{colour}{BOLD}  {text}{RESET}")
    print(f"{colour}{BOLD}{line}{RESET}\n")


def step(tag: str, message: str, colour: str = GREEN) -> None:
    """
    ID: UTIL-003
    Purpose: Print a single simulation step line with a coloured tag.
    Inputs:  tag - str bracket label; message - str description
    """
    print(f"{colour}{BOLD}[{tag}]{RESET} {message}")


def explain(text: str, indent: int = 4) -> None:
    """
    ID: UTIL-004
    Purpose: Print a wrapped explanation block indented and dimmed.
    Inputs:  text - str, may be multi-line; indent - int spaces
    """
    prefix = " " * indent
    for line in textwrap.wrap(text.strip(), width=70):
        print(f"{DIM}{prefix}{line}{RESET}")
    print()


def diff_block(filename: str, before: list[str], after: list[str]) -> None:
    """
    ID: UTIL-005
    Purpose: Render a minimal unified diff between before and after lines.
    Inputs:
        filename - str, shown in diff header
        before   - list[str], original lines
        after    - list[str], modified lines
    Outputs: None (prints to stdout)
    """
    print(f"{BOLD}--- a/{filename}{RESET}")
    print(f"{BOLD}+++ b/{filename}{RESET}")
    print(f"{DIM}@@ -1,{len(before)} +1,{len(after)} @@{RESET}")
    for line in before:
        print(f"{RED}-{line}{RESET}")
    for line in after:
        print(f"{GREEN}+{line}{RESET}")
    print()


def conflict_block(filename: str, ours: str, theirs: str) -> None:
    """
    ID: UTIL-006
    Purpose: Render Git-style conflict markers for a file.
    Inputs:
        filename - str
        ours     - str, content from current branch
        theirs   - str, content from incoming branch
    """
    print(f"{YELLOW}{BOLD}# {filename} (CONFLICT){RESET}")
    print(f"{RED}<<<<<<< HEAD{RESET}")
    print(f"{RED}{ours}{RESET}")
    print(f"{YELLOW}======={RESET}")
    print(f"{GREEN}{theirs}{RESET}")
    print(f"{GREEN}>>>>>>> incoming{RESET}")
    print()


def log_graph(commits: list[dict]) -> None:
    """
    ID: UTIL-007
    Purpose: Render a simplified ASCII commit graph.
    Inputs:  commits - list of dicts with keys: hash, branch, message, author
    Outputs: None (prints to stdout)
    """
    symbols = {"main": "*", "feature": "o", "bugfix": "x", "hotfix": "!"}
    for i, c in enumerate(commits):
        branch_type = c.get("branch", "main").split("/")[0]
        sym = symbols.get(branch_type, "*")
        indent = "  " if c.get("branch") != "main" else ""
        connector = "|/" if i > 0 and c.get("branch") != "main" else "|"
        if i > 0:
            print(f"{DIM}{indent}{connector}{RESET}")
        tag = f"{CYAN}({c['branch']}){RESET}" if c.get("branch") else ""
        print(
            f"{YELLOW}{sym}{RESET} "
            f"{DIM}{c['hash'][:7]}{RESET} "
            f"{WHITE}{c['message'][:50]}{RESET} "
            f"{tag} "
            f"{DIM}<{c.get('author','dev')}>{RESET}"
        )
    print()


def make_hash() -> str:
    """
    ID: UTIL-008
    Purpose: Generate a plausible-looking fake commit hash.
    Outputs: str, 40-char hex string
    """
    return "".join(random.choices("0123456789abcdef", k=40))


def fake_timestamp(offset_hours: int = 0) -> str:
    """
    ID: UTIL-009
    Purpose: Return a fake ISO timestamp offset from a fixed base.
    Inputs:  offset_hours - int, hours to add to base time
    Outputs: str ISO-8601
    """
    base = datetime(2026, 6, 10, 9, 0, 0)
    return (base + timedelta(hours=offset_hours)).strftime("%Y-%m-%d %H:%M")


def warning(text: str) -> None:
    """Print a bold red warning line."""
    print(f"{RED}{BOLD}[WARNING]{RESET} {RED}{text}{RESET}")


def success(text: str) -> None:
    """Print a bold green success line."""
    print(f"{GREEN}{BOLD}[OK]{RESET} {GREEN}{text}{RESET}")


def hr(char: str = "-", width: int = 66) -> None:
    """Print a horizontal rule."""
    print(f"{DIM}{char * width}{RESET}")
