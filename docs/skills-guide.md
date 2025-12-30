# Skills Implementation Guide

## Overview

Skills are structured workflows that implement the Accelerator Framework. Each skill is a markdown file in `/.claude/skills/` that contains detailed instructions for Claude to execute specific tasks.

This guide explains how each skill works, when to use it, and how to customize it.

---

## Skill 1: scan-leads

**File:** `/.claude/skills/scan-leads.md`

**Purpose:** Find new candidate companies from public sources (top of funnel)

**Funnel Stage:** Discovery (broad scanning)

### When to Use

- Entering a new sector (e.g., "Start prospecting in logistics")
- Quarterly refresh to find net-new companies
- Specific event scanning (e.g., "Find E50 2024 winners")

### Scope

**Input:** Specific source + sector filter
**Output:** 50-100 candidates in candidates.csv

**Typical Sources:**
- Award lists (E50, SME 500, industry awards)
- Tender databases (GeBIZ, public tenders)
- News searches ("Singapore [sector] expansion 2024")
- Industry association directories

### Workflow Logic

```
1. User specifies: source + sector
   Example: "Scan E50 2024 for logistics companies"

2. Search the specified source
   - If award list: scrape/search for winners
   - If tender: search tender awards in date range
   - If news: web search with sector keywords

3. Extract company names
   - Look for "Pte Ltd", "Private Limited" patterns
   - Filter for Singapore entities

4. Check for duplicates
   - Read existing companies.csv + candidates.csv
   - Skip companies already in system
   - Only add NET NEW candidates

5. For each new candidate:
   - Generate candidate_id (CAND### format)
   - Record source
   - Record initial_trigger (if obvious from source)
   - Set status=pending
   - Set date_added=today

6. Write to candidates.csv

7. Commit changes
   Message: "Added [N] candidates from [source] - [sector]"

8. Report to user:
   - "[N] new candidates found"
   - "[M] already in system (skipped)"
   - "Total candidates now: [X]"
   - "Next step: Verify candidates?"
```

### Example Usage

```
User: "Scan E50 2024 awards for manufacturing companies"

Claude executes scan-leads skill:
- Searches E50 2024 winner list
- Filters for manufacturing sector
- Finds 34 manufacturing companies
- Checks against existing data
- 12 already in system (skip)
- 22 new candidates added to candidates.csv
- Commits: "Added 22 candidates from E50 2024 - Manufacturing"
- Reports: "22 new candidates found, ready for verification"
```

### Customization Points

**Source templates:**
- E50 awards → search KPMG E50 site
- GeBIZ tenders → search government procurement
- News search → "[sector] Singapore [year]" pattern

**Sector keywords:**
- Logistics → "logistics", "supply chain", "freight", "warehousing"
- Manufacturing → "manufacturing", "precision engineering", "industrial"
- Healthcare → "clinic", "medical", "healthcare", "pharma"

**Exclusion patterns (apply during scan):**
- Skip if contains "Pte Ltd (Singapore)" (likely MNC subsidiary pattern)
- Skip if SGX-listed (can check against known list)
- Skip obvious global brands (DHL, FedEx, etc.)

---

## Skill 2: verify-leads

**File:** `/.claude/skills/verify-leads.md`

**Purpose:** Verify existence and apply qualification filters

**Funnel Stage:** Qualification (filtering)

### When to Use

- After scan-leads produces new candidates
- Periodic cleanup of pending candidates

### Scope

**Input:** All candidates with status=pending (or filtered by sector)
**Output:** 30-40% of candidates verified → moved to companies.csv

**Verification Checks:**
1. Website exists (official domain)
2. LinkedIn company page exists
3. Not SGX-listed
4. Not obvious MNC subsidiary
5. Not public DBS banker mention
6. Holdco plausibility check

### Workflow Logic

