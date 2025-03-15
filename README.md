# Ebay MCP server

Simple Ebay server that lets you fetch auctions from Ebay.com

Uses the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) to handle protocol communication and server interactions.

## Example

Let's you use prompts like, "Find me 10 auctions for batman comics"

## Components

### Tools

The server provides a single tool:

- list_auction: Scan ebay for auctions. This tool is helpful for finding auctions on ebay.
  - Required "query" argument for the search query
  - Optional "ammount" argument for ammount of results
    - defaults to 0
  - Returns result from Ebay's REST API

## Installation

### Requires [UV](https://github.com/astral-sh/uv) (Fast Python package and project manager)

If uv isn't installed.

```bash
# Using Homebrew on macOS
brew install uv
```

or

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Next, install the MCP server

```bash
# Install from source
uv pip install git+https://github.com/CooKey-Monster/EbayMcpServer.git
```

### Environment Variables

The following environment variable is required; you can find them on the [Ebay developer portal](https://developer.ebay.com/develop)

- `CLIENT_ID`: Your Ebay client ID
- `CLIENT_SECRET`: Your Ebay client secret
