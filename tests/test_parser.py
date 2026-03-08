"""Tests for SKILL.md parser."""

import pytest
from skills_as_mcp.parser import parse_skill_md, SkillMetadata, ParseError


class TestParseSkillMd:
    def test_parses_valid_skill(self, sample_skill_md):
        result = parse_skill_md(sample_skill_md)
        assert result.name == "weather"
        assert result.description == "Get current weather for any city using web search."
        assert result.body.startswith("# Weather Skill")
        assert result.metadata == {"author": "test", "version": "1.0"}

    def test_parses_minimal_skill(self, minimal_skill_md):
        result = parse_skill_md(minimal_skill_md)
        assert result.name == "minimal"
        assert result.description == "A minimal test skill."
        assert result.body.strip() == "Do the minimal thing."
        assert result.metadata == {}

    def test_rejects_missing_frontmatter(self):
        with pytest.raises(ParseError, match="frontmatter"):
            parse_skill_md("# Just markdown\nNo frontmatter here.")

    def test_rejects_missing_name(self):
        md = "---\ndescription: has desc but no name\n---\nbody"
        with pytest.raises(ParseError, match="name"):
            parse_skill_md(md)

    def test_rejects_missing_description(self):
        md = "---\nname: no-desc\n---\nbody"
        with pytest.raises(ParseError, match="description"):
            parse_skill_md(md)

    def test_rejects_invalid_name_format(self):
        md = "---\nname: Invalid Name!!\ndescription: bad\n---\nbody"
        with pytest.raises(ParseError, match="name"):
            parse_skill_md(md)

    def test_accepts_hyphens_and_numbers(self):
        md = "---\nname: my-skill-2\ndescription: valid\n---\nbody"
        result = parse_skill_md(md)
        assert result.name == "my-skill-2"

    def test_extracts_optional_fields(self):
        md = "---\nname: full\ndescription: full skill\nlicense: MIT\ncompatibility: Requires curl\n---\nbody"
        result = parse_skill_md(md)
        assert result.license == "MIT"
        assert result.compatibility == "Requires curl"

    def test_strips_body_whitespace(self):
        md = "---\nname: ws\ndescription: whitespace\n---\n\n  body content  \n\n"
        result = parse_skill_md(md)
        assert result.body == "body content"
