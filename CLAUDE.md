# Sales CRM AI - Claude Notes

> Canonical operations live in `/WORKFLOW.md`.

This file provides Claude-oriented notes and usage examples layered on top of the shared workflow. Shared rules are intentionally centralized in `WORKFLOW.md` and are not restated here in full.

## How to use this with Claude

- Start every task by following `/WORKFLOW.md` startup order.
- Use skill procedures in `/.claude/skills/` for task execution details.
- Keep outputs banker-friendly (summaries, suggested next actions, concise rationale).

## Claude-oriented examples

- "Scan E50 2024 awards for logistics companies"
- "Verify all pending candidates"
- "Generate prospect pack for YCH Group"
- "Summarize top 10 opportunities by trigger strength"

## Commit and PR behavior

- Commit behavior follows `/WORKFLOW.md`: commits are user-triggered.
- Do not assume automatic commits.
- If running in an environment that supports branch and PR workflows, PR creation may be used when explicitly requested by the user or when following the active environment’s normal review process.

## Conflict handling

If `CLAUDE.md` conflicts with `WORKFLOW.md`, follow `WORKFLOW.md` unless the user explicitly asks for Claude-specific behavior.
