#!/usr/bin/env python3
"""
Test script to verify the main.py CLI functionality works as expected.
"""

import subprocess
import sys
import os


def run_command(cmd):
    """Run a command and return the output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1


def test_cli():
    """Test the CLI functionality."""
    print("Testing CLI functionality...")

    # Test help command
    stdout, stderr, code = run_command("python src/cli/main.py --help")
    if code != 0:
        print(f"❌ Help command failed: {stderr}")
        return False
    print("✅ Help command works")

    # Test adding a task
    stdout, stderr, code = run_command("python src/cli/main.py add 'Test Task' 'Test Description'")
    if code != 0 or "Task added successfully" not in stdout:
        print(f"❌ Add task failed: {stderr}")
        return False
    print("✅ Add task works:", stdout)

    # Test listing tasks
    stdout, stderr, code = run_command("python src/cli/main.py list")
    if code != 0 or "Test Task" not in stdout:
        print(f"❌ List tasks failed: {stderr}")
        return False
    print("✅ List tasks works:", stdout.split('\n')[3] if len(stdout.split('\n')) > 3 else stdout)

    # Test updating a task
    stdout, stderr, code = run_command("python src/cli/main.py update 1 'Updated Task' 'Updated Description'")
    if code != 0 or "Task 1 updated successfully" not in stdout:
        print(f"❌ Update task failed: {stderr}")
        return False
    print("✅ Update task works:", stdout)

    # Test marking complete
    stdout, stderr, code = run_command("python src/cli/main.py complete 1")
    if code != 0 or "Task 1 marked as complete" not in stdout:
        print(f"❌ Mark complete failed: {stderr}")
        return False
    print("✅ Mark complete works:", stdout)

    # Test marking incomplete
    stdout, stderr, code = run_command("python src/cli/main.py incomplete 1")
    if code != 0 or "Task 1 marked as incomplete" not in stdout:
        print(f"❌ Mark incomplete failed: {stderr}")
        return False
    print("✅ Mark incomplete works:", stdout)

    # Test deleting a task
    stdout, stderr, code = run_command("python src/cli/main.py delete 1")
    if code != 0 or "Task 1 deleted successfully" not in stdout:
        print(f"❌ Delete task failed: {stderr}")
        return False
    print("✅ Delete task works:", stdout)

    # Test error handling - non-existent task
    stdout, stderr, code = run_command("python src/cli/main.py delete 999")
    if code == 0 or "does not exist" not in stdout:
        print(f"❌ Error handling failed: Expected error for non-existent task")
        return False
    print("✅ Error handling works:", stdout)

    # Test validation - empty title
    stdout, stderr, code = run_command("python src/cli/main.py add '' 'This should fail'")
    if code == 0 or "Title cannot be empty" not in stdout:
        print(f"❌ Validation failed: Expected error for empty title")
        return False
    print("✅ Validation works:", stdout)

    print("\n🎉 All tests passed! The CLI application is working correctly.")
    return True


if __name__ == "__main__":
    success = test_cli()
    if not success:
        sys.exit(1)
    print("\n✅ Main.py file testing completed successfully!")