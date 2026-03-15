# authentik-mcp

MCP server for [Authentik](https://goauthentik.io/) identity provider.

## Install

```
uvx --extra-index-url https://nikitatsym.github.io/authentik-mcp/simple authentik-mcp
```

## Configure

```json
{
  "mcpServers": {
    "authentik": {
      "command": "uvx",
      "args": ["--refresh", "--extra-index-url", "https://nikitatsym.github.io/authentik-mcp/simple", "authentik-mcp"],
      "env": {
        "AUTHENTIK_URL": "https://auth.example.com",
        "AUTHENTIK_TOKEN": "your-api-token"
      }
    }
  }
}
```

**Where to paste:**
- **Claude Desktop** — `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Cursor** — `.cursor/mcp.json` in your project
- **Claude Code** — `~/.claude.json` top-level `mcpServers`

Or use the [setup wizard](https://nikitatsym.github.io/authentik-mcp/) to generate the config.

## Getting an API token

Authentik admin panel → Directory → Tokens and App passwords → Create with API scope.

## Groups

| Tool | Description |
|------|-------------|
| `authentik_read` | Users, groups, apps, tokens, providers, outposts, crypto, RBAC (read-only) |
| `authentik_write` | Create/update core resources (non-destructive) |
| `authentik_delete` | Delete operations across all domains (destructive) |
| `authentik_flows_read` | Flows, stages, policies, sources, events (read-only) |
| `authentik_flows_write` | Create/update auth pipeline config (non-destructive) |
| `authentik_admin` | Admin settings, system info, lifecycle |

Call any group with `operation="help"` to list available operations.
