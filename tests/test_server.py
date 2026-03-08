"""Tests for MCP server tools."""

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError
from skills_as_mcp.server import create_server


@pytest.fixture
def server(tmp_shelf):
    return create_server(str(tmp_shelf))


class TestInstallSkill:
    async def test_install_from_content(self, server, sample_skill_md):
        async with Client(server) as client:
            result = await client.call_tool("install_skill", {
                "content": sample_skill_md,
            })
            text = result.content[0].text
            assert "weather" in text
            assert "installed" in text.lower()

    async def test_install_duplicate_overwrites(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            result = await client.call_tool("install_skill", {"content": sample_skill_md})
            text = result.content[0].text
            assert "weather" in text

    async def test_install_invalid_skill(self, server):
        async with Client(server) as client:
            with pytest.raises(ToolError, match="Invalid SKILL.md"):
                await client.call_tool("install_skill", {
                    "content": "not a valid skill file",
                })


class TestListSkills:
    async def test_list_empty(self, server):
        async with Client(server) as client:
            result = await client.call_tool("list_skills", {})
            text = result.content[0].text
            assert "no skills" in text.lower()

    async def test_list_with_skills(self, server, sample_skill_md, minimal_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            await client.call_tool("install_skill", {"content": minimal_skill_md})
            result = await client.call_tool("list_skills", {})
            text = result.content[0].text
            assert "weather" in text
            assert "minimal" in text


class TestGetSkill:
    async def test_get_existing(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            result = await client.call_tool("get_skill", {"name": "weather"})
            text = result.content[0].text
            assert "# Weather Skill" in text

    async def test_get_nonexistent(self, server):
        async with Client(server) as client:
            with pytest.raises(ToolError, match="not found"):
                await client.call_tool("get_skill", {"name": "nope"})


class TestSearchSkills:
    async def test_search_match(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            result = await client.call_tool("search_skills", {"query": "weather"})
            text = result.content[0].text
            assert "weather" in text

    async def test_search_no_match(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            result = await client.call_tool("search_skills", {"query": "quantum"})
            text = result.content[0].text
            assert "no skills" in text.lower() or "no match" in text.lower()


class TestRemoveSkill:
    async def test_remove_existing(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            result = await client.call_tool("remove_skill", {"name": "weather"})
            text = result.content[0].text
            assert "removed" in text.lower()

            # Verify it's gone
            with pytest.raises(ToolError, match="not found"):
                await client.call_tool("get_skill", {"name": "weather"})

    async def test_remove_nonexistent(self, server):
        async with Client(server) as client:
            with pytest.raises(ToolError, match="not found"):
                await client.call_tool("remove_skill", {"name": "nope"})


class TestEnableDisable:
    async def test_disable_skill(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            result = await client.call_tool("disable_skill", {"name": "weather"})
            assert "disabled" in result.content[0].text.lower()

    async def test_enable_skill(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            await client.call_tool("disable_skill", {"name": "weather"})
            result = await client.call_tool("enable_skill", {"name": "weather"})
            assert "enabled" in result.content[0].text.lower()
