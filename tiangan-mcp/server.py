from fastmcp import FastMCP
from tools.release_notes import GenerateReleaseNotes

app = FastMCP("tiangan-mcp")

app.add_tool(GenerateReleaseNotes())

app.run()
