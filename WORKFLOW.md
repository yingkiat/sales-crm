# WORKFLOW.md

## Purpose
This is the canonical operational workflow for this repository.

The repository is a **file-based CRM for Singapore SME prospecting and banker workflow support**. It is designed so AI coding agents can run repeatable prospecting, qualification, enrichment, and outreach workflows while keeping business users in control of decisions and commits.

## System overview
- The CRM is plain-text and file-based.
- **All durable state lives in CSV and markdown files in this repo**.
- Operational work is executed by following skill procedures (currently stored under `/.claude/skills/`) and supporting docs.
- The business workflow is: find candidates → verify qualification → enrich triggers → generate outreach → update CRM state.

## Startup order
At the start of any task:
1. Read `/WORKFLOW.md`.
2. Read `/data/user-parameters.md`.
3. Read relevant current CSVs before answering or editing.
4. Read the relevant skill or supporting doc for the requested operation.

## Core workflow
1. Scan candidates.
2. Verify candidates.
3. Enrich or refresh company triggers.
4. Generate prospect packs / outreach materials.
5. Update CRM state in files.
6. Commit only when the user explicitly asks.

## Source-of-truth files

### Canonical operational source
- `/WORKFLOW.md` (single canonical operational workflow)

### Additional authoritative inputs (task/data rules)
- `/README.md`
- `/data/user-parameters.md`
- `/.claude/skills/scan-leads.md`
- `/.claude/skills/verify-leads.md`
- `/.claude/skills/generate-prospect-pack.md`
- `/docs/data-schema.md`

If docs conflict, prefer the actual skill files over `docs/skills-guide.md`.

## Instruction precedence
1. Explicit user request
2. `WORKFLOW.md`
3. Skill files in `/.claude/skills/`
4. `AGENTS.md` or `CLAUDE.md` for environment-specific notes
5. Supporting docs in `/docs/`
6. README examples

## Data model and file locations
- `/data/candidates.csv`: unverified candidates
- `/data/companies.csv`: verified companies
- `/data/triggers.csv`: evidence-backed growth triggers by `company_id`
- `/data/user-parameters.md`: targeting, exclusions, and outreach preferences
- `/documents/prospect-packs/`: generated outreach/prospect materials

`company_id` is the primary relational key across company-level records.

## Commit policy
- **Do not auto-commit.**
- Skills and workflows may update files, but commits are user-triggered.
- Commit only when the user explicitly asks (e.g., “commit this”, “save changes”).

## CSV safety rules
- Preserve all existing columns.
- Validate each row shape against the header before saving.
- Use `company_id` as the primary relational key for joins and references.
- Do not leave CSV files in a malformed state.

## Scope and interaction guidelines
- Broad operations should be narrowed when expensive.
- Read the current pipeline state before suggesting next steps.
- Prefer business-friendly summaries over raw CSV dumps when presenting findings.

## Interface neutrality
- Do not assume a Claude-only environment.
- Claude Code and Codex can both operate this repo.
- Claude-specific file names (for example `CLAUDE.md` and `/.claude/skills/`) are historical implementation details, not hard dependencies.
