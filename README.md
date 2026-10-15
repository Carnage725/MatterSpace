# MatterSpace

Local project memory for Claude Code, exposed over MCP. Facts are embedded with
`all-MiniLM-L6-v2` and stored in a local ChromaDB, so nothing leaves your machine.

## Tools

- `remember(fact, project_id)`: save a decision, convention or gotcha
- `recall(query, project_id, top_k=5)`: semantic search over a project's memories
- `list_memories(project_id)`: dump everything stored for a project

## Setup

```sh
uv venv && uv pip install -r requirements.txt
claude mcp add project-memory -s user -- "$PWD/.venv/bin/python" "$PWD/mcp_server.py"
```

Copy `CLAUDE.md.example` into a project as `CLAUDE.md` to tell Claude when to
use the tools. Data lives in `project_mem_store/` next to the code.
