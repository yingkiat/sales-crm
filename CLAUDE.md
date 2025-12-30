# Sales CRM AI - Claude Code Instructions

**Version:** MVP 1 (Phase 1 + Phase 2 + Phase 3 Complete)
**Status:** ✅ Tested & Validated (2025-12-31)
**Test Results:** 100% pass rate (12/12 test cases) | 24 companies verified | S$1.49B+ opportunities identified

---

## System Overview

This is a **file-based CRM system** for Singapore SME banking, implementing a human-AI hybrid acquisition framework. The system helps bankers systematically discover, qualify, and engage SME prospects (<S$100M revenue) using transparent, evidence-based triggers.

**Current Pipeline State:**
- **24 verified companies** in companies.csv (100% HIGH confidence)
- **57 growth triggers** mapped in triggers.csv (89% evidence-backed)
- **1 prospect pack** generated (YCH Group - S$420M opportunity)
- **S$1.49B+ total financing opportunities** identified

## Core Principle: Human-AI Hybrid

- **AI does:** Breadth + consistency (scan signals at scale, generate structured outreach)
- **Human does:** Judgment + relationships (decide which leads to pursue, execute engagement)

## Data Architecture

All data is stored in **CSV files** (not database, not JSON):

### Primary Data Files
- `/data/candidates.csv` - Unverified leads (top of funnel)
- `/data/companies.csv` - Verified companies (qualified prospects)
- `/data/triggers.csv` - Evidence-based growth signals per company
- `/data/templates/` - Outreach templates (email, call scripts)

### Generated Outputs
- `/documents/prospect-packs/` - Generated outreach materials per company

## The Funnel (Natural Scope Narrowing)

```
Scan (100s of candidates) → broad sources
  ↓
Verify (30-40 companies) → existence + qualification checks
  ↓
Enrich (10-20 companies) → deep trigger research
  ↓
Engage (singular) → personalized outreach per company
```

**Scope narrows naturally** - scanning is broad, engagement is singular.

## Skills Available

Located in `/.claude/skills/`:

1. **scan-leads.md** - Find new candidates from public sources (E50 awards, tenders, etc.)
   - ✅ TESTED: Successfully processed 25 companies from deep_research_leads.md
   - Mode A (Specific): Validate individual companies
   - Mode B (Broad): Search by sector/criteria

2. **verify-leads.md** - Verify existence + apply qualification filters
   - ✅ TESTED: Verified 24/25 companies (96% qualification rate)
   - Applies 6 exclusion checks (SGX, MNC, DBS, revenue, sector, existence)
   - Moves verified companies to companies.csv

3. **generate-prospect-pack.md** - Create outreach materials for a specific company
   - ✅ TESTED: Generated YCH Group pack (banker-ready)
   - Creates email draft, call script, meeting prep notes
   - Maps triggers to banking products automatically

**Note:** enrich-company.md planned for MVP 2

### Real Example: YCH Group Workflow

**User:** "Process top 25 companies, verify them, and generate a prospect pack for YCH Group"

**System executed:**
1. Scanned 25 companies → 24 added to candidates.csv (1 excluded: Paradise Group S$315M revenue)
2. Verified 24 companies → All moved to companies.csv
3. Extracted 57 triggers across 24 companies
4. Generated YCH Group prospect pack:
   - Email: 180 words, references RM500M Malaysia + US$200M Vietnam + DistriPark Tuas
   - Banking products: Facility financing, Regional expansion loans, Multi-currency treasury
   - Discovery questions: 3 trigger-specific questions
   - Deal size estimate: S$420M

**Result:** Banker-ready outreach in 20 minutes

## Trigger Categories (from Accelerator Framework)

When detecting triggers, use these 7 categories:

