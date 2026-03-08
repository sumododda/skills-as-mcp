"""skills-as-mcp MCP server."""

from fastmcp import FastMCP

mcp = FastMCP(
    name="skills-as-mcp",
    instructions=(
        "Manages AI agent skills. Use install_skill to add skills from URLs, "
        "list_skills to see what's available, get_skill to read a skill's full "
        "instructions, and search_skills to find skills by keyword."
    ),
)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
