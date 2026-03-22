# Contributing to gh-copilot-linker

Thank you for your interest in contributing to gh-copilot-linker! This document provides guidelines and instructions for contributing.

## Workflow

1. **Create a branch** for your feature or fix
2. **Make commits** using [Conventional Commits](#conventional-commits) style
3. **Create a Pull Request** to merge your changes into `main`
4. **Pass CI checks** including commit linting and tests
5. **Get reviewed** and merge your PR
6. **Automated Release** - Once merged, an automated release workflow will:
   - Analyze conventional commits
   - Bump the version number
   - Generate changelog
   - Create a release tag
   - Publish to PyPI

## Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) to standardize commit messages. This enables automated versioning and changelog generation.

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding or updating tests
- **chore**: Changes to build process, dependencies, etc.
- **ci**: Changes to CI/CD configuration
- **revert**: Revert a previous commit

### Examples

```
feat: add --url option for custom repositories

fix: resolve symlink creation on Windows

docs: update README with new usage examples

chore: update dependencies
```

## Version Management

Version numbers follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for breaking changes
- **MINOR** version for new features
- **PATCH** version for bug fixes

The version is automatically bumped based on conventional commit types:
- `feat:` commits → MINOR version bump
- `fix:` commits → PATCH version bump
- `BREAKING CHANGE:` footer → MAJOR version bump

## Setting Up Your Environment

```bash
# Clone the repository
git clone https://github.com/msandeep12/gh-agent-sync.git
cd gh-agent-sync

# Install in development mode
pip install -e .

# Install development dependencies
pip install commitlint
```

## Before Submitting

1. Ensure your commits follow [Conventional Commits](#conventional-commits) style
2. Run tests locally
3. Update documentation if needed
4. Check that your branch is up to date with `main`

## Pull Request Process

1. Create a PR with a clear description of your changes
2. Reference any related issues
3. Ensure all CI checks pass
4. Wait for review and address any feedback
5. Merge will trigger automated release workflow

## Code Quality

- Write clean, readable code
- Add tests for new features
- Update documentation
- Follow PEP 8 style guide
- Include type hints where appropriate

## Questions?

Feel free to open an issue if you have questions about contributing!
