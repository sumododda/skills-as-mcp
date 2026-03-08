"""Tests for MCP resources."""

import pytest
from fastmcp import Client
from skills_as_mcp.server import create_server


@pytest.fixture
def server(tmp_shelf):
    return create_server(str(tmp_shelf))


class TestSkillResources:
    async def test_read_skill_resource(self, server, sample_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            result = await client.read_resource("skill://weather")
            text = result[0].text if hasattr(result[0], 'text') else str(result[0])
            assert "Weather Skill" in text

    async def test_read_index_resource(self, server, sample_skill_md, minimal_skill_md):
        async with Client(server) as client:
            await client.call_tool("install_skill", {"content": sample_skill_md})
            await client.call_tool("install_skill", {"content": minimal_skill_md})
            result = await client.read_resource("skill://index")
            text = result[0].text if hasattr(result[0], 'text') else str(result[0])
            assert "weather" in text
            assert "minimal" in text
