#!/usr/bin/env python3
"""
Copilot Linker - Link agents and skills from awesome-copilot to local .github/
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return True if successful."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        return False


def is_git_repo():
    """Check if current directory is a git repository."""
    return run_command("git rev-parse --git-dir")


def clone_or_update_awesome_copilot(repo_url):
    """Clone or update the awesome-copilot repository."""
    awesome_dir = Path(".github/awesome-copilot")
    repo_url = repo_url

    if awesome_dir.exists():
        print("Updating repository...")
        return run_command("git pull", cwd=awesome_dir)
    else:
        print("Cloning repository...")
        return run_command(f"git clone {repo_url} {awesome_dir}")


def create_link_or_copy(source, target):
    """Create a symlink or copy if symlink fails."""
    source = Path(source)
    target = Path(target)

    if target.exists():
        print(f"{target} already exists")
        return True

    try:
        # Try to create symlink
        os.symlink(source, target, target_is_directory=True)
        print(f"Created symlink: {target} -> {source}")
        return True
    except OSError as e:
        print(f"Symlink failed ({e}), copying instead...")
        try:
            shutil.copytree(source, target)
            print(f"Copied: {source} -> {target}")
            return True
        except Exception as e:
            print(f"Copy failed: {e}")
            return False


def remove_link(target):
    """Remove a link or copy."""
    target = Path(target)
    if target.exists():
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        print(f"Removed {target}")
    else:
        print(f"{target} does not exist")


def add_to_gitignore():
    """Add linked paths to .gitignore."""
    gitignore = Path(".gitignore")
    entries = [".github/agents", ".github/skills"]

    if gitignore.exists():
        with open(gitignore, "r") as f:
            content = f.read()
    else:
        content = ""

    added = False
    for entry in entries:
        if entry not in content:
            content += f"\n{entry}"
            added = True

    if added:
        with open(gitignore, "w") as f:
            f.write(content)
        print("Added entries to .gitignore")


def link(repo_url):
    """Link agents and skills."""
    # Ensure .github directory exists
    Path(".github").mkdir(exist_ok=True)

    # Clone/update repository
    if not clone_or_update_awesome_copilot(repo_url):
        print("Failed to clone/update repository")
        sys.exit(1)

    # Create links
    awesome_dir = Path(".github/awesome-copilot")

    success = True
    success &= create_link_or_copy(awesome_dir / "agents", Path(".github/agents"))
    success &= create_link_or_copy(awesome_dir / "skills", Path(".github/skills"))

    if success:
        add_to_gitignore()
        print("Done! Agents and skills are now linked to your repository.")
    else:
        print("Some links failed to create.")
        sys.exit(1)


def undo():
    """Undo the linking."""
    remove_link(".github/agents")
    remove_link(".github/skills")

    # Remove cloned repo
    awesome_dir = Path(".github/awesome-copilot")
    if awesome_dir.exists():
        shutil.rmtree(awesome_dir)
        print("Removed .github/awesome-copilot")

    print("Undo complete.")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Link or undo linking of agents and skills from a repository")
    parser.add_argument("command", choices=["link", "undo"], help="Command to run: link or undo")
    parser.add_argument("--url", default="https://github.com/github/awesome-copilot", help="URL of the repository containing agents and skills (default: awesome-copilot)")

    args = parser.parse_args()

    if not is_git_repo():
        print("Error: Not in a git repository")
        sys.exit(1)

    if args.command == "link":
        link(args.url)
    elif args.command == "undo":
        undo()


if __name__ == "__main__":
    main()