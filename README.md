# Sales CRM AI - Quick Start Guide

## What is this?

A file-based CRM system that helps you systematically find, qualify, and engage Singapore SME prospects using AI-powered research and evidence-based outreach.

**Key Features:**
- Natural language interface (Claude Code Web)
- Evidence-based lead discovery
- Transparent trigger tracking
- Template-driven outreach generation
- Git-based audit trail (user-controlled commits)

## How to Use

### Finding Companies

**Find companies by criteria (broad search):**
```
"Find 10 logistics companies with expansion triggers"
"Find manufacturing companies that won tenders in 2024"
```

**Validate a specific company:**
```
"Scan YCH Group"
"Check out Acme Logistics - heard they won a tender"
```

### Qualifying Candidates

**Verify candidates:**
```
"Verify all pending candidates"
"Verify logistics candidates"
```

### Generating Outreach

**Create prospect pack:**
```
"Generate prospect pack for YCH Group"
"Generate prospect pack for Supreme Components"
```

### Saving Your Work

**Commit changes:**
```
"Commit this"
"Save changes"
"Commit the new candidates"
```

## Your Business Parameters

Edit `/data/user-parameters.md` to customize:
- Target company size and sectors
- Exclusion rules (SGX-listed, MNC subsidiaries, etc.)
- Priority scoring criteria
- Banking products to mention in outreach (default: 3)
- Outreach tone and style

**All skills automatically apply these parameters.**

## Where is My Data?

- `/data/candidates.csv` - Companies pending verification
- `/data/companies.csv` - Verified, qualified companies
- `/data/triggers.csv` - Growth signals per company
- `/data/user-parameters.md` - Your business rules (editable)
- `/documents/prospect-packs/` - Generated outreach materials
- `/reference/deep_research_leads.md` - Existing 77 researched companies

## Common Commands

**Discovery:**
- "Find [N] [sector] companies with [trigger type] triggers"
- "Scan [company name]"

**Qualification:**
- "Verify all pending candidates"
- "Verify [sector] candidates"

**Outreach:**
- "Generate prospect pack for [company name]"

**Data Management:**
- "Commit this" / "Save changes"

## Workflow Example

```
1. Find companies: "Find 10 logistics companies with expansion triggers"
   → Searches deep_research_leads.md + web
   → Returns list of candidates

2. Review and approve: Claude shows you the list
   → You decide which to add

3. Verify candidates: "Verify all pending candidates"
   → Applies exclusion rules
   → Moves valid companies to companies.csv

4. Commit changes: "Commit this data"
   → Git commit with descriptive message

5. Generate outreach: "Generate prospect pack for YCH Group"
   → Creates email, call script, meeting prep notes

6. Commit again: "Commit the prospect pack"
   → Another git commit
```

## Tips

- **Start broad, narrow down:** Scan large lists → verify → generate outreach
- **Review before committing:** You control when git commits happen
- **Customize parameters:** Edit user-parameters.md anytime
- **Batch operations:** Verify multiple candidates at once
- **Specific commands work better:** "Scan YCH Group" is clearer than "check that company"

## Need Help?

- See `/docs/workflow.md` for detailed workflow examples
- See `/docs/skills-guide.md` for how skills work
- See `/planning/MVP1_PLAN.md` for system design
- See `CLAUDE.md` for technical system instructions

## Architecture

This CRM uses:
- **CSV files** for structured data (human-readable, version-controlled)
- **Markdown files** for documents (emails, meeting notes)
- **Git** for audit trail (you control commits)
- **Claude Code Web** as the interface (natural language, no coding)

Everything is in plain text files - no proprietary formats, no vendor lock-in.

---

**Built with the Accelerator Framework:** AI does breadth + consistency, you do judgment + relationships.
