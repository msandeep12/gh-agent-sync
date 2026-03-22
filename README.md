# Copilot Linker

A cross-platform Python utility to link agents and skills from the [awesome-copilot](https://github.com/github/awesome-copilot) repository to any local git repository.

## Installation

Install from source:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

From PyPI (once published):

```bash
pip install gh-agent-sync
```

## Usage

Run the utility from the root of your git repository:

### Link Agents and Skills

```bash
gh-agent-sync link
```

Or specify a custom repository:

```bash
gh-agent-sync link --url https://github.com/your-org/your-agents-repo
```

This will:
- Clone or update the awesome-copilot repository into `.github/awesome-copilot`
- Create symbolic links (or copies if symlinks fail) to `.github/agents` and `.github/skills`
- Add the linked paths to `.gitignore` to prevent them from being committed

### Undo Linking

```bash
gh-agent-sync undo
```

This will:
- Remove the `.github/agents` and `.github/skills` directories
- Remove the cloned `.github/awesome-copilot` repository

## Development

### Building

To build the package:

```bash
python -m build
```

### Publishing

1. Create a release on GitHub
2. The CI/CD workflow will automatically build and publish to PyPI

Make sure to set up PyPI API tokens in the repository secrets if needed.

## What it does

- Checks if the current directory is a git repository
- Clones or updates the awesome-copilot repository into `.github/awesome-copilot`
- Creates symbolic links (or copies if symlinks fail):
  - `.github/agents` → `.github/awesome-copilot/agents`
  - `.github/skills` → `.github/awesome-copilot/skills`
- Adds linked paths to `.gitignore`

This allows you to use the agents and skills from awesome-copilot in your repository without copying the files directly.

## Requirements

- Python 3.8+
- Git
- Internet connection for cloning the repository

## Notes

- On systems where symlinks are not supported or require special permissions, the utility will fall back to copying the directories.
- The utility creates links/copies, so changes in the awesome-copilot repo will be reflected in your links (after updating with `git pull` in the cloned directory).

## Architecture

### MCP Integration

This tool uses a **Model Context Protocol (MCP)** based git server for all git operations. This provides:

- Type-safe git operations
- Better error handling
- Easier testing and mocking
- Potential for distributed git operations
- Integration with AI agents via MCP

The `GitMCPServer` class in `src/gh_agent_sync/git_mcp.py` provides standardized interfaces for:
- `is_git_repo()` - Check if in a git repository
- `clone()` - Clone a repository
- `pull()` - Pull updates
- `add()` - Stage files
- `commit()` - Commit changes
- `push()` - Push to remote

## Contributing

We use a pull request workflow with automated versioning and release management. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- How to create pull requests
- Conventional commit message style
- Automated versioning and release process

All commits should follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.