```
1. Read candidates.csv WHERE status=pending
   - Optionally filter by sector if user specified

2. For each candidate (iterate):

   a) Existence verification:
      - Search "[company name] Singapore"
      - Look for official website
      - Look for LinkedIn company page
      - If NEITHER found → mark as dropped (reason: "No website/LinkedIn found")
      - If FOUND → continue to next checks

   b) Exclusion checks:
      - SGX-listed check: Search "[company name] SGX"
        If listed → drop (reason: "SGX-listed company")

      - MNC subsidiary check: Look for patterns:
        - Parent company mentioned (e.g., "A subsidiary of [MNC]")
        - Global brand name (FedEx, UPS, Siemens, etc.)
        If MNC → drop (reason: "MNC subsidiary")

      - Public DBS mention: Search "[company name] DBS bank"
        If press release/article explicitly mentions DBS as banker
        → drop (reason: "Public DBS banker mention")

      - Holdco plausibility: Look for signals:
        - "Holdings", "Group" in name
        - Listed parent company
        - Wide regional subsidiary network
        If strong signals → flag holdco_flag=yes (don't auto-drop, needs review)

   c) If passed all checks:
      - Create company_id (kebab-case from company name)
      - Extract basic info:
        - Legal name (if found)
        - Website URL
        - LinkedIn URL
        - Sector (from candidate record)
        - Industry (if identifiable from website/LinkedIn)
      - Set priority=medium (default, will be updated after enrichment)
      - Set confidence=MEDIUM (default)
      - Set date_verified=today
      - Set last_enriched=never
      - Set current_stage=verified
      - Add to companies.csv
      - Update candidate status=verified

   d) If failed checks:
      - Update candidate status=dropped
      - Record drop_reason

3. Commit changes
   Message: "Verified [N] candidates: [X] passed, [Y] dropped"

4. Report to user:
   - Summary table of results
   - Breakdown of drop reasons
   - Suggest next step (enrich verified companies)
```

### Example Usage

```
User: "Verify all pending candidates"

Claude executes verify-leads skill:
- Found 47 pending candidates
- Verified 47 companies (checking website, LinkedIn, exclusions)
- Results:
  ✓ 29 verified → moved to companies.csv
  ✗ 18 dropped:
    - 8x No website or LinkedIn found
    - 5x MNC subsidiaries (DHL, FedEx, Siemens SG, ABB SG, Accenture SG)
    - 3x SGX-listed
    - 2x Public DBS mention found
- Commits: "Verified 47 candidates: 29 passed, 18 dropped"
- Reports: "29 new companies ready for enrichment"
```

### Customization Points

**Existence verification strictness:**
- Require BOTH website AND LinkedIn (strict)
- Or accept EITHER website OR LinkedIn (lenient)
- Or accept credible directory listing (Crunchbase, SGPBusiness)

**Holdco red flags:**
- "Holdings" in legal name
- "Group" in legal name
- Mentions of "parent company", "subsidiary of"
- Regional presence in >5 countries
- Employee count >1000 (rare for true SME)

**Public DBS exclusion:**
- Search for "[company] DBS" in news
- Look for phrases: "banking partner", "facility from DBS", "financed by DBS"
- Exclude if found in press release or credible article
- Don't exclude based on speculation or rumors

---

## Skill 3: enrich-company

**File:** `/.claude/skills/enrich-company.md`

**Purpose:** Deep trigger research for verified companies

**Funnel Stage:** Intelligence gathering (focused research)

### When to Use

- After companies are verified (last_enriched=never)
- Periodic refresh for high-priority targets (>14 days stale)
- Before generating prospect pack (ensure triggers are current)

### Scope

**Input:** Specific company OR subset (sector, priority, staleness)
**Output:** 3-5 triggers per company added to triggers.csv

**Time Estimates:**
- 1 company: 1-2 minutes
- 10 companies: 10-15 minutes
- 50 companies: 50-60 minutes

### Workflow Logic

