#!/usr/bin/env python3
"""
Copilot Linker - Link agents and skills from awesome-copilot to local .github/
"""

import os
import sys
import shutil
import argparse
import tempfile
from pathlib import Path
from .git_mcp import GitMCPServer


def is_git_repo():
    """Check if current directory is a git repository."""
    return GitMCPServer.is_git_repo()


def clone_or_update_awesome_copilot(repo_url):
    """Clone the repository to a temporary directory and return the path.
    
    This uses a temporary directory to keep the project directory clean.
    The full repository is not stored in the project.
    """
    temp_dir = tempfile.mkdtemp(prefix="gh-agent-sync-")
    temp_path = Path(temp_dir)
    
    print(f"Cloning repository to temporary directory...")
    success, message = GitMCPServer.clone(repo_url, str(temp_path))
    if not success:
        print(f"Error: {message}")
        shutil.rmtree(temp_path, ignore_errors=True)
        return None
    else:
        print(message)
    
    return temp_path


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

    # Clone repository to temporary directory
    temp_repo = clone_or_update_awesome_copilot(repo_url)
    if not temp_repo:
        print("Failed to clone repository")
        sys.exit(1)

    try:
        # Create links from temporary directory
        success = True
        success &= create_link_or_copy(temp_repo / "agents", Path(".github/agents"))
        success &= create_link_or_copy(temp_repo / "skills", Path(".github/skills"))

        if success:
            add_to_gitignore()
            print("Done! Agents and skills are now linked to your repository.")
        else:
            print("Some links failed to create.")
            sys.exit(1)
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_repo, ignore_errors=True)
        print(f"Cleaned up temporary directory")


def undo():
    """Undo the linking."""
    remove_link(".github/agents")
    remove_link(".github/skills")
    
    print("Undo complete. The agents and skills links have been removed.")


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