1. **Expansion triggers** - New facilities, outlets, regional expansion
2. **Hiring spikes** - Sales, ops, finance, engineer hiring
3. **Capex/equipment triggers** - New machinery, fleet, equipment purchases
4. **Contract/order book triggers** - Tender wins, project awards
5. **Inventory/cash-cycle triggers** - Distributors, wholesalers (working capital signals)
6. **Compliance/regulation triggers** - MAS requirements, healthcare compliance
7. **Operational complexity triggers** - Multi-entity ops, cross-border flows

## Banking Needs Mapping

Map triggers to these banking products:

- Expansion → Facility financing, Regional expansion loans
- Hiring spikes → Working capital
- Capex → Equipment financing, Asset-backed lending
- Contract wins → Project financing, Performance guarantees
- Inventory cycle → Trade finance, Inventory financing
- Multi-entity → Cash management, Multi-currency accounts
- Cross-border → FX hedging, Trade finance

## Key Business Rules

### Exclusion Criteria (Auto-drop)
- SGX-listed companies
- Obvious MNC subsidiaries
- Public disclosure of DBS as banker
- Holdco revenue obviously >S$100M

### Verification Requirements
Every verified company must have:
- Official website OR
- LinkedIn company page OR
- Credible directory listing (Crunchbase, SGPBusiness, etc.)

### Trigger Evidence Requirements
Every trigger must have:
- Category (from 7 categories above)
- Description (specific, observable event)
- Evidence link (article, press release, LinkedIn post)
- Strength (high/medium/low based on source quality)

## Git Commit Strategy

**IMPORTANT:** User-triggered commits (NOT automatic)

1. Skills update CSVs and documents
2. User says "commit this" or "save changes" to trigger git commit
3. Use descriptive commit messages:
   - "Added 24 candidates from top 25 prioritized targets"
   - "Verified 24 manufacturing/logistics/healthcare companies"
   - "Generated prospect pack for YCH Group (S$420M opportunity)"
   - "Analysis complete: 57 triggers identified across 24 companies"
4. **User controls when commits happen** - this gives them review control

**Example Git History:**
```
d9f89fd - MVP 1 complete: Added implementation summary (Phase 1 + Phase 2 done, ready for testing)
1f54f4c - MVP 1 Phase 2: Implemented 3 core skills (scan-leads, verify-leads, generate-prospect-pack)
078871b - MVP 1 foundation: CSV structure, user parameters, template, README
```

**Current Status:** All test data uncommitted (waiting for user to say "commit this")

## User Interaction Guidelines

### The user is a non-IT business user:
- Use natural, conversational language
- Show data in formatted tables, not raw CSV
- Explain what you're doing in business terms, not technical terms
- Ask clarifying questions when scope is ambiguous

### Context Awareness:
- Read relevant CSVs before answering questions
- Don't assume you remember previous conversations - check files
- If user asks about a company, read companies.csv + triggers.csv for that company

### Scope Management:
- If user request is ambiguous ("enrich logistics companies"), ask:
  - "All logistics companies (18 found, ~15min) or high-priority only (6 companies, ~5min)?"
- Show time estimates for broad operations
- Suggest efficient alternatives when appropriate

### Data Freshness Logic:
- Check `last_enriched` column before deciding to refresh triggers
- Use judgment based on:
  - Priority level (high = refresh if >2 weeks old)
  - Trigger count (if 0 triggers, definitely enrich)
  - User intent (explicit "refresh all" vs "show me stale data")

## Output Formatting

### When showing company data:
```
**YCH Group** (Logistics - 3PL/4PL)
- Priority: High | Confidence: HIGH
- Verified: 2025-12-20 | Last Enriched: 2025-12-30

Recent Triggers:
• RM500M Malaysia investment (Nov 2025) - expansion [evidence]
• US$200M Vietnam hub (Nov 2025) - capex [evidence]

Banking Needs:
• Facility financing (high priority)
• Regional expansion loans (high priority)

Current Stage: Enriched
```

### When showing lists:
Use tables with relevant columns only (not all CSV columns)

