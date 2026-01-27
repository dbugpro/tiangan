from fastmcp import FastMCP
from tools.release_notes import generate_release_notes

app = FastMCP("tiangan-mcp")

app.add_tool(generate_release_notes)

app.run()
