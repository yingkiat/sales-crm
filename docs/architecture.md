# System Architecture

## Design Philosophy

### File-Based CRM
This system uses **flat files (CSV + Markdown)** instead of a traditional database to enable:
- **Git version control** - Full audit trail of all changes
- **Human-readable data** - Business users can inspect data in Excel
- **Claude Code Web interface** - Natural language access via chat
- **Zero infrastructure** - No servers, no databases, just files
- **Portability** - Easy to export, backup, or migrate

### Human-AI Hybrid Model
The system implements the Accelerator Framework from `sales_accelerator_concept.md`:

**AI Responsibilities:**
- Scan public sources for candidate companies (scale)
- Verify existence and apply qualification filters (consistency)
- Extract growth triggers from news/web (breadth)
- Generate structured outreach materials (consistency)

**Human Responsibilities:**
- Decide which sectors/sources to scan (strategy)
- Judge which leads to pursue (business intuition)
- Execute relationship building (human touch)
- Adapt messaging based on responses (relationship skills)

## Data Architecture

### Three-Tier Data Model

```
┌─────────────────────────────────────────────────────────┐
│ TIER 1: CANDIDATES (Top of Funnel)                     │
│ - Unverified leads from broad scanning                 │
│ - Minimal data (name, source, initial trigger)         │
│ - Status: pending / verified / dropped                 │
└─────────────────────────────────────────────────────────┘
                          ↓
                  verify-leads skill
                          ↓
┌─────────────────────────────────────────────────────────┐
│ TIER 2: COMPANIES (Verified Prospects)                 │
│ - Existence verified (website + LinkedIn)              │
│ - Basic qualification applied (not MNC, holdco check)  │
│ - Moderate data (sector, industry, priority)           │
└─────────────────────────────────────────────────────────┘
                          ↓
                  enrich-company skill
                          ↓
┌─────────────────────────────────────────────────────────┐
│ TIER 3: TRIGGERS (Enriched Intelligence)               │
│ - Evidence-based growth signals                        │
│ - Deep research per company                            │
│ - Links to banking needs                               │
└─────────────────────────────────────────────────────────┘
```

### Relational Model (CSV-based)

```
candidates.csv                    companies.csv
┌──────────────┐                 ┌──────────────┐
│ candidate_id │◄────────────────│ company_id   │
│ company_name │                 │ legal_name   │
│ source       │                 │ website      │
│ status       │                 │ sector       │
└──────────────┘                 │ priority     │
                                 │ last_enriched│
                                 └──────┬───────┘
                                        │
                                        │ 1:many
                                        ↓
                                 triggers.csv
                                 ┌──────────────┐
                                 │ trigger_id   │
                                 │ company_id   │←──┐
                                 │ category     │   │
                                 │ description  │   │
                                 │ evidence_link│   │
                                 └──────────────┘   │
                                                    │
                                                    │
                           (Future: banking_needs.csv,
                            activities.csv, contacts.csv)
```

## Skill Architecture

### Skills as Workflow Orchestrators

Skills are **not just prompts** - they are structured workflows with:
- Clear scope boundaries (funnel-aware)
- Data validation rules
- Template-driven outputs (reduce hallucination)
- Automatic git commits
- Progress reporting

### Funnel-Aligned Skill Design

| Skill | Funnel Stage | Input Scope | Output Scope | Frequency |
|-------|--------------|-------------|--------------|-----------|
| scan-leads | Discovery | Broad (source-specific) | 50-100 candidates | Quarterly / New sector |
| verify-leads | Qualification | All pending candidates | 30-40 companies | After scan |
| enrich-company | Intelligence | Targeted subset (1-20) | Triggers per company | Weekly / As needed |
| generate-prospect-pack | Engagement | Single company | 1 outreach pack | Per outreach |

**Key insight:** Scope DECREASES as you move down funnel. Skills are designed for their funnel position.

### Skill Decision Logic Pattern

All skills follow this pattern:

