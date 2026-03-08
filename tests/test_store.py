"""Tests for skill store."""

import json
import pytest
from skills_as_mcp.store import SkillStore
from skills_as_mcp.parser import SkillMetadata


class TestSkillStore:
    def test_save_and_get(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md, source_url="https://example.com/weather.md")

        skill = store.get("weather")
        assert skill is not None
        assert skill["name"] == "weather"
        assert skill["source_url"] == "https://example.com/weather.md"
        assert skill["enabled"] is True

    def test_get_content(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md, source_url="https://example.com/weather.md")

        content = store.get_content("weather")
        assert "# Weather Skill" in content

    def test_get_nonexistent_returns_none(self, tmp_shelf):
        store = SkillStore(tmp_shelf)
        assert store.get("nonexistent") is None

    def test_list_skills(self, tmp_shelf, sample_skill_md, minimal_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)
        store.save(minimal_skill_md)

        skills = store.list_skills()
        assert len(skills) == 2
        names = {s["name"] for s in skills}
        assert names == {"weather", "minimal"}

    def test_list_skills_empty(self, tmp_shelf):
        store = SkillStore(tmp_shelf)
        assert store.list_skills() == []

    def test_remove(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)
        assert store.get("weather") is not None

        removed = store.remove("weather")
        assert removed is True
        assert store.get("weather") is None
        # Skill directory should be deleted
        assert not (tmp_shelf / "skills" / "weather").exists()

    def test_remove_nonexistent(self, tmp_shelf):
        store = SkillStore(tmp_shelf)
        assert store.remove("nonexistent") is False

    def test_enable_disable(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)

        store.set_enabled("weather", False)
        skill = store.get("weather")
        assert skill["enabled"] is False

        store.set_enabled("weather", True)
        skill = store.get("weather")
        assert skill["enabled"] is True

    def test_search_by_name(self, tmp_shelf, sample_skill_md, minimal_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)
        store.save(minimal_skill_md)

        results = store.search("weather")
        assert len(results) == 1
        assert results[0]["name"] == "weather"

    def test_search_by_description(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)

        results = store.search("city")
        assert len(results) == 1
        assert results[0]["name"] == "weather"

    def test_search_case_insensitive(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)

        results = store.search("WEATHER")
        assert len(results) == 1

    def test_search_no_results(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)

        assert store.search("quantum computing") == []

    def test_list_only_enabled(self, tmp_shelf, sample_skill_md, minimal_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md)
        store.save(minimal_skill_md)
        store.set_enabled("minimal", False)

        enabled = store.list_skills(enabled_only=True)
        assert len(enabled) == 1
        assert enabled[0]["name"] == "weather"

    def test_overwrite_existing_skill(self, tmp_shelf, sample_skill_md):
        store = SkillStore(tmp_shelf)
        store.save(sample_skill_md, source_url="https://v1.com")
        store.save(sample_skill_md, source_url="https://v2.com")

        skill = store.get("weather")
        assert skill["source_url"] == "https://v2.com"
        # Should still only be one
        assert len(store.list_skills()) == 1

    def test_initializes_missing_directory(self, tmp_path):
        shelf_dir = tmp_path / "new-shelf"
        store = SkillStore(shelf_dir)
        store.save("---\nname: test\ndescription: test skill\n---\nbody")
        assert store.get("test") is not None
