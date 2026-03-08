---
name: code-reviewer
description: Review code changes for bugs, style issues, and improvements. Works with git diffs and pull requests.
license: MIT
compatibility: Requires git CLI access and file reading capability
metadata:
  author: skills-as-mcp
  version: "1.0"
  tags:
    - code-review
    - git
    - quality
---

# Code Reviewer

Perform thorough code reviews on staged changes, commits, or pull request diffs.

## When to Use

Activate this skill when the user asks you to:
- Review code changes, a diff, or a pull request
- Check code for bugs, issues, or improvements
- Provide feedback on recently written or modified code

## Instructions

### 1. Gather the Changes

Determine what to review based on the user's request:

- **Staged changes:** Run `git diff --cached`
- **Unstaged changes:** Run `git diff`
- **Specific commit:** Run `git show <commit-hash>`
- **Branch comparison:** Run `git diff main...HEAD` (or the appropriate base branch)
- **PR number:** Run `gh pr diff <number>`

If the user doesn't specify, default to reviewing all uncommitted changes (`git diff` + `git diff --cached`).

### 2. Understand Context

For each changed file, read enough surrounding code to understand:
- What the function or module does
- What data types are involved
- What the expected behavior should be

Read the full file when the diff alone is ambiguous.

### 3. Review Checklist

Evaluate every change against these categories:

**Bugs and Correctness**
- Off-by-one errors, null/undefined access, unhandled edge cases
- Race conditions or concurrency issues
- Incorrect logic or broken control flow
- Missing error handling or swallowed exceptions

**Security**
- Hardcoded secrets, credentials, or API keys
- SQL injection, XSS, or command injection risks
- Improper input validation

**Performance**
- Unnecessary loops, repeated computation, or N+1 queries
- Missing indexes for database queries
- Large allocations in hot paths

**Maintainability**
- Unclear naming, dead code, or duplicated logic
- Missing or misleading comments
- Functions that are too long or do too many things

**Testing**
- Are new code paths covered by tests?
- Are edge cases tested?
- Do existing tests still pass with these changes?

### 4. Format Your Review

Structure your response as follows:

```
## Summary
One-sentence overview of the changes and your overall assessment.

## Issues
### [Critical/Warning/Suggestion] — Short title
**File:** `path/to/file.py`, line N
**Description:** What the problem is and why it matters.
**Suggestion:** How to fix it (include a code snippet if helpful).

## Positive Notes
- Call out things done well (good error handling, clean abstractions, etc.)
```

### 5. Severity Levels

- **Critical:** Bugs, security issues, or data loss risks. Must fix before merging.
- **Warning:** Performance problems, missing edge cases, or maintainability concerns. Should fix.
- **Suggestion:** Style improvements, minor refactors, or nice-to-haves. Consider fixing.

## Constraints

- Be specific. Always reference the exact file and line number.
- Be constructive. Explain *why* something is a problem, not just *that* it is.
- Do not nitpick formatting if a linter or formatter is configured in the project.
- If the changes look good and you find no issues, say so. Do not invent problems.
