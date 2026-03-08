"""Parse SKILL.md files following the agentskills.io specification."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml


# Name must be lowercase letters, numbers, hyphens. No leading/trailing/consecutive hyphens.
_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)", re.DOTALL)


class ParseError(Exception):
    """Raised when a SKILL.md file is invalid."""


@dataclass(frozen=True)
class SkillMetadata:
    """Parsed SKILL.md content."""

    name: str
    description: str
    body: str
    license: str = ""
    compatibility: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


def parse_skill_md(content: str) -> SkillMetadata:
    """Parse a SKILL.md string into structured metadata.

    Args:
        content: Raw SKILL.md file content.

    Returns:
        SkillMetadata with parsed fields.

    Raises:
        ParseError: If the file is missing required fields or has invalid format.
    """
    match = _FRONTMATTER_RE.match(content)
    if not match:
        raise ParseError("SKILL.md must start with YAML frontmatter (--- delimiters)")

    raw_yaml, body = match.group(1), match.group(2)

    try:
        front = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as e:
        raise ParseError(f"Invalid YAML in frontmatter: {e}") from e

    if not isinstance(front, dict):
        raise ParseError("Frontmatter must be a YAML mapping")

    name = front.get("name")
    if not name or not isinstance(name, str):
        raise ParseError("Frontmatter must include a 'name' field")
    if len(name) > 64 or not _NAME_RE.match(name):
        raise ParseError(
            f"Invalid name '{name}': must be lowercase letters, numbers, and hyphens, "
            "max 64 chars, no leading/trailing/consecutive hyphens"
        )

    description = front.get("description")
    if not description or not isinstance(description, str):
        raise ParseError("Frontmatter must include a 'description' field")
    if len(description) > 1024:
        raise ParseError("Description must be 1024 characters or fewer")

    meta = front.get("metadata", {})
    if not isinstance(meta, dict):
        meta = {}

    return SkillMetadata(
        name=name,
        description=description,
        body=body.strip(),
        license=str(front.get("license", "")),
        compatibility=str(front.get("compatibility", "")),
        metadata={str(k): str(v) for k, v in meta.items()},
    )
