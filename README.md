# Link Agents and Skills Script

This repository contains a shell script `link-agents-skills.sh` that can be used to link agents and skills from the [awesome-copilot](https://github.com/github/awesome-copilot) repository to any local git repository.

## Usage

1. Copy the `link-agents-skills.sh` script to the root of your git repository.
2. Run the script:

   ```bash
   ./link-agents-skills.sh
   ```

   Or if bash is not available:

   ```bash
   bash link-agents-skills.sh
   ```

## What it does

- Checks if the current directory is a git repository
- Clones or updates the awesome-copilot repository into `.github/awesome-copilot`
- Creates symbolic links:
  - `.github/agents` → `.github/awesome-copilot/agents`
  - `.github/skills` → `.github/awesome-copilot/skills`

This allows you to use the agents and skills from awesome-copilot in your repository without copying the files directly.

## Requirements

- Bash shell (available on Linux, macOS, or Windows with Git Bash/WSL)
- Git
- Internet connection for cloning the repository

## Notes

- On Windows, you may need to run this in Git Bash or WSL for symlink support.
- The script creates symlinks, so changes in the awesome-copilot repo will be reflected in your links (after updating with `git pull` in the cloned directory).