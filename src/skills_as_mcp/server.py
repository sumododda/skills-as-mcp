"""skills-as-mcp MCP server — dynamic AI agent skill management."""

from __future__ import annotations

import os

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from skills_as_mcp.parser import ParseError
from skills_as_mcp.store import SkillStore

_store: SkillStore | None = None


def _get_store() -> SkillStore:
    global _store
    if _store is None:
        base_dir = os.environ.get("SKILL_SHELF_DIR")
        _store = SkillStore(base_dir)
    return _store


def create_server(shelf_dir: str | None = None) -> FastMCP:
    """Create a skills-as-mcp MCP server instance.

    Args:
        shelf_dir: Override the storage directory (for testing).
    """
    global _store
    _store = SkillStore(shelf_dir)

    server = FastMCP(
        name="skills-as-mcp",
        instructions=(
            "Manages AI agent skills. Use install_skill to add skills from URLs or "
            "raw content, list_skills to see what's available, get_skill to read a "
            "skill's full instructions, and search_skills to find skills by keyword."
        ),
    )

    @server.tool
    async def install_skill(
        url: str = "",
        content: str = "",
    ) -> str:
        """Install a skill from a URL or raw SKILL.md content.

        Provide either a URL pointing to a SKILL.md file, or the raw content directly.
        The skill will be parsed, validated, and made available immediately.
        """
        store = _get_store()

        if not url and not content:
            raise ToolError("Provide either 'url' or 'content'.")

        source_url = url
        if url and not content:
            try:
                async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    content = resp.text
            except httpx.HTTPError as e:
                raise ToolError(f"Failed to fetch URL: {e}")

        try:
            name = store.save(content, source_url=source_url)
        except ParseError as e:
            raise ToolError(f"Invalid SKILL.md: {e}")

        skill = store.get(name)
        return f"Skill '{name}' installed successfully.\nDescription: {skill['description']}"

    @server.tool
    def list_skills(enabled_only: bool = False) -> str:
        """List all installed skills with their name, description, and status."""
        store = _get_store()
        skills = store.list_skills(enabled_only=enabled_only)

        if not skills:
            return "No skills installed."

        lines = []
        for s in skills:
            status = "enabled" if s.get("enabled", True) else "disabled"
            lines.append(f"- **{s['name']}** [{status}]: {s['description']}")
        return "\n".join(lines)

    @server.tool
    def get_skill(name: str) -> str:
        """Get the full SKILL.md content for a skill. Read this to learn how to use the skill."""
        store = _get_store()
        content = store.get_content(name)
        if content is None:
            raise ToolError(f"Skill '{name}' not found.")
        return content

    @server.tool
    def search_skills(query: str) -> str:
        """Search installed skills by keyword (matches name and description)."""
        store = _get_store()
        results = store.search(query)

        if not results:
            return f"No skills matching '{query}'."

        lines = [f"Found {len(results)} skill(s):"]
        for s in results:
            lines.append(f"- **{s['name']}**: {s['description']}")
        return "\n".join(lines)

    @server.tool
    def remove_skill(name: str) -> str:
        """Remove an installed skill permanently."""
        store = _get_store()
        if not store.remove(name):
            raise ToolError(f"Skill '{name}' not found.")
        return f"Skill '{name}' removed."

    @server.tool
    def enable_skill(name: str) -> str:
        """Enable a previously disabled skill."""
        store = _get_store()
        if not store.set_enabled(name, True):
            raise ToolError(f"Skill '{name}' not found.")
        return f"Skill '{name}' enabled."

    @server.tool
    def disable_skill(name: str) -> str:
        """Disable a skill without removing it. Disabled skills won't appear in enabled listings."""
        store = _get_store()
        if not store.set_enabled(name, False):
            raise ToolError(f"Skill '{name}' not found.")
        return f"Skill '{name}' disabled."

    return server


# Default server instance for CLI entry point
mcp = create_server()


def main():
    mcp.run()


if __name__ == "__main__":
    main()
