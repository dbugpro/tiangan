from mcp.server import Server
from mcp.types import TextContent

server = Server("tiangan-mcp")

@server.tool()
def hello(name: str) -> TextContent:
    return TextContent(f"Hello, {name}! This is Tiangan MCP.")

if __name__ == "__main__":
    server.run()
