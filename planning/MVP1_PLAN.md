# MVP 1 Implementation Plan

## Objective

Build a minimal viable CRM system that enables a business user to:
1. **Find companies matching business criteria** (scan via web + existing research)
2. **Validate and qualify candidates** (verify existence + apply business rules)
3. **Generate evidence-based outreach** (personalized emails from templates)

This proves the core value proposition: **AI does breadth + consistency, human does judgment + relationships.**

---

## Scope Definition

### IN SCOPE (MVP 1)

**Data Structure:**
- 3 CSV files with headers (candidates, companies, triggers)
- user-parameters.md (business rules and target profile)
- 1 outreach email template
- Complete directory structure

**Skills (3 total):**
1. **scan-leads.md** - Find/validate companies (specific OR broad search)
2. **verify-leads.md** - Qualify candidates (apply exclusions, move to companies)
3. **generate-prospect-pack.md** - Create outreach materials

**Core Workflows:**
- Broad search: "Find 10 logistics companies with expansion triggers"
- Specific search: "Scan YCH Group"
- Verify batch: "Verify all pending candidates"
- Generate outreach: "Generate prospect pack for Supreme Components"

**Technical Foundation:**
- User-triggered git commits (natural language: "commit this", "save changes")
- Claude Code Web only (chat interface)
- Natural language commands
- Business rules persist in user-parameters.md (flexible, user-editable)

### OUT OF SCOPE (Deferred to MVP 2+)

- enrich-company skill (refresh triggers for existing companies)
- Migration of 77 companies to CSV (keep in deep_research_leads.md for now)
- Multiple templates (sector/trigger-specific variants)
- Activities logging, meeting tracking
- Banking needs CSV, contacts CSV
- Pipeline stage progression tracking (outreach sent, meeting held, etc.)
- Multi-user collaboration
- Analytics/reporting dashboards

---

## Architecture Decisions

### Decision 1: Scan-Leads Dual Mode

**Specific Search (Narrow):**
- User provides company name: "Scan YCH Group"
- Skill researches that ONE company
- Validates existence, finds triggers
- Adds to candidates if user approves

**Broad Search (Wide):**
- User provides criteria: "Find 10 logistics companies with expansion triggers"
- Skill searches: deep_research_leads.md FIRST, then web search if needed
- Returns list of matching companies
- Adds to candidates in batch

**Why both modes:**
- Specific = validates tips/referrals (common workflow)
- Broad = discovers new targets at scale (Accelerator framework core)

### Decision 2: Search Strategy (Broad Mode)

**Order of operations:**
1. Read user-parameters.md (apply target profile, exclusions)
2. Search deep_research_leads.md first (existing 77 researched companies)
3. If insufficient matches → supplement with web search
4. Apply exclusions (SGX, MNC, public DBS, size constraints)
5. Return combined results (research doc + web)

**Why this order:**
- Leverage existing high-quality research first (77 companies already vetted)
- Web search fills gaps (net-new companies not in research doc)
- Consistent business rules applied to both sources

### Decision 3: User Parameters File

**Location:** `/data/user-parameters.md`

**Contents:**
- Target profile (geography, size, sectors)
- Exclusions (SGX, MNC, public DBS mention)
- Priority scoring criteria (user-defined, not auto-calculated by skills)
- Banking products focus (including count: default 3 products in outreach)
- Outreach preferences (tone, length, CTA)
- Trigger preferences (for reference, not auto-scoring)

**Why persistent parameters:**
- User doesn't repeat constraints every session
- Skills apply consistent business rules
- **User can edit anytime** - skills adapt automatically
- Easy to customize (plain markdown file)
- Transparent methodology (MD can review parameters)
- Business logic lives in user-editable file, not hardcoded in skills

### Decision 4: Deep Research Leads Usage