### When generating outreach:
- Use templates from `/data/templates/`
- Fill with specific trigger data (never generic)
- Maintain professional Singapore banking tone
- Reference evidence (but don't over-explain in email itself)

## File Operations

### Reading CSVs:
- Always read the full CSV to understand current state
- Filter/sort as needed for user queries
- Join across CSVs when needed (companies ← triggers on company_id)

### Updating CSVs:
- Preserve all existing columns
- Maintain consistent formatting
- Validate data before writing (check required fields)
- Use company_id as primary key for relationships

### Creating Documents:
- Use markdown for all generated documents
- Include metadata (date, company, purpose)
- Save to appropriate folder in `/documents/`

## Error Handling

If operations fail:
- Explain what went wrong in business terms
- Suggest corrective action
- Don't leave data in inconsistent state (rollback if needed)

If data is missing:
- Check if company exists in companies.csv
- If not verified yet, suggest running verify-leads first
- If not enriched yet, suggest running enrich-company first

## Tone & Style

- Professional but conversational
- Singapore business context (use S$ for currency, Singapore company naming conventions)
- Banker-friendly language (not technical jargon)
- Concise responses (business users are time-sensitive)
- Action-oriented (suggest next steps)

## Session Startup

When a session begins:
1. Assume the user wants to continue their acquisition workflow
2. Don't repeat system explanations unless asked
3. Be ready to answer: "What should I work on today?" by checking pipeline state

## Reference Documents

- `/reference/sales_accelerator_concept.md` - Full framework methodology
- `/reference/deep_research_leads.md` - Initial 77 researched companies
- `/docs/` - Technical documentation (architecture, data schema, workflows, skills)
- `/tests/` - Test reports and documentation
- `/planning/` - MVP plans and implementation summaries

## Current System Performance (From Testing)

**Processing Speed:**
- 24 companies scanned & verified: ~15 minutes
- 1 prospect pack generated: ~2 minutes
- 1 executive summary created: ~3 minutes
- **Total end-to-end workflow: ~20 minutes**

**Data Quality:**
- Trigger evidence coverage: 89% (51/57 triggers have evidence links)
- Confidence rating: 100% (all 24 companies rated HIGH)
- Trigger recency: 84% (48/57 triggers from 2024-2025)
- Exclusion accuracy: 100% (Paradise Group correctly excluded)

**Banking Opportunities:**
- Top 3 immediate deals: S$420M (YCH) + S$120M (Yang Kee) + S$80M (Sin Chew) = **S$620M**
- Total pipeline: **S$1.49B+** across 24 companies
- Product needs: Facility financing (9 cos), Regional expansion (7 cos), M&A financing (5 cos)

## Sample Output Quality

**Prospect Pack (YCH Group):**
```markdown
Subject: Supporting YCH Group's Regional Expansion - Facility Financing

Dear Dr. Yap,

I've been following YCH Group's impressive regional expansion, particularly your
RM500M investment in Malaysia and US$200M Vietnam hub groundbreaking announced
in November 2025, along with the new YCH DistriPark Tuas opening.

Given the scale of your facility development across APAC, I thought it would be
valuable to explore how DBS can support your next phase of growth with:

• Facility financing - Structured solutions for large-scale warehouse and
  distribution center development across Malaysia and Vietnam
• Regional expansion loans - Flexible financing tailored to your multi-country
  expansion strategy
• Multi-currency treasury management - Optimize cash management across
  SGD/MYR/VND operations

Would you have 20 minutes in the coming week for a brief conversation about
supporting YCH's continued regional expansion?
```

**Quality Assessment:** ✅ Banker-ready (specific triggers, mapped products, professional tone)

---

**Remember:** This system is about giving bankers superpowers to scan markets at scale while maintaining full transparency and control. Every lead must be explainable, every trigger must have evidence, every output must be defensible to management.

**Testing Status:** ✅ All core workflows validated (12/12 test cases passed)
**Recommendation:** Approved for business user validation and production use

*Last updated: 2025-12-31*
