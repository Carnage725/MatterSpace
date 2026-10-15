"""
mcp_server.py - exposes local project memory to Claude Code via MCP.

Requires: pip install mcp

Register in Claude Code (e.g. in .mcp.json or via `claude mcp add`):
    command: python
    args: ["/absolute/path/to/mcp_server.py"]
"""

from mcp.server.mcpserver import MCPServer
from store import LocalStore

mcp = MCPServer("project-memory")
store = LocalStore()


@mcp.tool()
def remember(fact: str, project_id: str) -> str:
    """Save a durable fact, decision, convention, or gotcha about a project
    so future sessions can recall it. Keep facts short and self-contained,
    e.g. 'Uses pnpm, not npm' or 'Decided against Mongo, went with Postgres
    because of relational queries in reporting.'"""
    return store.remember(fact, project_id)


@mcp.tool()
def recall(query: str, project_id: str, top_k: int = 5) -> list[str]:
    """Retrieve memories relevant to a query for a given project."""
    return store.recall(query, project_id, top_k)


@mcp.tool()
def list_memories(project_id: str) -> list[str]:
    """List all stored memories for a project (useful at session start)."""
    return store.list_all(project_id)


if __name__ == "__main__":
    mcp.run()