1. **Read current state** (from CSVs)
2. **Determine scope** (based on user input + data freshness)
3. **Confirm with user** (if scope is large/ambiguous)
4. **Execute operations** (web search, data validation, template filling)
5. **Update data** (CSVs, documents)
6. **Commit changes** (automatic git commit)
7. **Report results** (business-friendly summary)

Example: enrich-company skill logic
```
IF user says "enrich logistics companies" THEN
  - Read companies.csv WHERE sector=logistics
  - Check last_enriched dates
  - Count how many need refresh (>14 days for high-priority, >30 for medium)
  - IF count > 15 THEN ask user: "Found 18 companies to refresh, all or high-priority only?"
  - Execute based on choice
  - Update last_enriched for processed companies
  - Commit with message "Enriched [N] logistics companies"
```

## User Interface (Claude Code Web Only)

### Zero Technical Skills Required

**User never:**
- Edits CSVs directly (Claude does it via skills)
- Uses git commands (automatic commits)
- Writes code or scripts
- Deals with file paths or syntax

**User only:**
- Chats in natural language
- Views formatted outputs (tables, summaries)
- Makes business decisions (which leads to pursue, what to say)

### Session Model

Each Claude Code Web session:
1. Loads CLAUDE.md (system context)
2. Has access to all data files
3. Can invoke skills
4. Commits changes automatically
5. User sees only conversational interface

### State Persistence

**Problem:** LLM context resets between sessions

**Solution:** All state in files
- Current pipeline status → companies.csv (current_stage column)
- What needs attention → computed from last_enriched, priority, stage
- Company history → triggers.csv (dated), documents/ (timestamped)

No reliance on LLM memory - everything reconstructible from files.

## Trigger Detection Framework

### Seven Trigger Categories

From `sales_accelerator_concept.md`:

1. **Expansion triggers**
   - Signals: New facilities, outlets, regional markets, JVs
   - Banking needs: Facility financing, regional expansion loans

2. **Hiring spikes**
   - Signals: LinkedIn job posts, "we're hiring" news, team expansion
   - Banking needs: Working capital (payroll, operations)

3. **Capex/equipment triggers**
   - Signals: New machinery, fleet, cold chain, medical devices
   - Banking needs: Equipment financing, asset-backed lending

4. **Contract/order book triggers**
   - Signals: Tender wins, project awards, long-cycle contracts
   - Banking needs: Project financing, performance guarantees, working capital

5. **Inventory/cash-cycle triggers**
   - Signals: Distributor/wholesaler business model, seasonal inventory
   - Banking needs: Trade finance, inventory financing, receivables financing

6. **Compliance/regulation triggers**
   - Signals: MAS requirements, healthcare certifications, cyber/regtech needs
   - Banking needs: Compliance financing, technology loans

7. **Operational complexity triggers**
   - Signals: Multi-entity structure, cross-border operations, multi-currency
   - Banking needs: Cash management, multi-currency accounts, FX hedging

### Evidence Strength Scoring

**High Strength:**
- Press release from company
- News article from credible source (Business Times, Straits Times)
- Official announcement (LinkedIn company post, website news)
- Award recognition (E50, SME 500, industry awards)

**Medium Strength:**
- Secondary reporting (blog posts, aggregator sites)
- Inferred from job postings
- Industry association mentions

**Low Strength:**
- Unverified directories
- Social media rumors
- Outdated information (>18 months)

### Non-Black-Box Requirement

**Every trigger must have:**
- Category (which of the 7)
- Specific description (not vague)
- Evidence link (URL to verify)
- Date observed
- Strength rating

**User can always answer:** "Why did we target this company?"
→ "See triggers.csv: 3 expansion triggers with Business Times articles as evidence"

## Git Strategy

### Automatic Commits

Skills automatically commit after every data change:

**Commit message patterns:**
- Data additions: "Added [N] candidates from [source]"
- Data updates: "Enriched [company] with [N] new triggers"
- Deletions: "Dropped [N] candidates (reason: [exclusion])"
- Generated outputs: "Generated prospect pack for [company]"

### Audit Trail

Git history provides:
- What changed (git diff shows CSV row changes)
- When changed (commit timestamp)
- Why changed (commit message)
- Who changed (commit author - for multi-user future)

