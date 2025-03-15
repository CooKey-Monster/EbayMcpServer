import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl
import logging

from ebayAPItool import get_access_token, make_ebay_api_request

server = Server("mcp-ebay-server")
logger = logging.getLogger("mcp-ebay-server")
logger.setLevel(logging.INFO)


## Logging
@server.set_logging_level()
async def set_logging_level(level: types.LoggingLevel) -> types.EmptyResult:
    logger.setLevel(level.upper())
    await server.request_context.session.send_log_message(
        level="info", data=f"Log level set to {level}", logger="mcp-ebay-server"
    )
    return types.EmptyResult()


## Tools
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available search tools.
    """
    return [
        types.Tool(
            name="list-auction",
            description="Scan ebay for auctions. This tool is helpful for finding auctions on ebay.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search on ebay. This should just be a name not a description.",
                    },
                    "ammount": {
                        "type": "integer",
                        "description": "The ammount of results to fetch. This should be a whole non negative number.",

                    },
                },
                "required": ["query", "ammount"],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle search tool execution requests.
    """
    if name != "list-auction":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    query = arguments.get("query")

    ammount = arguments.get("ammount")

    if not query:
        raise ValueError("Missing query")

    if not ammount:
        ammount = 1


    CLIENT_ID = "Your Ebay Client ID"          # App ID (Client ID)
    CLIENT_SECRET = "Clint Secret"             # Make a Ebay dev acc to get these
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    search_response = make_ebay_api_request(access_token, query, ammount)

    return [
        types.TextContent(
            type="text",
            text=str(search_response),
        )
    ]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-ebay-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
