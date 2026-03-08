"""Shared test fixtures for skills-as-mcp."""

import json
import pytest
from pathlib import Path


SAMPLE_SKILL_MD = """\
---
name: weather
description: Get current weather for any city using web search.
metadata:
  author: test
  version: "1.0"
---

# Weather Skill

## When to Use
When the user asks about weather conditions.

## Instructions
1. Ask for the city name
2. Search for current weather
3. Return temperature and conditions
"""

MINIMAL_SKILL_MD = """\
---
name: minimal
description: A minimal test skill.
---

Do the minimal thing.
"""


@pytest.fixture
def tmp_shelf(tmp_path):
    """Create a temporary skills-as-mcp directory."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps({"skills": {}}))
    return tmp_path


@pytest.fixture
def sample_skill_md():
    return SAMPLE_SKILL_MD


@pytest.fixture
def minimal_skill_md():
    return MINIMAL_SKILL_MD
