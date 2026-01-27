from mcp.server import Server
from mcp.types import TextContent, Tool

async def hello(name: str):
    return TextContent(f"Hello, {name}! This is Tiangan MCP.")

server = Server(
    name="tiangan-mcp",
    tools=[
        Tool(
            name="hello",
            description="Say hello",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
            handler=hello,
        )
    ],
)

if __name__ == "__main__":
    server.run()