```
1. Determine scope:
   IF user specified single company ("Enrich YCH Group"):
     - scope = [that company]

   ELSE IF user specified sector ("Enrich logistics companies"):
     - Read companies.csv WHERE sector=logistics
     - Check last_enriched dates
     - Apply freshness logic:
       - never enriched → definitely include
       - >30 days + priority=high → include
       - >60 days + priority=medium → include
       - <14 days → skip (too recent)
     - If resulting scope >20 companies:
       - Ask user: "Found [N] companies to enrich (~[X] min).
         Enrich all / high-priority only / top [M]?"

   ELSE IF user specified "stale data":
     - Read companies.csv WHERE last_enriched < [date 30 days ago]
     - Suggest scope

2. Confirm scope with user if large (>10 companies)

3. For each company in scope:

   a) Web research for triggers:
      - Search: "[company name] Singapore news 2024 2025"
      - Search: "[company name] expansion"
      - Search: "[company name] LinkedIn" (for job posts, company updates)
      - Search: "[company name] awards"

   b) Extract trigger signals:
      - Expansion triggers:
        - "new facility", "new outlet", "new office"
        - "expanding to [country/region]"
        - "opened [location]"
        - Joint ventures, partnerships

      - Hiring spikes:
        - LinkedIn job posts (count, roles)
        - "hiring", "team growth", "expanding workforce"

      - Capex triggers:
        - "acquired equipment", "new machinery"
        - "fleet expansion", "new vehicles"
        - "invested in [technology/equipment]"

      - Contract wins:
        - "awarded tender", "won project"
        - "contract with [client]"
        - "partnership with [company]"

      - Inventory/cash cycle:
        - "distributor for [brand]"
        - "wholesaler", "supply chain"

      - Compliance:
        - "ISO certification", "regulatory approval"
        - "accreditation", "MAS license"

      - Operational complexity:
        - "multi-entity", "cross-border"
        - "operations in [N] countries"

   c) For each trigger found:
      - Classify into category (expansion/hiring/capex/contract/inventory/compliance/operational)
      - Extract specific description (not vague)
      - Get evidence link (article URL, press release, LinkedIn post)
      - Determine date_observed (when trigger occurred)
      - Rate strength (high/medium/low based on source quality)
      - Generate trigger_id (T### sequential)
      - Add to triggers.csv

   d) Update company record:
      - Update last_enriched=today
      - Recalculate priority based on trigger count/strength:
        - 3+ high-strength triggers → priority=high
        - 2+ medium/high triggers → priority=medium
        - <2 triggers or low strength → priority=low
      - Update current_stage to "enriched" (if was "verified")

   e) Progress update to user:
      - "Enriched [company]: found [N] triggers"

4. Commit changes
   Message: "Enriched [N] companies with [X] total triggers"

5. Report summary:
   - Total triggers found
   - Average triggers per company
   - Companies promoted to high priority
   - Suggested next steps
```

### Example Usage

```
User: "Enrich YCH Group"

Claude executes enrich-company skill:
- Researching YCH Group...
- Found 4 trigger sources:
  1. Business Times article (Nov 2025): RM500M Malaysia investment
  2. Company press release (Nov 2025): US$200M Vietnam hub groundbreaking
  3. Straits Times (Nov 2025): YCH DistriPark Tuas opening
  4. LinkedIn company post (Oct 2025): Sustainability report published

- Classified triggers:
  T045: expansion - RM500M Malaysia investment - HIGH strength
  T046: capex - US$200M Vietnam hub - HIGH strength
  T047: expansion - YCH DistriPark Tuas opening - HIGH strength
  T048: operational - Multi-country operations expanded - MEDIUM strength

- Added 4 triggers to triggers.csv
- Updated YCH Group:
  - last_enriched: 2025-12-30
  - priority: high (promoted from medium)
  - current_stage: enriched

- Commits: "Enriched YCH Group with 4 triggers"
- Reports: "YCH Group enriched: 4 triggers found, priority set to HIGH"
```

### Customization Points

**Trigger detection sensitivity:**
- Conservative: Only include triggers with strong evidence (press releases, credible news)
- Moderate: Include inferred triggers (job posts indicate hiring, etc.)
- Aggressive: Include weak signals (directory listings, old news)

**Date relevance:**
- Strict: Only triggers in last 12 months
- Moderate: Up to 18 months
- Lenient: Up to 24 months (for companies with sparse news)

**Priority auto-calculation:**
- Trigger-based: Count of high-strength triggers
- Sector-weighted: Manufacturing triggers weighted higher than F&B
- Scale-weighted: Larger companies (by employees) get higher priority

**Freshness thresholds:**
- High priority: Refresh if >14 days
- Medium priority: Refresh if >30 days
- Low priority: Refresh if >60 days

---

## Skill 4: generate-prospect-pack

**File:** `/.claude/skills/generate-prospect-pack.md`

**Purpose:** Create banker-ready outreach materials

**Funnel Stage:** Engagement (singular focus)

### When to Use

- After company is enriched (has triggers)
- Before sending outreach
- Can generate in batches for multiple companies

### Scope

**Input:** Single company (or list of companies for batch)
**Output:** 1 prospect pack document per company

**Pack Contents:**
- Email draft (150-200 words)
- Call script opener + 3 discovery questions
- Meeting prep notes

### Workflow Logic