**Keep in:** reference/deep_research_leads.md (don't migrate to CSV yet)

**Skills that read it:**
- scan-leads.md (for broad searches)
- generate-prospect-pack.md (for outreach generation)

**Why defer migration:**
- Faster MVP 1 delivery
- Can still use the data
- Validate skill logic before committing to CSV structure
- MVP 2 can migrate once skills proven

### Decision 5: Template Strategy

**Single generic template** (not sector/trigger-specific)

**Template includes:**
- Email draft
- Call script + discovery questions
- Meeting prep notes

**Why single template:**
- Simpler MVP 1
- Tests template-filling logic
- User feedback will inform if variants needed
- Can add specialized templates in MVP 2

### Decision 6: Git Commit Strategy (User-Triggered)

**User controls when commits happen:**
- Skills do work (add/update CSV files) but DON'T auto-commit
- User explicitly triggers commits: "Commit this", "Save changes", "Commit the new candidates"
- Claude detects commit intent from natural language variations
- Claude auto-generates descriptive commit messages
- Gentle reminders if user starts new operation with uncommitted changes

**Workflow:**
```
Skill completes → updates CSV → reports to user
User reviews data (can open CSV to verify)
User says: "Commit this data"
→ Git commit happens with auto-generated message
```

**Benefits:**
- User can batch multiple operations into one commit
- User controls git history granularity
- User can review changes before committing
- User can make manual CSV edits before committing

**User never sees:**
- Commit hashes, branch names, git technical details
- Just confirmation: "✓ Changes committed: Added 5 candidates from logistics search"

---

## Deliverables

### 1. Directory Structure

```
/sales-crm
  /data
    candidates.csv              ← Empty with headers
    companies.csv               ← Empty with headers
    triggers.csv                ← Empty with headers
    user-parameters.md          ← NEW: Business rules and preferences
    /templates
      outreach-email-template.md

  /documents
    /prospect-packs             ← Empty folder (generated outputs saved here)

  /.claude
    /skills
      scan-leads.md             ← Skill 1: Find/validate companies
      verify-leads.md           ← Skill 2: Qualify candidates
      generate-prospect-pack.md ← Skill 3: Create outreach

  /reference
    sales_accelerator_concept.md  (existing)
    deep_research_leads.md        (existing - 77 companies)

  /docs
    architecture.md             (existing)
    data-schema.md              (existing)
    workflow.md                 (existing)
    skills-guide.md             (existing)

  /planning
    MVP1_PLAN.md                ← This document
    MVP1_SUMMARY.md             ← Created after MVP 1 complete

  CLAUDE.md                     (existing)
  README.md                     ← NEW: User quick-start guide
```

### 2. CSV Files (Empty with Headers)

**candidates.csv:**
```csv
candidate_id,company_name,source,initial_trigger,date_added,status,drop_reason
```

**companies.csv:**
```csv
company_id,legal_name,common_name,website,linkedin,uen,sector,industry,priority,confidence,holdco_flag,date_verified,last_enriched,current_stage,assigned_to,notes
```

**triggers.csv:**
```csv
trigger_id,company_id,category,description,evidence_link,date_observed,strength,date_added,added_by
```

### 3. User Parameters File

**user-parameters.md:**
```markdown
# CRM Business Parameters

## Target Profile

**Geography:** Singapore (operating entities only)

**Company Size:**
- Revenue: S$30M - S$100M (holdco aggregated)
- Employee range: 50-500 employees (proxy indicator)

**Target Sectors (Priority Order):**
1. Logistics, Supply Chain & Trade
2. Manufacturing & Industrial
3. Healthcare, Wellness & Life Sciences
4. F&B, Retail & Consumer
5. Technology & Professional Services

**Exclusions (Hard Rules):**
- SGX-listed companies
- Obvious MNC subsidiaries (FedEx, DHL, Siemens, etc.)
- Public disclosure of DBS as primary banker
- Government agencies / Statutory boards
- Holdco revenue obviously >S$100M

## Priority Scoring Criteria

**High Priority:**
- New to bank (no existing DBS relationship)
- Company size close to S$40-100M revenue range

**Low Priority:**
- Media companies

**Note:** Skills do NOT auto-calculate priority. User assigns priority based on these criteria during data entry.

## Trigger Preferences (Reference)

**High-Value Triggers:**
- Expansion (facilities, regional, new outlets)
- Capex (equipment, fleet, machinery)
- Contract wins (tenders, project awards)
- M&A activity (acquisitions, mergers)

**Medium-Value Triggers:**
- Hiring spikes (team expansion)
- Compliance/regulation needs
- Operational complexity (multi-entity, cross-border)

**Low-Value Triggers:**
- General news mentions
- Social media activity

**Note:** This is for user reference. Skills capture triggers but don't assign strength ratings automatically.

## Banking Products Focus

**Primary Products:**
- Trade finance
- Facility financing
- Equipment financing
- Working capital
- Regional expansion loans

**Secondary Products:**
- FX hedging
- Multi-currency accounts
- Cash management
- Project financing

**Products to Mention in Outreach:** 3 (default)

## Outreach Preferences

**Tone:** Professional but relationship-focused (Singapore business culture)

**Email Length:** 150-200 words

**Call-to-Action:** Low commitment (15-20 min intro call)

**Key Message:** DBS understands SME growth challenges

**Recipient Name:** Use actual name if available, generic fallback ("Dear CEO") if not

---

*Last updated: 2025-12-30*
```

### 4. Outreach Template

**outreach-email-template.md:**
```markdown
Subject: {{SUBJECT_HOOK}} - {{COMPANY_NAME}}

Dear {{RECIPIENT_NAME}},

{{OPENING_PARAGRAPH}}

{{BANKING_NEEDS_PARAGRAPH}}

{{CALL_TO_ACTION}}

Best regards,
[Your name]

---

## Call Script

**Opener:**
{{CALL_OPENER}}

**Discovery Questions:**
{{DISCOVERY_Q1}}
{{DISCOVERY_Q2}}
{{DISCOVERY_Q3}}

---

## Meeting Prep Notes

**Company Background:**
{{COMPANY_BACKGROUND}}

**Key Triggers:**
{{KEY_TRIGGERS}}

**Banking Needs Hypotheses:**
{{BANKING_NEEDS}}

**Questions to Ask:**
{{MEETING_QUESTIONS}}
```

### 5. README.md (User Quick-Start)

```markdown
# Sales CRM AI - Quick Start Guide

## What is this?

A file-based CRM system that helps you systematically find, qualify, and engage Singapore SME prospects using AI-powered research and evidence-based outreach.

## How to use

### Finding Companies

**Find companies by criteria:**
- "Find 10 logistics companies with expansion triggers"
- "Find manufacturing companies that won tenders in 2024"

**Validate a specific company:**
- "Scan YCH Group"
- "Check out Acme Logistics - heard they won a tender"

### Qualifying Candidates

**Verify candidates:**
- "Verify all pending candidates"
- "Verify logistics candidates"

### Generating Outreach

**Create prospect pack:**
- "Generate prospect pack for YCH Group"
- "Generate prospect pack for Supreme Components"

## Your Business Parameters

Edit `/data/user-parameters.md` to set:
- Target company size and sectors
- Exclusion rules
- Trigger preferences
- Outreach style

All skills automatically apply these parameters.

## Where is my data?

- `/data/candidates.csv` - Companies pending verification
- `/data/companies.csv` - Verified, qualified companies
- `/data/triggers.csv` - Growth signals per company
- `/documents/prospect-packs/` - Generated outreach materials

## Common Commands

- "Find [N] [sector] companies with [trigger type] triggers"
- "Scan [company name]"
- "Verify all pending candidates"
- "Generate prospect pack for [company name]"
- "Show me [company name]" (not implemented yet - just open CSV)

## Need Help?

- See `/docs/workflow.md` for detailed examples
- See `/docs/skills-guide.md` for how skills work
- See `CLAUDE.md` for system instructions
```

---

## Skill Specifications

### Skill 1: scan-leads.md

**Purpose:** Find/validate companies (specific OR broad search)

**Inputs:**

**Mode A (Specific):**
- Company name: "Scan YCH Group"
- Optional hint: "Scan Acme Logistics - heard they won a tender"

**Mode B (Broad):**
- Criteria: "Find 10 logistics companies with expansion triggers"
- Parameters: sector, trigger type, count

**Process:**

```
STEP 1: Read user-parameters.md
- Extract: target geography, size, sectors, exclusions, trigger preferences

STEP 2: Detect mode (specific vs broad)
- IF user provided company name → Mode A (specific)
- IF user provided criteria → Mode B (broad)

MODE A (Specific Company):

STEP 3A: Research the company
- Search: "[company name] Singapore"
- Find: website, LinkedIn, company info
- Search: "[company name] news 2024 2025"
- Search: "[company name] expansion / tender / hiring / awards"

STEP 4A: Validate existence
- IF no website AND no LinkedIn found → report "Could not verify existence"
- IF found → continue

STEP 5A: Extract triggers
- Scan search results for trigger signals:
  - Expansion: "new facility", "expanding to", "opened", "regional"
  - Capex: "acquired equipment", "new machinery", "fleet"
  - Contract: "awarded tender", "won project", "contract with"
  - Hiring: LinkedIn job posts, "hiring", "team growth"
  - M&A: "acquired", "merged with", "partnership"
  - Compliance: "ISO", "certification", "regulatory approval"
  - Operational: "multi-entity", "cross-border", "[N] countries"
- For each trigger:
  - Classify category (expansion/capex/contract/hiring/etc.)
  - Extract specific description
  - Capture evidence link (article URL)
  - Determine date_observed
  - Rate strength (high/medium/low based on source + recency)

STEP 6A: Apply user parameters
- Check exclusions (SGX-listed? MNC subsidiary? Public DBS mention?)
- IF excluded → report "Found but excluded: [reason]"
- IF passed → continue

STEP 7A: Determine priority
- IF 3+ high-strength triggers → priority=high
- IF 2+ medium/high triggers → priority=medium
- ELSE → priority=low

STEP 8A: Report findings to user
- Company name
- Existence confirmed (website, LinkedIn)
- Triggers found (list with evidence)
- Priority recommendation
- Exclusion status
- Ask: "Add to candidates? (yes/no)"

STEP 9A: If user approves
- Generate candidate_id (CAND### sequential)
- Add row to candidates.csv:
  - candidate_id, company_name, source="user scan", initial_trigger=(top trigger), date_added=today, status=pending
- Git commit: "Added [company] to candidates via scan"
- Confirm: "✓ [Company] added to candidates (CAND###)"

MODE B (Broad Search):

STEP 3B: Parse criteria
- Extract: sector (if specified), trigger type (if specified), count (default 10)
- Example: "Find 10 logistics companies with expansion triggers"
  → sector=logistics, trigger_type=expansion, count=10

STEP 4B: Search deep_research_leads.md first
- Read reference/deep_research_leads.md
- Filter by sector (if specified)
- Filter by trigger type (if specified)
- Apply exclusions from user-parameters.md
- Count matches

STEP 5B: If insufficient matches, supplement with web search
- IF matches from research doc >= count → use those
- IF matches < count → web search for additional
- Web search query: "[sector] Singapore [trigger_type] 2024 2025"
- Example: "logistics Singapore expansion 2024 2025"
- Parse results for company names
- For each found company:
  - Quick existence check (website/LinkedIn)
  - Quick trigger check (does it have the trigger type requested?)
  - Apply exclusions
  - If passes → add to candidate list

STEP 6B: Combine results
- Companies from research doc + companies from web search
- Remove duplicates
- Limit to requested count (or slightly more if many found)

STEP 7B: Report findings to user
- Show list: company name, sector, trigger(s) found, source (research doc vs web)
- Example:
  Found 10 logistics companies with expansion triggers:
  1. YCH Group (research doc) - RM500M Malaysia investment, Vietnam hub
  2. Yang Kee Logistics (research doc) - Acquired Axima, Fliway
  3. Acme Cold Chain (web) - Won NTUC tender for expansion
  ...
- Ask: "Add all 10 to candidates? Or select specific ones?"

STEP 8B: If user approves
- For each company:
  - Generate candidate_id (CAND### sequential)
  - Add row to candidates.csv
- Git commit: "Added [N] candidates from [criteria] search"
- Confirm: "✓ [N] companies added to candidates"

ERROR HANDLING:
- IF company not found → "Could not verify [company]. No credible sources found."
- IF no triggers found → "Company verified but no recent triggers found. Low priority."
- IF all results excluded → "Found [N] companies but all excluded (reasons: [list])"

NEXT STEP SUGGESTION:
- After adding candidates → "Next step: Verify candidates to move to companies.csv?"
```

**Example Outputs:**

**Specific Search:**
```
User: "Scan YCH Group"

Claude:
Researching YCH Group...

✓ Company verified
- Website: https://www.ych.com
- LinkedIn: https://linkedin.com/company/ych-group
- Sector: Logistics - 3PL/4PL

Found 3 triggers:
1. RM500M Malaysia investment (Nov 2025, expansion) - HIGH strength
   Evidence: https://www.businesstimes.com.sg/...
2. US$200M Vietnam hub groundbreaking (Nov 2025, capex) - HIGH strength
   Evidence: https://www.ych.com/news/...
3. YCH DistriPark Tuas opening (Nov 2025, expansion) - HIGH strength
   Evidence: https://www.straitstimes.com/...

Priority: HIGH (3 high-strength triggers)
Exclusions: None (passed all checks)

Add YCH Group to candidates?
```

**Broad Search:**
```
User: "Find 10 logistics companies with expansion triggers"

Claude:
Searching for logistics companies with expansion triggers...

Checked: reference/deep_research_leads.md
- Found 6 matches

Supplementing with web search: "logistics Singapore expansion 2024 2025"
- Found 8 additional candidates
- 4 passed exclusion filters

Total: 10 companies found

Results:
1. YCH Group (research doc) - RM500M Malaysia investment, Vietnam hub
2. Yang Kee Logistics (research doc) - Acquired Axima (A$34M), Fliway (NZ$52M)
3. Sin Chew Woodpaq (research doc) - Planning 300K sqft facility by 2026
4. Commonwealth Kokubu (research doc) - Regional expansion planned
5. Dawn Shipping Group (research doc) - ASEAN expansion
6. IPSCOM (research doc) - Vietnam expansion
7. Acme Cold Chain (web) - Won S$50M NTUC expansion tender
8. Beta Logistics (web) - Opened new Tuas warehouse (2024)
9. Gamma Supply Chain (web) - Expanding to Malaysia
10. Delta Freight (web) - New cold chain facility

Add all 10 to candidates? (yes/all/select)
```

---

### Skill 2: verify-leads.md

**Purpose:** Qualify candidates (apply exclusions, move to companies)

**Inputs:**
- All candidates with status=pending
- Optional filter: sector, source

**Process:**

```
STEP 1: Read user-parameters.md
- Extract exclusion rules (SGX, MNC, public DBS, size)

STEP 2: Read candidates.csv
- Filter: status=pending
- Optional: filter by sector if user specified

STEP 3: For each candidate:

  a) Existence verification
     - Verify website exists (search "[company] Singapore")
     - Verify LinkedIn company page exists
     - IF neither found → drop (reason: "No website/LinkedIn found")

  b) SGX-listed check
     - Search: "[company] SGX listed"
     - IF listed on SGX → drop (reason: "SGX-listed company")

  c) MNC subsidiary check
     - Look for patterns:
       - "[Company] subsidiary of [parent]"
       - Global brand names (FedEx, DHL, UPS, Siemens, etc.)
       - Website mentions international parent
     - IF MNC subsidiary → drop (reason: "MNC subsidiary")

  d) Public DBS mention check
     - Search: "[company] DBS bank"
     - Look for: "banking partner", "facility from DBS", "financed by DBS"
     - IF found in press release/article → drop (reason: "Public DBS banker mention")

  e) Holdco plausibility check
     - Look for: "Holdings", "Group" in legal name
     - Search for: parent company, group structure
     - Check for: listed parent, wide regional operations (>5 countries)
     - IF strong signals → flag holdco_flag=yes (don't auto-drop, needs review)
     - IF obvious >S$100M → drop (reason: "Holdco revenue >S$100M")

  f) Sector validation
     - Check if sector in target sectors from user-parameters.md
     - IF not in target sectors → drop (reason: "Out of target sectors")

  g) If passed all checks:
     - Create company_id (kebab-case from company name)
     - Extract basic info:
       - Legal name (if found)
       - Website URL
       - LinkedIn URL
       - Sector
       - Industry (if identifiable)
     - Set defaults:
       - priority=medium (will update after enrichment)
       - confidence=MEDIUM
       - date_verified=today
       - last_enriched=never
       - current_stage=verified
     - Add to companies.csv
     - Update candidate: status=verified

  h) If failed checks:
     - Update candidate: status=dropped, drop_reason=[reason]

STEP 4: Summary statistics
- Count: verified, dropped
- Group drop reasons

STEP 5: Git commit
- Message: "Verified [N] candidates: [X] passed, [Y] dropped"

STEP 6: Report to user
- Summary table
- Breakdown of drop reasons
- Suggest next step

ERROR HANDLING:
- IF no pending candidates → "No pending candidates to verify"
- IF all dropped → "All [N] candidates excluded: [reasons]"

NEXT STEP SUGGESTION:
- "Next step: Generate prospect packs for verified companies?"
```

**Example Output:**

```
User: "Verify all pending candidates"

Claude:
Verifying 12 pending candidates...

Results:
✓ 7 companies verified → moved to companies.csv
  - YCH Group
  - Yang Kee Logistics
  - Sin Chew Woodpaq
  - Acme Cold Chain
  - Beta Logistics
  - Gamma Supply Chain
  - Delta Freight

✗ 5 companies dropped:
  - FedEx Singapore → MNC subsidiary
  - DHL Supply Chain → MNC subsidiary
  - Alpha Logistics → SGX-listed company
  - Omega Holdings → Public DBS banker mention
  - Zeta Trading → No website/LinkedIn found

Summary:
- 7 verified (58%)
- 5 dropped (42%)

7 companies ready for outreach generation.

Next step: Generate prospect packs for verified companies?
```

---

### Skill 3: generate-prospect-pack.md

**Purpose:** Create outreach materials for a company

**Inputs:**
- Company name

**Process:**

```
STEP 1: Read user-parameters.md
- Extract: outreach preferences (tone, length, CTA), banking products focus

STEP 2: Find company data
- Check companies.csv for company_id or common_name match
- IF not found in companies.csv → check reference/deep_research_leads.md
- IF not found in either → error "Company not found"

STEP 3: Gather intelligence

  a) From companies.csv:
     - Read: common_name, sector, industry, notes
     - Read triggers.csv WHERE company_id=matched
     - Sort triggers by: strength (high first), date (recent first)
     - Select top 2-3 triggers for outreach focus

  b) From deep_research_leads.md (if not in companies.csv):
     - Parse company row from markdown table
     - Extract: sector, triggers from "Growth Signals" column, banking needs

STEP 4: Map triggers to banking needs

  Apply trigger → banking need mapping (from user-parameters.md focus):

  - expansion triggers → Facility financing, Regional expansion loans
  - capex triggers → Equipment financing, Asset-backed lending
  - contract triggers → Project financing, Performance guarantees
  - hiring triggers → Working capital
  - M&A triggers → M&A financing, Multi-currency accounts
  - inventory triggers → Trade finance, Inventory financing
  - compliance triggers → Technology loans
  - operational triggers → Cash management, Multi-currency accounts, FX hedging

  Select top 2-3 banking products based on trigger categories

STEP 5: Load template
- Read: /data/templates/outreach-email-template.md

STEP 6: Fill template

  EMAIL:

  Subject:
  - Hook based on top trigger: "Supporting [Company]'s [trigger type]"
  - Example: "Supporting YCH Group's Regional Expansion - Facility Financing"

  Recipient Name:
  - If contact info available → use name
  - Else → "Leadership Team" or "[Role]"

  Opening Paragraph:
  - Reference 1-2 specific triggers with dates
  - Show research done (not generic)
  - Example: "I've been following YCH Group's impressive regional expansion,
    particularly your RM500M investment in Malaysia and US$200M Vietnam hub
    announced in November."

  Banking Needs Paragraph:
  - "Given [trigger context], I thought it valuable to explore how DBS can support..."
  - List 2-3 specific banking products (from trigger mapping)
  - Tie each product to a trigger
  - Use bullet points for clarity

  Call to Action:
  - Use CTA from user-parameters.md (default: 15-20 min intro call)
  - Low commitment language
  - Example: "Would you have 20 minutes in the coming week for a brief conversation?"

  CALL SCRIPT:

  Opener:
  - "Hi [Name], I'm [Banker] from DBS SME Banking. I've been following [Company]'s
    recent [trigger 1] and [trigger 2]. I thought it would be valuable to have a
    brief conversation about how we can support your [growth/expansion]. Do you
    have 15 minutes now or would another time work better?"

  Discovery Questions (3 tailored to triggers):
  - Expansion trigger: "Tell me about your expansion plans for [region/facility]?"
  - Capex trigger: "What's driving your equipment investment right now?"
  - Contract trigger: "How are you managing working capital for [project]?"
  - M&A trigger: "Are you considering additional acquisitions in the near term?"
  - Hiring trigger: "What's driving your team expansion?"

  MEETING PREP NOTES:

  Company Background:
  - Sector, industry, scale indicators
  - Key people (if available)
  - Notable achievements (awards, etc.)

  Key Triggers:
  - List top 3 triggers with evidence links
  - Dates and context

  Banking Needs Hypotheses:
  - Mapped banking products (from triggers)
  - Rationale for each

  Questions to Ask:
  - 3 discovery questions (from call script)
  - Current banking relationship (who, satisfaction)
  - Decision-making process

STEP 7: Save document
- Filename: /documents/prospect-packs/[company-id]-[YYYY-MM-DD].md
- Include: email, call script, prep notes
- Include metadata: company, date generated, triggers used

STEP 8: Git commit
- Message: "Generated prospect pack for [company]"

STEP 9: Report to user
- Display email draft
- Provide document path
- Ask: "Ready to send? Or need edits?"

ERROR HANDLING:
- IF company not found → "Company not found in companies.csv or deep_research_leads.md"
- IF no triggers found → Generate anyway but warn "No triggers found, email may be generic"
- IF template missing → Error "Template not found at /data/templates/outreach-email-template.md"

NEXT STEP SUGGESTION:
- "After sending: Update status to 'Outreach Sent'?" (future feature)
```

**Example Output:**

```
User: "Generate prospect pack for YCH Group"

Claude:
Reading YCH Group data...
- Found in companies.csv (verified 2025-12-30)
- Triggers: 3 (2 expansion, 1 capex)
- Banking needs: Facility financing, Regional expansion loans, Multi-currency accounts

Generating prospect pack...

---

Subject: Supporting YCH Group's Regional Expansion - Facility Financing

Dear Dr. Robert Yap,

I've been following YCH Group's impressive regional expansion, particularly your
RM500M investment in Malaysia and US$200M Vietnam hub groundbreaking announced in
November 2025.

Given the scale of your facility development across APAC, I thought it would be
valuable to explore how DBS can support your next phase of growth with:

• Facility financing - Structured solutions for large-scale warehouse and
  distribution center development
• Regional expansion loans - Flexible financing for your Malaysia and Vietnam hubs
• Multi-currency treasury - Optimize cash management across SGD/MYR/VND operations

Would you have 20 minutes in the coming week for a brief conversation about
supporting YCH's continued expansion?

Best regards,
[Your name]

---

✓ Prospect pack saved to: /documents/prospect-packs/ych-group-2025-12-30.md

Pack includes:
- Email draft (above)
- Call script with 3 discovery questions
- Meeting prep notes (company background, triggers, banking needs hypotheses)

Ready to send?
```

---

## Implementation Steps

### Phase 1: Foundation Setup (30-45 min)

**Step 1.1: Create directory structure**
```bash
mkdir -p data/templates
mkdir -p documents/prospect-packs
mkdir -p .claude/skills
```

**Step 1.2: Create CSV files with headers**
- candidates.csv
- companies.csv
- triggers.csv

**Step 1.3: Create user-parameters.md**
- Populated with default business rules (from spec above)

**Step 1.4: Create outreach-email-template.md**
- Populated with template structure (from spec above)

**Step 1.5: Create README.md**
- User quick-start guide (from spec above)

**Step 1.6: Initial git commit**
```bash
git add .
git commit -m "MVP 1 foundation: CSV structure, user parameters, template"
```

### Phase 2: Implement Skills (4-6 hours)

**Step 2.1: Implement scan-leads.md (2.5-3 hours)**
- Write skill markdown with full workflow logic
- Include: mode detection, specific search logic, broad search logic
- Include: deep_research_leads.md parsing (straightforward markdown table)
- Include: web search patterns
- Include: trigger detection (7 categories)
- Include: exclusion checks from user-parameters.md
- Include: CSV write logic
- Include: user priority assignment (ask user, suggest based on triggers)
- **NO auto-commit** - just update CSV, report changes
- Default broad search count: 10 companies (tell user upfront)
- Test with: specific company, broad search (sector + trigger), web supplementation

**Step 2.2: Implement verify-leads.md (1-1.5 hours)**
- Write skill markdown with verification workflow
- Include: existence checks, exclusion rules (SGX, MNC, DBS, holdco) from user-parameters.md
- Include: companies.csv write logic
- Include: candidates.csv update logic
- **NO auto-commit** - just update CSVs, report changes
- Remind user if uncommitted changes exist before starting
- Test with: batch of mixed candidates (valid + invalid)

**Step 2.3: Implement generate-prospect-pack.md (1.5-2 hours)**
- Write skill markdown with outreach generation workflow
- Include: data gathering (companies.csv + deep_research_leads.md)
- Include: trigger → banking need mapping (read count from user-parameters.md: default 3)
- Include: template loading and filling
- Include: document generation (markdown)
- **NO auto-commit** - just create document, report path
- Test with: company in companies.csv, company in deep_research_leads.md

**Step 2.4: Integration testing (1 hour)**
- End-to-end workflow: scan → verify → user commits → generate → user commits
- Test user-triggered commits with natural language variations
- Check git history (user-triggered commits, descriptive messages)
- Check CSV data integrity (no corruption, proper formatting)
- Check generated documents (specific not generic, proper formatting)
- Test uncommitted changes reminder

### Phase 3: Testing & Validation (2-3 hours)

**Step 3.1: Functional testing**

Test scan-leads:
- [ ] Specific company found (e.g., "Scan YCH Group")
- [ ] Specific company not found (e.g., "Scan Fake Company Ltd")
- [ ] Broad search with sufficient research doc matches (e.g., "Find 5 logistics companies")
- [ ] Broad search requiring web supplementation (e.g., "Find 20 logistics companies")
- [ ] Broad search tells user upfront: "Searching for 10 companies (default)"
- [ ] Exclusions from user-parameters.md applied correctly (SGX, MNC filtered out)
- [ ] Triggers categorized correctly (expansion, capex, etc.)
- [ ] CSV write successful, candidate_id sequential
- [ ] User asked to assign priority (suggested based on triggers)
- [ ] NO auto-commit (CSV updated, user must commit separately)

Test verify-leads:
- [ ] Verifies valid candidates (moves to companies.csv)
- [ ] Drops SGX-listed companies
- [ ] Drops MNC subsidiaries
- [ ] Drops public DBS mentions
- [ ] Flags holdco concerns (doesn't auto-drop unless obvious)
- [ ] CSV updates correct (status changed, drop_reason populated)
- [ ] Reminder shown if uncommitted changes exist
- [ ] NO auto-commit (CSV updated, user must commit separately)

Test generate-prospect-pack:
- [ ] Generates pack from companies.csv data
- [ ] Generates pack from deep_research_leads.md data
- [ ] Email references specific triggers (not generic)
- [ ] Banking needs count read from user-parameters.md (default 3)
- [ ] Banking needs mapped correctly from triggers
- [ ] Call script includes relevant discovery questions
- [ ] Document saved to correct path
- [ ] NO auto-commit (document created, user must commit separately)

Test user-triggered commits:
- [ ] "Commit this" triggers git commit
- [ ] "Save changes" triggers git commit
- [ ] "Commit the new candidates" triggers git commit
- [ ] Auto-generated commit message is descriptive
- [ ] User only sees confirmation, no git technical details
- [ ] Multiple CSV changes can be batched into one commit

**Step 3.2: User experience testing**

- [ ] All commands work with natural language (no technical syntax required)
- [ ] Skills ask clarifying questions when ambiguous
- [ ] Skills report progress for long operations
- [ ] Skills suggest next steps (including "commit this data?")
- [ ] Error messages are user-friendly (not technical)
- [ ] Git operations invisible except when user explicitly triggers commit

**Step 3.3: Edge case testing**

- [ ] Empty CSVs (no candidates, no companies)
- [ ] Duplicate company names (scan same company twice)
- [ ] Company with no triggers found
- [ ] Broad search finds 0 results
- [ ] Template file missing (graceful error)
- [ ] Malformed CSV (recovery or clear error)

### Phase 4: Documentation & Handoff (1 hour)

**Step 4.1: Create MVP1_SUMMARY.md**
- What was built
- What works (features delivered)
- Known limitations
- Test results summary
- Next steps (MVP 2 scope)

**Step 4.2: User acceptance prep**
- Walk user through README.md
- Demonstrate: scan → verify → generate workflow
- Show: where data lives, how to check git history (for admin)
- Gather feedback

---

## Success Criteria

### Functional Requirements

✅ **Scan-Leads (Specific):**
- User can validate a specific company via natural language
- Skill finds existence, triggers, applies exclusions
- Data added to candidates.csv correctly

✅ **Scan-Leads (Broad):**
- User can search by criteria (sector + trigger + count)
- Skill searches deep_research_leads.md first, supplements with web
- Multiple companies added to candidates.csv in batch

✅ **Verify-Leads:**
- User can verify candidates in batch
- Exclusion rules applied (SGX, MNC, public DBS, holdco)
- Valid candidates moved to companies.csv, invalid marked as dropped

✅ **Generate-Prospect-Pack:**
- User can generate outreach for any company (in CSV or research doc)
- Email references specific triggers (not generic)
- Document saved to /documents/prospect-packs/

✅ **Git Integration (User-Triggered):**
- User triggers commits with natural language ("commit this", "save changes")
- Commit messages auto-generated and descriptive
- Git technical details invisible to user
- User can batch multiple changes into one commit
- Gentle reminders if uncommitted changes exist

### Non-Functional Requirements

✅ **Usability:**
- All interactions via natural language (Claude Code Web chat)
- No technical commands required
- Skills ask clarifying questions when needed
- Skills suggest next steps

✅ **Performance:**
- Specific scan: <2 minutes per company
- Broad scan: <5 minutes for 10 companies
- Verify: <3 minutes for 20 candidates
- Generate: <30 seconds per company

✅ **Reliability:**
- Graceful error handling (no crashes)
- CSV data integrity maintained
- Git commits succeed (or fail gracefully)

✅ **Maintainability:**
- User can edit user-parameters.md directly (flexible business rules)
- Skills automatically apply updated parameters
- Priority scoring criteria user-defined (not hardcoded)
- Banking products count user-defined (not hardcoded)
- No code changes needed for business rule updates

### User Experience Requirements

✅ User understands what each skill does (README.md clear)
✅ User can invoke skills without consulting documentation (natural language)
✅ User receives progress updates for long operations
✅ User is prompted with next steps after each operation
✅ User never sees technical errors (git, CSV parsing, etc.)

---

## Risks & Mitigations

### Risk 1: Web research quality
**Risk:** Broad searches might return low-quality or irrelevant companies
**Mitigation:**
- Prioritize deep_research_leads.md (high-quality source)
- Apply strict exclusions from user-parameters.md
- User reviews results before adding to candidates (approval required)

### Risk 2: Trigger detection accuracy
**Risk:** LLM might hallucinate triggers or misclassify categories
**Mitigation:**
- Require evidence links for high-strength triggers
- User can verify sources in candidates.csv
- Clear strength ratings (high/medium/low)

### Risk 3: Template feels generic
**Risk:** Generated emails might not feel personalized enough
**Mitigation:**
- Template requires specific trigger references
- Includes company-specific details (dates, amounts, etc.)
- User feedback will inform template improvements in MVP 2

### Risk 4: CSV corruption
**Risk:** Skills might write malformed CSV data
**Mitigation:**
- Git provides rollback capability
- Test thoroughly before user acceptance
- Start with empty CSVs (no risk to existing data)

### Risk 5: Deep research leads parsing
**Risk:** Markdown table parsing might fail or be inconsistent
**Mitigation:**
- Test with multiple companies from deep_research_leads.md
- Fallback: if parsing fails, ask user to provide company details manually
- MVP 2 can migrate to CSV for more reliable parsing

### Risk 6: User confusion
**Risk:** User doesn't know which skill to use or how to invoke
**Mitigation:**
- Clear README.md with common commands
- Skills suggest next steps after each operation
- Simple mental model: scan → verify → generate

---

## Open Questions & Decisions

### All Resolved ✅

✅ **Q1:** User parameters scope → Business rules only (for MVP 1)
✅ **Q2:** Parameter editing → Chat in Claude Code Web (consistent interface)
✅ **Q3:** Broad search sources → Web search + deep_research_leads.md
✅ **Q4:** Verify-leads in MVP 1 → Yes, needed for basic funnel
✅ **Q5:** Trigger strength scoring → User enters priority manually (not auto-calculated). Criteria: new to bank + S$40-100M size = high priority. Media = low priority
✅ **Q6:** Broad search default → 10 companies (tell user upfront)
✅ **Q7:** Deep research leads parsing → Straightforward markdown table parsing
✅ **Q8:** Git commits → User-triggered only (natural language: "commit this", "save changes")
✅ **Q9:** Recipient name → Anything for now (not critical, use fallback if needed)
✅ **Q10:** Banking needs count → Read from user-parameters.md (default: 3 products)

---

## Timeline Estimate

**Phase 1 (Foundation Setup):** 30-45 minutes
**Phase 2 (Skills Implementation):** 4-6 hours
**Phase 3 (Testing & Validation):** 2-3 hours
**Phase 4 (Documentation & Handoff):** 1 hour

**Total: 7.5-10.5 hours**

**Suggested Schedule:**
- Session 1 (2 hours): Foundation setup + start scan-leads
- Session 2 (3 hours): Finish scan-leads + verify-leads
- Session 3 (2 hours): Generate-prospect-pack + integration testing
- Session 4 (2 hours): Full testing + documentation + user acceptance

---

## MVP 2 Preview (Not Implementing Yet)

After MVP 1 validation and user feedback, MVP 2 would add:

**Skills:**
- enrich-company.md (refresh triggers for existing companies)
- advance-pipeline.md (move companies through stages)
- log-activity.md (track meetings, calls, outcomes)

**Data:**
- Migrate 77 companies from deep_research_leads.md → CSV
- Add banking_needs.csv (track product opportunities per company)
- Add activities.csv (interaction timeline)
- Add contacts.csv (key people at companies)

**Templates:**
- Sector-specific outreach templates
- Trigger-specific templates (expansion vs M&A vs capex)
- Follow-up email templates

**Features:**
- Pipeline stage tracking (outreach sent → meeting held → proposal sent)
- Stale data detection ("These 12 companies need trigger refresh")
- Daily briefing ("What should I work on today?")
- Sector analysis ("Show me all logistics companies")

---

## Plan Status

✅ **All decisions resolved** - Ready for implementation

**Key Principles Confirmed:**
1. **User-triggered commits** - Better UX, user controls git history
2. **Flexible user-parameters.md** - Business logic in editable file, not hardcoded
3. **User assigns priority** - Not auto-calculated (based on: new to bank + S$40-100M size)
4. **Default 10 companies for broad search** - Communicated upfront
5. **3 banking products in outreach** - Read from user-parameters.md

---

**Next Step:** Proceed to Phase 1 (Foundation Setup).

**Updated:** 2025-12-30
