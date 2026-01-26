import subprocess
import sys
import json

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


# -----------------------------
# Ritual Discovery & Listing
# -----------------------------

def test_ritual_list():
    """Ensure rituals can be listed."""
    exit_code, stdout, stderr = run_cli("tiangan ritual --list")
    assert_ok(exit_code, stdout, stderr, "tiangan ritual --list")

    rituals = stdout.strip().splitlines()
    if not rituals:
        raise AssertionError("No rituals returned by ritual list.")

    # Basic sanity: rituals should have names
    if not any(len(r.strip()) > 0 for r in rituals):
        raise AssertionError("Ritual list output appears empty or malformed.")


# -----------------------------
# Ritual Invocation
# -----------------------------

def test_invoke_sample_ritual():
    """
    Test invoking a ritual.
    Adjust 'greet' to match one of your real rituals.
    """
    exit_code, stdout, stderr = run_cli("tiangan ritual invoke greet --name test-user")
    assert_ok(exit_code, stdout, stderr, "tiangan ritual invoke greet")

    if "test-user" not in stdout:
        raise AssertionError("Ritual invocation did not include expected output.")


def test_invoke_ritual_missing_args():
    """Ensure missing arguments produce a helpful error."""
    exit_code, stdout, stderr = run_cli("tiangan ritual invoke greet")
    if exit_code == 0:
        raise AssertionError("Ritual invocation without args should fail.")

    if "missing" not in stderr.lower() and "required" not in stderr.lower():
        raise AssertionError("Missing-argument error message not informative.")


# -----------------------------
# Messageboard Interactions
# -----------------------------

def test_messageboard_post():
    """Ensure posting to the shared messageboard works."""
    exit_code, stdout, stderr = run_cli(
        "tiangan board post --message 'hello-world'"
    )
    assert_ok(exit_code, stdout, stderr, "tiangan board post")

    if "posted" not in stdout.lower():
        raise AssertionError("Messageboard post did not confirm success.")


def test_messageboard_fetch():
    """Ensure fetching messages works."""
    exit_code, stdout, stderr = run_cli("tiangan board fetch --limit 1")
    assert_ok(exit_code, stdout, stderr, "tiangan board fetch")

    if not stdout.strip():
        raise AssertionError("Messageboard fetch returned no messages.")


# -----------------------------
# Dashboard / Settings
# -----------------------------

def test_dashboard_show_settings():
    """Ensure dashboard settings can be displayed."""
    exit_code, stdout, stderr = run_cli("tiangan dashboard show")
    assert_ok(exit_code, stdout, stderr, "tiangan dashboard show")

    # Expect JSON or key-value pairs
    if "{" not in stdout and ":" not in stdout:
        raise AssertionError("Dashboard settings output appears malformed.")


def test_dashboard_set_setting():
    """Ensure a setting can be updated."""
    exit_code, stdout, stderr = run_cli(
        "tiangan dashboard set theme dark"
    )
    assert_ok(exit_code, stdout, stderr, "tiangan dashboard set theme")

    if "updated" not in stdout.lower():
        raise AssertionError("Dashboard setting update did not confirm success.")


# -----------------------------
# Error Handling
# -----------------------------

def test_unknown_command():
    """Ensure unknown commands produce a helpful error."""
    exit_code, stdout, stderr = run_cli("tiangan ritual summon-dragon")
    if exit_code == 0:
        raise AssertionError("Unknown command should not succeed.")

    if "unknown" not in stderr.lower() and "invalid" not in stderr.lower():
        raise AssertionError("Unknown-command error message not informative.")


# -----------------------------
# Manual Execution
# -----------------------------

if __name__ == "__main__":
    test_imports()
    test_help()
    test_ritual_list()
    test_invoke_sample_ritual()
    test_invoke_ritual_missing_args()
    test_messageboard_post()
    test_messageboard_fetch()
    test_dashboard_show_settings()
    test_dashboard_set_setting()
    test_unknown_command()
    print("All expanded tiangan CLI ritual tests passed.")