```
1. Validate inputs:
   - Read companies.csv for specified company
   - Check that company exists
   - Check that company has been enriched (last_enriched != never)
   - If not enriched → suggest running enrich-company first

2. Gather intelligence:
   a) Read company data from companies.csv:
      - common_name, sector, industry

   b) Read triggers from triggers.csv WHERE company_id=specified:
      - Get all triggers
      - Sort by strength (high first) and date (recent first)
      - Select top 2-3 triggers for outreach focus

   c) Map triggers to banking needs:
      Apply trigger → banking need mapping:

      expansion triggers →
        - Facility financing (primary)
        - Regional expansion loans (primary)
        - Working capital (secondary)

      hiring triggers →
        - Working capital (primary)
        - Payroll financing (secondary)

      capex triggers →
        - Equipment financing (primary)
        - Asset-backed lending (primary)
        - Leasing (secondary)

      contract triggers →
        - Project financing (primary)
        - Performance guarantees (primary)
        - Working capital (secondary)

      inventory triggers →
        - Trade finance (primary)
        - Inventory financing (primary)
        - Receivables financing (secondary)

      compliance triggers →
        - Technology loans (primary)
        - Compliance financing (secondary)

      operational triggers →
        - Cash management (primary)
        - Multi-currency accounts (primary)
        - FX hedging (secondary)

   d) Read contact info (if available in companies.csv notes or future contacts.csv)

3. Load template:
   - Read /data/templates/outreach-email-template.md
   - (Future: Select template based on trigger type or sector)

4. Fill template with company-specific data:

   EMAIL STRUCTURE:

   Subject: [Trigger-specific hook] - [Company Name]

   Dear [Recipient Name / "Leadership Team" if unknown],

   [Opening paragraph: Reference specific trigger]
   - Mention 1-2 specific triggers with dates
   - Show you've done research (not generic blast)

   [Value proposition paragraph: Map trigger to banking need]
   - "Given your [trigger], we thought it valuable to discuss:"
   - List 2-3 specific banking products (not all products)
   - Tie each product to a trigger

   [Call to action: Low commitment]
   - 15-20 minute call
   - Or facility walk-through
   - Or quick diagnostic

   Best regards,
   [Banker name]

   EXAMPLE:

   Subject: Supporting YCH Group's Regional Expansion - Facility Financing

   Dear Dr. Yap,

   I've been following YCH Group's impressive regional expansion, particularly
   your RM500M investment in Malaysia and the US$200M Vietnam hub groundbreaking
   announced in November.

   Given the scale of your facility development across APAC, I thought it would
   be valuable to explore how DBS can support your next phase of growth with:

   • Facility financing - Structured solutions for large-scale warehouse
     and distribution center development
   • Multi-currency treasury - Optimize cash management across SGD/MYR/VND operations
   • Regional expansion loans - Flexible financing for your APAC expansion roadmap

   Would you have 20 minutes in the coming week for a brief conversation about
   supporting YCH's continued expansion?

   Best regards,
   [Your name]

5. Generate call script:

   CALL OPENER:
   "Hi [Name], I'm [Banker] from DBS SME Banking. I've been following [Company]'s
   recent [trigger 1] and [trigger 2]. I thought it would be valuable to have a
   brief conversation about how we can support your [growth/expansion/operations].
   Do you have 15 minutes now or would another time work better?"

   DISCOVERY QUESTIONS (tailored to triggers):
   - Expansion trigger: "Tell me about your expansion plans for [region/facility]?"
   - Capex trigger: "What's driving your equipment/fleet investment right now?"
   - Contract trigger: "How are you financing the working capital for [project]?"

   (Generate 3 specific questions based on trigger categories)

6. Generate meeting prep notes:

   KEY TALKING POINTS:
   - Company background (from companies.csv)
   - Trigger summary (top 3 triggers with evidence)
   - Banking needs hypotheses (mapped from triggers)
   - Sector context (Singapore [sector] landscape)

   QUESTIONS TO ASK:
   - [3 discovery questions from call script]
   - Current banking relationship (who, satisfaction level)
   - Decision-making process (who's involved, timeline)

   OBJECTION HANDLING:
   - "We already have a bank" → "I understand. Many of our best relationships
     started as secondary banking partners. Given [specific trigger], I thought
     it was worth exploring if we can add value in [specific area]."
   - "Not the right time" → "No problem. When would be a better time to revisit?
     I'd be happy to stay in touch as your [expansion/project] progresses."

7. Save document:
   - Create /documents/prospect-packs/[company-id]-[date].md
   - Include all sections (email, call script, prep notes)
   - Add metadata header (company, date generated, triggers used)

8. Update company record:
   - Set current_stage=outreach_prepared (if was "enriched")

9. Commit changes:
   Message: "Generated prospect pack for [company]"

10. Report to user:
    - Show the email draft
    - Provide document path
    - Ask: "Update status to 'Outreach Prepared'?"
```