### User Never Sees Git

All git operations are silent:
- No "Committing changes..." messages to user
- No git errors shown (handle gracefully)
- User just sees: "YCH Group enriched ✓"

## Scalability Considerations

### Current Design (MVP)
- 100-200 companies in companies.csv
- Excel can handle this easily
- Skills read full CSV into memory (fast enough)

### Future Scaling (500+ companies)
- May need index.csv for faster queries
- Consider partitioning by sector (manufacturing.csv, logistics.csv)
- Or archive inactive companies (archived/ folder)

### Multi-User Future
- Each user has own Claude Code account
- GitHub as source of truth (shared repo)
- Auto-sync on session start (git pull)
- Auto-push on commit
- Conflicts rare if users work on different companies
- Can add assigned_to column for partitioning work

## Security & Privacy

### Data Sensitivity
- Company data is public (web-scraped)
- No PII, no confidential bank data
- Meeting notes might contain sensitive discussions → user discretion

### Access Control
- Repository permissions (GitHub private repo)
- Claude Code login (Anthropic account)
- No additional auth needed (file-based)

### Compliance
- Audit trail via git history
- Easy to implement retention policies (git history truncation)
- Easy to export for compliance reporting (CSVs are standard format)
- Easy to delete companies (remove rows, commit)

## Templates & Consistency

### Template Strategy

Templates prevent hallucination by constraining LLM output:

**Outreach email template structure:**
```markdown
Subject: [Trigger-based hook] - [Company Name]

Dear [Recipient Name],

[Opening: Reference specific trigger with date]

[Hypothesis: How trigger maps to banking need]

[Offer: Specific banking capability, not generic]

[CTA: Low-commitment next step - 15min call, quick diagnostic, etc.]

Best regards,
[Banker Name]
```

**Template variables filled from:**
- companies.csv (company name, industry)
- triggers.csv (trigger description, date)
- Banking needs mapping (trigger category → banking product)

### Multi-Template Future

Can expand to:
- Sector-specific templates (manufacturing tone vs healthcare)
- Trigger-specific templates (expansion email vs capex email)
- Stage-specific templates (first outreach vs follow-up)

Templates stored in `/data/templates/` as markdown files.

## Integration Points (Future)

While MVP is self-contained, future integrations could include:

**MCP Tools for:**
- ACRA API (if available) - automatic UEN lookup
- Email sending - direct Gmail/Outlook integration
- Calendar - schedule follow-ups automatically
- Web scraping - scheduled trigger monitoring

**External Systems:**
- Bank CRM (export companies.csv → import to Salesforce)
- Email client (copy prospect pack → send via Outlook)
- Reporting tools (import CSVs → Power BI dashboards)

## Performance Characteristics

### Typical Operation Times

**scan-leads:**
- E50 award list scan: 3-5 minutes (finite list)
- Tender search: 5-10 minutes (web search + extraction)
- Output: 50-100 candidates

**verify-leads:**
- 50 candidates: ~10 minutes
- Checks: website exists, LinkedIn exists, basic holdco flags
- Output: ~30-40 verified companies

**enrich-company:**
- 1 company: 1-2 minutes (deep web research)
- 10 companies: 10-15 minutes
- Output: 3-5 triggers per company (average)

**generate-prospect-pack:**
- 1 company: 30 seconds (template filling)
- Output: Email + call script

### Optimization Strategy

- Batch verification (verify 50 candidates in one skill run)
- Incremental enrichment (only refresh stale data)
- Template reuse (generate 10 packs quickly)
- Scope awareness (user controls time/scope tradeoff)

---

## Summary: Why This Architecture?

**For the Business User:**
- Natural chat interface (no technical skills needed)
- Transparent outputs (can verify everything)
- Consistent results (templates + rules, not LLM creativity)

**For the Administrator:**
- Version controlled (full audit trail)
- Debuggable (can inspect CSVs, git history)
- Extensible (add skills, templates, integrations)

**For Management:**
- Defensible methodology (non-black-box triggers)
- Scalable process (intern can replicate)
- Measurable funnel (candidates → verified → enriched → engaged)
