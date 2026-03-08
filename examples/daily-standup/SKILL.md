---
name: daily-standup
description: Prepare a daily standup summary from recent git activity, open issues, and work-in-progress.
license: MIT
compatibility: Requires git CLI access. Optional GitHub CLI (gh) for issue and PR context.
metadata:
  author: skills-as-mcp
  version: "1.0"
  tags:
    - productivity
    - git
    - standup
    - reporting
---

# Daily Standup

Generate a concise daily standup report based on recent git activity and project state.

## When to Use

Activate this skill when the user asks for:
- A standup summary or standup notes
- A recap of what they worked on yesterday or recently
- Help preparing for a daily standup meeting

## Instructions

### 1. Gather Recent Activity

Run these commands to collect data about recent work:

```bash
# Commits from the last 24 hours by the current user
git log --author="$(git config user.name)" --since="24 hours ago" --format="%h %s" --all

# If no commits in 24 hours, extend to 48 hours
git log --author="$(git config user.name)" --since="48 hours ago" --format="%h %s" --all

# Current branch and status
git branch --show-current
git status --short
```

### 2. Gather Project Context (if GitHub CLI is available)

Try these commands, but do not fail if `gh` is not installed:

```bash
# PRs authored by the user
gh pr list --author="@me" --state=open --limit=5

# PRs where review is requested
gh pr list --search="review-requested:@me" --state=open --limit=5

# Issues assigned to the user
gh issue list --assignee="@me" --state=open --limit=5
```

### 3. Analyze and Categorize

Group the gathered information into three standup categories:

- **Done:** Completed work (merged PRs, finished commits, closed issues)
- **In Progress:** Active work (current branch changes, open PRs, uncommitted work)
- **Blockers:** Anything that might be blocking progress (stale PRs awaiting review, failing CI)

### 4. Format the Standup

Present the standup in this format:

```
## Standup — [Today's Date]

### Done
- Merged PR #42: Add user authentication
- Fixed pagination bug in search results (abc1234)

### In Progress
- Working on feature/notifications branch (3 uncommitted files)
- PR #45 open: Refactor database layer (awaiting review)

### Blockers
- PR #43 has been open for 3 days with no review
- CI failing on main branch
```

### 5. Keep It Brief

- Each bullet point should be one short sentence.
- Limit to 3-5 items per category. Prioritize the most important items.
- If a category is empty, include it with "None" rather than omitting it.
- Use commit short hashes and PR numbers for easy reference.

## Constraints

- Only report on the current user's activity, not the entire team.
- If git history is empty or the repo is brand new, say so and suggest the user describe their progress manually.
- Do not editorialize or add opinions about the work. Report facts.
- Always include today's date in the header.
