from mcp.server.fastmcp import tool
import subprocess

@tool
async def generate_release_notes(tag: str = "HEAD") -> str:
    """
    Generate release notes from git commits.
    """
    try:
        output = subprocess.check_output(
            ["git", "log", f"{tag}..HEAD", "--pretty=format:* %s"],
            text=True
        )
        if not output.strip():
            return f"No new commits found since {tag}."
        return f"Release notes since {tag}:\n\n{output}"
    except Exception as e:
        return f"Error generating release notes: {e}"
