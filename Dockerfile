# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS uv

# Install the project into /app
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the pyproject.toml to install dependencies
COPY pyproject.toml /app/pyproject.toml

# Install the project's dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv     uv pip install -r /app/pyproject.toml --no-dev --no-editable

# Then, add the rest of the project source code and install it
ADD src /app/src

# Environment variables
ENV CLIENT_ID = YourEbayClientID
ENV CLIENT_SECRET = YourEbayClientSceret

ENTRYPOINT ["uv", "run", "ebay-mcp"]
