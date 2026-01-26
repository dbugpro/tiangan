import subprocess
import sys

def run_cli(command):
    """Run a tiangan CLI command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )
    return result.returncode, result.stdout, result.stderr


def assert_ok(exit_code, stdout, stderr, context):
    """Fail with a clear message if a CLI ritual misbehaves."""
    if exit_code != 0:
        raise AssertionError(
            f"CLI ritual failed during: {context}\n"
            f"Exit code: {exit_code}\n"
            f"STDOUT:\n{stdout}\n"
            f"STDERR:\n{stderr}"
        )


def test_imports():
    """Ensure the Python wrapper imports cleanly."""
    import tiangan
    import dbugtools


def test_help():
    """Ensure the CLI responds to --help."""
    exit_code, stdout, stderr = run_cli("tiangan --help")
    assert_ok(exit_code, stdout, stderr, "tiangan --help")
    if "Usage" not in stdout and "usage" not in stdout:
        raise AssertionError("CLI help text missing expected content.")


def test_basic_rituals():
    """
    Test a minimal ritual invocation.
    Adjust the command if your CLI uses subcommands like:
        tiangan ritual greet
        tiangan ritual sync
        tiangan ritual cast
    """
    exit_code, stdout, stderr = run_cli("tiangan ritual --list")
    assert_ok(exit_code, stdout, stderr, "tiangan ritual --list")

    # Basic sanity check: rituals should produce some output
    if not stdout.strip():
        raise AssertionError("Ritual list returned no output.")


if __name__ == "__main__":
    # Run tests manually if needed
    test_imports()
    test_help()
    test_basic_rituals()
    print("All tiangan CLI tests passed.")

