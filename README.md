# skills-as-mcp

An MCP server for dynamic AI agent skill management. Install, search, and manage
[Agent Skills](https://agentskills.io) from any MCP client — Claude Code, Cursor,
Simba, or any tool that speaks MCP.

## What Makes This Different

Every existing solution assumes skills are local files you manually place. skills-as-mcp
lets your AI agent **install skills from URLs mid-conversation**:

```
You: "install this skill https://example.com/weather/SKILL.md"
Agent: calls install_skill(url="https://example.com/weather/SKILL.md")
Agent: "Weather skill installed. You now have weather lookup capabilities."
You: "what's the weather in Tokyo?"
Agent: reads skill://weather → follows instructions → answers
```

## Install

```bash
pip install skills-as-mcp
```

## Quick Start

### With Claude Code

Add to your MCP config (`.claude/settings.json` or `~/.claude.json`):

```json
{
  "mcpServers": {
    "skills-as-mcp": {
      "command": "skills-as-mcp"
    }
  }
}
```

### With Any MCP Client

```bash
# Run via stdio (default)
skills-as-mcp

# Run as HTTP server
skills-as-mcp --transport http --port 8000
```

### Storage

Skills are stored in `~/.skills-as-mcp/` by default. Override with:

```bash
export SKILL_SHELF_DIR=/path/to/shelf
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `install_skill(url?, content?)` | Install from URL or raw SKILL.md content |
| `list_skills(enabled_only?)` | List all installed skills |
| `get_skill(name)` | Read full SKILL.md instructions |
| `search_skills(query)` | Search by name/description |
| `remove_skill(name)` | Uninstall a skill |
| `enable_skill(name)` | Re-enable a disabled skill |
| `disable_skill(name)` | Disable without removing |

## MCP Resources

| URI | Description |
|-----|-------------|
| `skill://index` | Index of all enabled skills |
| `skill://{name}` | Full SKILL.md content for a skill |

## SKILL.md Format

Follows the [agentskills.io](https://agentskills.io/specification) open standard:

```yaml
---
name: my-skill
description: What this skill does and when to use it
license: MIT
compatibility: Requires internet access
metadata:
  author: your-name
  version: "1.0"
---

# My Skill

Instructions the agent reads and follows...
```

## Development

```bash
git clone https://github.com/sumo/skills-as-mcp.git
cd skills-as-mcp
pip install -e ".[dev]"
pytest -v
```

## License

MIT
