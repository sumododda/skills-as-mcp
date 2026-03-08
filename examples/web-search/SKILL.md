---
name: web-search
description: Search the web for current information and summarize the results clearly.
license: MIT
compatibility: Requires web search tool (e.g., WebSearch, Tavily, Brave Search, or similar)
metadata:
  author: skills-as-mcp
  version: "1.0"
  tags:
    - search
    - research
    - summarization
---

# Web Search

Search the web for up-to-date information and return a clear, well-structured summary.

## When to Use

Activate this skill when the user asks about:
- Current events, news, or recent developments
- Facts you are unsure about or that may have changed since your training cutoff
- Product comparisons, reviews, or recommendations that benefit from live data
- Any question where the user explicitly asks you to "search", "look up", or "find"

## Instructions

1. **Clarify the query.** If the user's request is vague, ask one short follow-up question before searching. Otherwise, proceed immediately.

2. **Construct effective search queries.** Break complex questions into 1-3 focused search queries. Use specific keywords rather than full sentences. Include a year or date range when recency matters.

3. **Search and gather results.** Execute your search queries using the available web search tool. Aim for at least 3 distinct sources to cross-reference.

4. **Synthesize a summary.** Combine the results into a clear answer:
   - Lead with the direct answer to the user's question.
   - Include key facts, numbers, or dates when relevant.
   - Note any conflicting information across sources.
   - Keep the summary concise (2-4 paragraphs for most questions).

5. **Cite your sources.** At the end of your response, list the sources you used:
   ```
   Sources:
   - [Title](URL)
   - [Title](URL)
   ```

## Constraints

- Never present search results as your own knowledge. Always attribute information to sources.
- If search results are inconclusive or contradictory, say so clearly rather than guessing.
- Prefer authoritative sources (official sites, major publications, peer-reviewed content) over forums or blogs when available.
- If the search tool is unavailable or returns no results, tell the user honestly and offer to help with what you do know.