### Example Usage

```
User: "Generate prospect pack for Yang Kee Logistics"

Claude executes generate-prospect-pack skill:
- Reading Yang Kee Logistics data...
- Found 4 triggers (2 expansion, 1 capex, 1 contract)
- Selected top 2 triggers for outreach:
  1. Acquired Axima for A$34M (expansion)
  2. Acquired Fliway for NZ$52M (expansion)
- Mapped to banking needs: M&A financing, Multi-currency treasury
- Generating prospect pack...

[Displays email draft]

Subject: Supporting Yang Kee's Regional Expansion - M&A & Treasury Solutions

Dear Mr. Ken Koh,

I've been following Yang Kee Logistics' impressive acquisition strategy,
particularly your recent acquisitions of Axima (A$34M) and Fliway (NZ$52M)
expanding your footprint across Australia and New Zealand.

Given your active M&A activity and cross-border operations, I thought it
would be valuable to explore how DBS can support your continued growth with:

• M&A financing - Flexible structures for acquisition financing across APAC
• Multi-currency treasury - Optimize cash management across SGD/AUD/NZD operations
• Trade finance - Support your cross-border logistics operations

Would you have 20 minutes in the coming week for a brief conversation about
supporting Yang Kee's regional expansion?

Best regards,
[Your name]

---

✓ Prospect pack saved to: /documents/prospect-packs/yang-kee-logistics-2025-12-30.md
✓ Also includes: Call script + 3 discovery questions, Meeting prep notes

Update Yang Kee Logistics to "Outreach Prepared" stage?
```

### Customization Points

**Email tone:**
- Formal: "Dear [Title] [Last Name]" + professional language
- Conversational: "Hi [First Name]" + casual tone
- Singapore business: Mix of formal + relationship-focused

**Email length:**
- Short (100-150 words): Busy executives, cold outreach
- Medium (150-200 words): Standard, most situations
- Long (200-250 words): Warm introduction, complex triggers

**Banking needs selection:**
- Conservative: Only mention 2 needs directly tied to triggers
- Comprehensive: Mention 3-4 needs including secondary
- Exploratory: Mention 2 needs + "and other growth financing needs"

**Call-to-action:**
- Low commitment: "15 minute call"
- Medium: "Coffee chat / Quick diagnostic"
- High commitment: "Facility walk-through / Detailed needs analysis"

**Template variations (future):**
- By sector: Manufacturing email vs Healthcare email
- By trigger: Expansion template vs M&A template
- By stage: First outreach vs Follow-up

---

## Skill Development Guidelines

### Anatomy of a Skill File

```markdown
# [Skill Name]

## Purpose
[What this skill does in 1-2 sentences]

## When to Use
[Scenarios where this skill is invoked]

## Instructions for Claude

You are helping the user [task description]. Follow these steps exactly:

### Step 1: [First Step Name]
[Detailed instructions]
- Specific data to read
- Specific logic to apply
- Decision points

### Step 2: [Second Step Name]
[Detailed instructions]

...

### Final Step: Reporting
[What to tell the user]
[What to commit to git]

## Business Rules
- [Rule 1]
- [Rule 2]
- [Exclusion criteria, validation rules, etc.]

## Output Format
[Template or structure for outputs]

## Error Handling
IF [error condition] THEN [recovery action]

## Examples
[1-2 example executions with sample data]
```

### Skill Design Principles

**1. Be Explicit, Not Generic**
- ❌ "Research the company"
- ✅ "Search '[company name] Singapore news 2024 2025', extract expansion signals matching these patterns: [list]"

**2. Include Decision Logic**
- ❌ "Update priority"
- ✅ "IF trigger_count >= 3 AND strength=high THEN priority=high; ELSE IF trigger_count >= 2 THEN priority=medium; ELSE priority=low"

**3. Validate Before Acting**
- ❌ "Add to companies.csv"
- ✅ "Check if company_id already exists. If exists, ask user if this is a duplicate or different company."

**4. Scope Awareness**
- ❌ "Enrich companies"
- ✅ "IF scope > 20 companies THEN ask user: 'This will take ~[X] minutes. Proceed with all / high-priority only / top N?'"

**5. User Communication**
- ❌ Silent execution
- ✅ "Progress: Enriched 5/10 companies..." and "Summary: 10 companies enriched, 34 triggers found"

