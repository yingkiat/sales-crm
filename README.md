# Sales CRM AI - Quick Start Guide

**Version:** MVP 1 (Tested & Validated ✅)
**Status:** Production-ready for business use
**Last Updated:** 2025-12-31

---

## What is this?

A file-based CRM system that helps you systematically find, qualify, and engage Singapore SME prospects using AI-powered research and evidence-based outreach.

**Current Pipeline:** 24 verified companies | 57 growth triggers | S$1.49B+ opportunities

**Key Features:**
- Natural language interface (Claude Code)
- Evidence-based lead discovery (89% triggers have evidence links)
- Transparent trigger tracking (7 standardized categories)
- Template-driven outreach generation (banker-ready outputs)
- Git-based audit trail (user-controlled commits)

## System Performance (Real Test Results)

**✅ Tested 2025-12-31:**
- **Processing Speed:** 24 companies in 20 minutes (end-to-end)
- **Data Quality:** 100% HIGH confidence | 89% evidence coverage
- **Output Quality:** Banker-ready prospect packs and executive summaries
- **Test Pass Rate:** 100% (12/12 test cases passed)

**Current Pipeline Snapshot:**
- 24 companies verified (96% qualification rate)
- 57 triggers identified (avg 2.4 per company)
- Top 3 opportunities: S$420M + S$120M + S$80M = **S$620M**
- Sector breakdown: Healthcare (25%), Manufacturing (25%), Logistics (21%), F&B (17%), Tech (13%)

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

## Real Workflow Example (From Testing)

**User Request:** "Process top 25 companies, verify them, and generate a prospect pack for YCH Group"

**System Executed (20 minutes):**

```
1. Scan 25 companies from deep_research_leads.md
   ✓ 25 companies parsed
   ✓ 1 excluded (Paradise Group - revenue S$315M exceeds target)
   ✓ 24 added to candidates.csv

2. Verify 24 pending candidates
   ✓ Existence checks (website/LinkedIn)
   ✓ Exclusion filters (SGX/MNC/DBS/revenue/sector)
   ✓ 24 companies moved to companies.csv
   ✓ 57 triggers extracted and mapped

3. Generate prospect pack for YCH Group
   ✓ Email draft: 180 words, specific trigger references
   ✓ Banking products: Facility financing, Regional expansion, Multi-currency
   ✓ Call script: 3 discovery questions
   ✓ Meeting prep: Company background, triggers, deal size (S$420M)

4. Create executive summary
   ✓ 2,800-word analysis document
   ✓ Sector breakdown, trigger analysis, top 10 opportunities
   ✓ Banking product mapping, risk assessment

Result: Banker-ready pipeline with S$1.49B+ identified opportunities
```

**Outputs Generated:**
- `documents/prospect-packs/ych-group-2025-12-30.md` - Ready for banker review
- `documents/SME_Pipeline_Analysis_2025-12-30.md` - Management-ready summary
- `data/companies.csv` - 24 verified prospects
- `data/triggers.csv` - 57 mapped growth signals

## Sample Output: YCH Group Prospect Pack

**Email Draft (Generated):**
```
Subject: Supporting YCH Group's Regional Expansion - Facility Financing

Dear Dr. Yap,

I've been following YCH Group's impressive regional expansion, particularly
your RM500M investment in Malaysia and US$200M Vietnam hub groundbreaking
announced in November 2025, along with the new YCH DistriPark Tuas opening.

Given the scale of your facility development across APAC, I thought it would
be valuable to explore how DBS can support your next phase of growth with:

• Facility financing - Structured solutions for large-scale warehouse and
  distribution center development across Malaysia and Vietnam
• Regional expansion loans - Flexible financing tailored to your multi-country
  expansion strategy
• Multi-currency treasury management - Optimize cash management across
  SGD/MYR/VND operations

Would you have 20 minutes in the coming week for a brief conversation about
supporting YCH's continued regional expansion?

Best regards,
[Your name]
DBS SME Banking
```

**Quality:** ✅ Specific triggers | ✅ Mapped products | ✅ Professional tone | ✅ Low-commitment CTA

---

## Tips

- **Start broad, narrow down:** Scan large lists → verify → generate outreach
- **Review before committing:** You control when git commits happen
- **Customize parameters:** Edit `user-parameters.md` anytime
- **Batch operations:** Verify multiple candidates at once (tested with 24)
- **Specific commands work better:** "Scan YCH Group" is clearer than "check that company"
- **Check test results:** See `/tests/TEST_REPORT_2025-12-31.md` for detailed validation

## Need Help?

**Documentation:**
- `/tests/TEST_REPORT_2025-12-31.md` - Full test results (12 test cases, all passed)
- `/planning/MVP1_SUMMARY.md` - Complete implementation & testing summary
- `/docs/workflow.md` - Detailed workflow examples
- `/docs/skills-guide.md` - How skills work
- `CLAUDE.md` - System instructions for Claude

**Quick Stats (From Testing):**
- ✅ 100% test pass rate (12/12 cases)
- ✅ 24 companies verified in 20 minutes
- ✅ S$1.49B+ opportunities identified
- ✅ 89% trigger evidence coverage
- ✅ 100% HIGH confidence rating

## Architecture

This CRM uses:
- **CSV files** for structured data (human-readable, version-controlled)
- **Markdown files** for documents (emails, meeting notes)
- **Git** for audit trail (you control commits via "commit this")
- **Claude Code** as the interface (natural language, no coding)

Everything is in plain text files - no proprietary formats, no vendor lock-in.

**Tested & Validated:** All core workflows passed testing (scan → verify → generate → analyze)

---

## What's Been Tested ✅

| Workflow | Status | Evidence |
|----------|--------|----------|
| **Broad company search** | ✅ TESTED | 25 companies from deep_research_leads.md |
| **Exclusion filters** | ✅ TESTED | 1 excluded (Paradise Group), 0 false positives |
| **Batch verification** | ✅ TESTED | 24 companies verified and moved to companies.csv |
| **Trigger extraction** | ✅ TESTED | 57 triggers (avg 2.4 per company) |
| **Prospect pack generation** | ✅ TESTED | YCH Group pack generated (banker-ready) |
| **Executive summary** | ✅ TESTED | 2,800-word comprehensive analysis |
| **CSV data integrity** | ✅ TESTED | All files valid, no corruption |
| **No auto-commits** | ✅ TESTED | User controls when commits happen |

**Overall:** 100% pass rate on all acceptance criteria

---

**Built with the Accelerator Framework:** AI does breadth + consistency, you do judgment + relationships.

**Next Steps:** Business user validation, then production deployment

*Last tested: 2025-12-31 | Status: Ready for business use*
