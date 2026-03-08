"""Skill storage — filesystem + JSON registry."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from skills_as_mcp.parser import parse_skill_md


_DEFAULT_DIR = Path.home() / ".skills-as-mcp"


class SkillStore:
    """Manages skill files and registry metadata."""

    def __init__(self, base_dir: Path | str | None = None):
        self._base = Path(base_dir) if base_dir else _DEFAULT_DIR
        self._skills_dir = self._base / "skills"
        self._registry_path = self._base / "registry.json"
        self._ensure_dirs()

    def _ensure_dirs(self):
        self._skills_dir.mkdir(parents=True, exist_ok=True)
        if not self._registry_path.exists():
            self._write_registry({"skills": {}})

    def _read_registry(self) -> dict:
        return json.loads(self._registry_path.read_text())

    def _write_registry(self, data: dict):
        self._registry_path.write_text(json.dumps(data, indent=2, default=str))

    def save(self, content: str, source_url: str = "") -> str:
        """Parse and save a SKILL.md. Returns the skill name."""
        parsed = parse_skill_md(content)

        # Write SKILL.md file
        skill_dir = self._skills_dir / parsed.name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content)

        # Update registry
        registry = self._read_registry()
        registry["skills"][parsed.name] = {
            "name": parsed.name,
            "description": parsed.description,
            "source_url": source_url,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "enabled": True,
            "license": parsed.license,
            "compatibility": parsed.compatibility,
            "metadata": parsed.metadata,
        }
        self._write_registry(registry)
        return parsed.name

    def get(self, name: str) -> dict | None:
        """Get skill registry entry by name."""
        registry = self._read_registry()
        return registry["skills"].get(name)

    def get_content(self, name: str) -> str | None:
        """Read the full SKILL.md content for a skill."""
        path = self._skills_dir / name / "SKILL.md"
        if not path.exists():
            return None
        return path.read_text()

    def list_skills(self, enabled_only: bool = False) -> list[dict]:
        """List all skills, optionally filtered to enabled only."""
        registry = self._read_registry()
        skills = list(registry["skills"].values())
        if enabled_only:
            skills = [s for s in skills if s.get("enabled", True)]
        return sorted(skills, key=lambda s: s["name"])

    def remove(self, name: str) -> bool:
        """Remove a skill. Returns True if it existed."""
        registry = self._read_registry()
        if name not in registry["skills"]:
            return False
        del registry["skills"][name]
        self._write_registry(registry)

        skill_dir = self._skills_dir / name
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        return True

    def set_enabled(self, name: str, enabled: bool) -> bool:
        """Enable or disable a skill. Returns True if skill exists."""
        registry = self._read_registry()
        if name not in registry["skills"]:
            return False
        registry["skills"][name]["enabled"] = enabled
        self._write_registry(registry)
        return True

    def search(self, query: str) -> list[dict]:
        """Search skills by name and description (case-insensitive)."""
        query_lower = query.lower()
        results = []
        for skill in self.list_skills():
            name = skill["name"].lower()
            desc = skill.get("description", "").lower()
            if query_lower in name or query_lower in desc:
                results.append(skill)
        return results