**6. Template-Driven Outputs**
- ❌ "Write a professional email"
- ✅ "Use template from /data/templates/outreach-email-template.md. Fill {{COMPANY}} with common_name, {{TRIGGER}} with top trigger description..."

**7. Git Hygiene**
- Always commit after data changes
- Descriptive commit messages
- Never mention git to user

**8. Error Recovery**
- "If company not found, ask user: 'Company not found. Did you mean [similar name]? Or add as new lead?'"
- "If no triggers found, suggest: 'No recent triggers found. This company may be low priority or information is sparse.'"

---

## Testing Skills

### Test Checklist for Each Skill

**scan-leads:**
- [ ] Finds expected number of candidates from source
- [ ] Filters out duplicates (existing companies)
- [ ] Correctly extracts company names (handles variations)
- [ ] Sets correct initial_trigger when obvious
- [ ] Commits with clear message

**verify-leads:**
- [ ] Successfully verifies website + LinkedIn existence
- [ ] Correctly identifies SGX-listed companies (drop)
- [ ] Correctly identifies MNC subsidiaries (drop)
- [ ] Handles holdco flags appropriately (flag, don't auto-drop)
- [ ] Moves verified companies to companies.csv
- [ ] Updates candidate status correctly

**enrich-company:**
- [ ] Applies correct freshness logic (doesn't re-enrich recent data)
- [ ] Finds 3-5 triggers per company on average
- [ ] Correctly classifies triggers into 7 categories
- [ ] Includes evidence links for high-strength triggers
- [ ] Updates last_enriched date
- [ ] Recalculates priority based on triggers

**generate-prospect-pack:**
- [ ] Reads company + trigger data correctly
- [ ] Maps triggers to appropriate banking needs
- [ ] Generates email with specific trigger references (not generic)
- [ ] Creates call script with relevant discovery questions
- [ ] Saves document to correct path
- [ ] Email tone is professional yet conversational

### Test with Edge Cases

**Empty data:**
- What if company has 0 triggers? (Should still generate pack, but warn user)
- What if candidate has no website or LinkedIn? (Should drop)

**Large scope:**
- What if user asks to "enrich all 500 companies"? (Should warn and suggest alternatives)
- What if scan finds 200 candidates? (Should work but report large count)

**Duplicates:**
- What if same company added twice? (Should detect and skip/warn)
- What if similar names? (Should ask user for clarification)

**Stale data:**
- What if company last_enriched was 6 months ago? (Should flag for refresh)
- What if trigger date_observed is 3 years old? (Should still include but mark as low strength)

---

## Skill Maintenance

### When to Update Skills

**1. User Feedback**
- "Emails feel too formal" → Adjust template tone
- "Too many low-quality triggers" → Increase strength threshold

**2. Data Quality Issues**
- "Too many false positives in verification" → Tighten exclusion rules
- "Missing obvious companies" → Expand source search patterns

**3. Process Evolution**
- Add new trigger categories (e.g., "sustainability triggers")
- Add new banking products (e.g., "ESG financing")

**4. Integration Needs**
- Connect to ACRA API when available
- Connect to email sender (automate outreach)

### Version Control for Skills

Since skills are markdown files in git:
- Each update is a commit
- Can revert if skill change causes issues
- Can A/B test (temporarily use different version)

Example commit messages:
- "Adjusted enrich-company: increased evidence link requirement for high-strength triggers"
- "Updated prospect-pack template: shorter email format (150 words max)"
- "Fixed verify-leads: better handling of holdco detection"

---

## Future Skill Ideas (Post-MVP)

### follow-up-outreach
Generate follow-up emails for companies that didn't respond

### schedule-meeting
Integrate with calendar, propose meeting times

### prepare-proposal
Generate banking proposal document based on needs

### monitor-triggers
Scheduled background job to check for new triggers weekly

### competitive-intel
Research which bank a company currently uses

### relationship-mapping
Identify mutual connections (LinkedIn integration)

### pipeline-forecast
Predict conversion probability based on triggers + sector

### sector-deep-dive
Comprehensive analysis of a sector (trends, opportunities)

---

## Summary

Skills transform the CRM from a data repository into an **execution engine**. Each skill:

- Implements a specific stage of the Accelerator Framework
- Has clear scope boundaries (funnel-aware)
- Uses templates to ensure consistency
- Validates data before acting
- Communicates progress to user
- Commits changes automatically
- Suggests logical next steps

The skills work together as a **workflow orchestration system** that guides the user from discovery → verification → enrichment → engagement, maintaining transparency and control at every step.
