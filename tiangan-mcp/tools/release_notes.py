from fastmcp.tools import MCPTool
import subprocess

class GenerateReleaseNotes(MCPTool):
    name: str = "generate_release_notes"
    description: str = "Generate release notes from git commits."

    async def run(self, tag: str = "HEAD") -> str:
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

