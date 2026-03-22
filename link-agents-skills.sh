#!/bin/bash

# Script to link agents and skills from awesome-copilot to local .github/
# Run this script from the root of any git repository to set up symlinks
# to the agents and skills from https://github.com/github/awesome-copilot

set -e

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Clone awesome-copilot if not exists
AWESOME_DIR=".github/awesome-copilot"
if [ ! -d "$AWESOME_DIR" ]; then
    echo "Cloning awesome-copilot..."
    git clone https://github.com/github/awesome-copilot "$AWESOME_DIR"
else
    echo "awesome-copilot already cloned, updating..."
    cd "$AWESOME_DIR"
    git pull
    cd - > /dev/null
fi

# Create .github directory if it doesn't exist
mkdir -p .github

# Create symlinks
if [ ! -L .github/agents ]; then
    ln -s ../awesome-copilot/agents .github/agents
    echo "Created symlink .github/agents"
else
    echo ".github/agents symlink already exists"
fi

if [ ! -L .github/skills ]; then
    ln -s ../awesome-copilot/skills .github/skills
    echo "Created symlink .github/skills"
else
    echo ".github/skills symlink already exists"
fi

echo "Done! Agents and skills are now linked to your repository."