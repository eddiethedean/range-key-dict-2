#!/usr/bin/env bash
# Run all example scripts
# Usage: ./run_all.sh

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set PYTHONPATH to include project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

echo "=================================="
echo "Running all range-key-dict-2 examples"
echo "=================================="
echo

# Run each example
for script in "$SCRIPT_DIR"/0*.py; do
    if [ -f "$script" ]; then
        echo "▶️  Running $(basename "$script")..."
        echo
        python "$script"
        echo
        echo "✅ $(basename "$script") completed successfully!"
        echo
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo
    fi
done

echo
echo "🎉 All examples completed successfully!"

