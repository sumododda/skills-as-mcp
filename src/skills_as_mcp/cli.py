"""CLI commands for skills-as-mcp: install, list, remove, serve."""

from __future__ import annotations

import argparse
import os
import sys

import httpx

from skills_as_mcp.store import SkillStore
from skills_as_mcp.parser import ParseError


def _normalize_url(url: str) -> str:
    """Convert GitHub blob/gist URLs to raw content URLs."""
    import re

    m = re.match(r"^https?://github\.com/([^/]+)/([^/]+)/blob/(.+)$", url)
    if m:
        user, repo, path = m.group(1), m.group(2), m.group(3)
        return f"https://raw.githubusercontent.com/{user}/{repo}/{path}"

    m = re.match(r"^https?://gist\.github\.com/([^/]+)/([^/]+)/?$", url)
    if m:
        user, gist_id = m.group(1), m.group(2)
        return f"https://gist.githubusercontent.com/{user}/{gist_id}/raw"

    return url


def _get_store() -> SkillStore:
    base_dir = os.environ.get("SKILL_SHELF_DIR")
    return SkillStore(base_dir)


def cmd_install(args):
    """Install a skill from a URL or local file."""
    store = _get_store()

    for source in args.sources:
        # Local file
        if os.path.isfile(source):
            content = open(source).read()
            source_url = f"file://{os.path.abspath(source)}"
        # URL
        elif source.startswith("http://") or source.startswith("https://"):
            fetch_url = _normalize_url(source)
            try:
                resp = httpx.get(fetch_url, follow_redirects=True, timeout=30)
                resp.raise_for_status()
                content = resp.text
                source_url = source
            except httpx.HTTPError as e:
                print(f"  Error fetching {source}: {e}", file=sys.stderr)
                continue
        else:
            print(f"  Error: '{source}' is not a valid URL or file path", file=sys.stderr)
            continue

        try:
            name = store.save(content, source_url=source_url)
            skill = store.get(name)
            print(f"  Installed: {name} — {skill['description']}")
        except ParseError as e:
            print(f"  Error parsing {source}: {e}", file=sys.stderr)


def cmd_list(args):
    """List installed skills."""
    store = _get_store()
    skills = store.list_skills(enabled_only=args.enabled)

    if not skills:
        print("  No skills installed.")
        return

    for s in skills:
        status = "enabled" if s.get("enabled", True) else "disabled"
        marker = "+" if status == "enabled" else "-"
        print(f"  {marker} {s['name']}: {s.get('description', '')}")


def cmd_remove(args):
    """Remove an installed skill."""
    store = _get_store()
    if store.remove(args.name):
        print(f"  Removed: {args.name}")
    else:
        print(f"  Skill '{args.name}' not found.", file=sys.stderr)
        sys.exit(1)


def cmd_serve(args):
    """Run the MCP server (default behavior)."""
    from skills_as_mcp.server import main as serve_main
    serve_main()


def main():
    parser = argparse.ArgumentParser(
        prog="skills-as-mcp",
        description="MCP server for dynamic AI agent skill management",
    )
    sub = parser.add_subparsers(dest="command")

    # install
    p_install = sub.add_parser("install", help="Install skills from URLs or local files")
    p_install.add_argument("sources", nargs="+", help="URLs or file paths to SKILL.md files")
    p_install.set_defaults(func=cmd_install)

    # list
    p_list = sub.add_parser("list", aliases=["ls"], help="List installed skills")
    p_list.add_argument("--enabled", action="store_true", help="Only show enabled skills")
    p_list.set_defaults(func=cmd_list)

    # remove
    p_remove = sub.add_parser("remove", aliases=["rm"], help="Remove an installed skill")
    p_remove.add_argument("name", help="Skill name to remove")
    p_remove.set_defaults(func=cmd_remove)

    # serve (default)
    p_serve = sub.add_parser("serve", help="Run the MCP server (default)")
    p_serve.set_defaults(func=cmd_serve)

    args = parser.parse_args()

    # No subcommand → run MCP server (backward compatible)
    if args.command is None:
        cmd_serve(args)
    else:
        args.func(args)
