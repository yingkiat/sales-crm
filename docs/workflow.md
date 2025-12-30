# User Workflows

## Overview

This document describes how bankers use the Sales CRM AI system in their daily work. All interactions happen through **Claude Code Web** using natural language.

---

## Workflow 1: Entering a New Sector

**Scenario:** Banker wants to start prospecting in the Logistics sector

### Steps

**1. Scan for candidates**

```
User: "Scan E50 2024 awards for logistics companies"

Claude: Scanning E50 2024 award winners for logistics sector...

Found 23 logistics companies:
- YCH Group (E50 Rank not specified)
- Yang Kee Logistics (E50 Rank not specified)
- Sin Chew Woodpaq (E50 Rank #11)
... [20 more]

Added 23 candidates to candidates.csv ✓

Next step: Verify these candidates to check existence and apply qualification filters?
```

**2. Verify candidates**

```
User: "Yes, verify them"

Claude: Verifying 23 logistics candidates...

[Progress updates as verification happens]

Verification complete:
✓ 18 companies verified (moved to companies.csv)
✗ 5 companies dropped:
  - 2x No website found
  - 2x MNC subsidiaries (FedEx, DHL)
  - 1x SGX-listed (rejected)

18 verified companies ready for enrichment.

Next step: Enrich all 18 companies to find triggers (~20 minutes), or just high-priority subset?
```

**3. Enrich high-priority subset**

```
User: "Just the top 10 by employee count"

Claude: Enriching top 10 logistics companies by scale...

Companies to enrich:
1. YCH Group (2,000+ employees)
2. Yang Kee Logistics (1,250+ employees)
3. Commonwealth Kokubu Logistics (500+ estimated)
... [7 more]

This will take approximately 10-12 minutes. Proceed?

User: "Yes"

Claude: [Enriches 10 companies, researching triggers for each]

Enrichment complete ✓

Summary:
- YCH Group: 3 triggers (2 expansion, 1 capex) - HIGH priority
- Yang Kee Logistics: 4 triggers (2 expansion, 1 capex, 1 contract) - HIGH priority
- Sin Chew Woodpaq: 2 triggers (1 expansion, 1 capex) - HIGH priority
... [7 more]

Total: 31 triggers found across 10 companies
Average: 3.1 triggers per company

Top 5 by trigger count ready for outreach.

Next step: Generate prospect pack for a specific company?
```

**Outcome:**
- 18 verified logistics companies in pipeline
- 10 enriched with triggers
- Ready to start outreach to top prospects

---

## Workflow 2: Daily Prospecting Routine

**Scenario:** Banker starts their day and wants to know what needs attention

### Morning Check-In

```
User: "What should I work on today?"

Claude: Good morning! Here's your pipeline status:

📋 NEEDS ATTENTION:
• 3 companies haven't been enriched yet (verified >7 days ago):
  - Dawn Shipping Group
  - Global Cold Chain Solutions
  - SDR Logistics

📬 FOLLOW-UP REQUIRED:
• 2 companies with outreach sent >7 days, no response:
  - YCH Group (outreach sent 2025-12-15, 15 days ago)
  - Commonwealth Kokubu (outreach sent 2025-12-18, 12 days ago)

🎯 READY FOR OUTREACH:
• 5 enriched companies, no outreach sent yet:
  - Yang Kee Logistics (4 triggers, HIGH priority)
  - Sin Chew Woodpaq (2 triggers, HIGH priority)
  - EES Freight Services (3 triggers, HIGH priority)
  - Dawn Shipping Group (needs enrichment first)
  - Trans Global (S) (needs enrichment first)

📈 PIPELINE SUMMARY:
- Total companies: 18
- Enriched: 10
- Outreach sent: 2
- Meetings held: 0

Recommendation: Generate prospect pack for Yang Kee Logistics (highest trigger count, active M&A signals)?
```

**User chooses priority:**

```
User: "Show me Yang Kee Logistics"

Claude: **Yang Kee Logistics**

**Overview:**
- Sector: Logistics - Integrated 3PL/Chemical Logistics
- Scale: 2.7M sqft facilities globally, 1,250+ employees
- Revenue: >S$400M (may exceed target range but privately held)
- Confidence: HIGH

**Recent Triggers (Last 18 Months):**
1. ✈️ World's first automated container depot (expansion) - HIGH strength
   Evidence: https://www.businesstimes.com.sg/...

2. 🤝 Acquired Axima for A$34M (expansion) - HIGH strength
   Evidence: https://www.straitstimes.com/...

3. 🤝 Acquired Fliway for NZ$52M (expansion) - HIGH strength
   Evidence: https://www.yangkee.com/news/...

4. 🚛 Expanding fleet operations (capex) - MEDIUM strength
   Evidence: LinkedIn job posts for fleet managers

**Banking Needs (Inferred):**
- M&A financing (active acquirer)
- Fleet financing (truck/container fleet)
- Trade finance (cross-border operations)
- Multi-currency accounts (regional operations)

**Current Stage:** Enriched (ready for outreach)

**Suggested Approach:**
Lead with M&A financing capability given recent acquisitions. Emphasize cross-border treasury support for regional expansion.

Generate prospect pack now?
```

```
User: "Yes"

Claude: Prospect pack generated for Yang Kee Logistics ✓

Saved to: /documents/prospect-packs/yang-kee-logistics-2025-12-30.md

[Claude displays the email draft]

Subject: Supporting Yang Kee's Regional Expansion - M&A & Treasury Solutions

Dear Mr. Ken Koh,

I've been following Yang Kee Logistics' impressive growth trajectory, particularly your recent acquisitions of Axima (A$34M) and Fliway (NZ$52M), and the development of the world's first automated container depot.

Given your active regional expansion across Australia and New Zealand, I thought it would be valuable to explore how DBS can support your next phase of growth with:

• **M&A financing** - Flexible structures for acquisition financing across APAC
• **Multi-currency treasury solutions** - Optimize cash management across SGD/AUD/NZD operations
• **Fleet and asset financing** - Support your container depot and logistics infrastructure investments

Would you have 20 minutes in the coming week for a brief conversation about how we can support Yang Kee's continued expansion?

Best regards,
[Your name]

---

Also generated:
- Call script with 3 discovery questions
- Meeting prep notes (key talking points)

Update status to "Outreach Prepared"?
```

```
User: "Yes, and I sent the email just now"

Claude: ✓ Yang Kee Logistics updated:
- Current stage: Outreach Sent
- Outreach date: 2025-12-30
- Outreach type: Email to Ken Koh (CEO)

Suggested follow-up date: 2026-01-06 (if no response in 7 days)

Anything else?
```

**Outcome:**
- Identified highest-priority target
- Generated evidence-based outreach
- Sent email
- Pipeline updated
- Follow-up reminder set

---

## Workflow 3: Post-Meeting Update

**Scenario:** Banker had a meeting and needs to log outcome

```
User: "I met with YCH Group yesterday"

Claude: Great! Let me log that meeting.

**Meeting with YCH Group**

A few questions:
1. Who did you meet with?
2. What banking needs did they express?
3. What's the next step?

User: "Met with Dr. Robert Yap. They need facility financing for the Malaysia investment and Vietnam hub. Also interested in multi-currency cash management. Next step is I send a proposal for facility financing."

Claude: ✓ Meeting logged for YCH Group

**Summary:**
- Meeting date: 2025-12-29
- Attendee: Dr. Robert Yap (Executive Chairman)
- Banking needs discussed:
  • Facility financing (high priority) - for RM500M Malaysia investment
  • Facility financing (high priority) - for US$200M Vietnam hub
  • Multi-currency cash management (medium priority)
- Next action: Send facility financing proposal

**Stage updated:** Outreach Sent → Meeting Held → Needs Confirmed

Created meeting notes at: /documents/meeting-notes/ych-group-2025-12-29.md

Would you like me to draft the facility financing proposal?
```

**Outcome:**
- Meeting logged
- Banking needs captured
- Pipeline stage advanced
- Next action identified
- Document created for reference

---

## Workflow 4: Refreshing Stale Data

**Scenario:** It's been 2 weeks, banker wants to check for new triggers

```
User: "Refresh triggers for all logistics companies"

Claude: Checking trigger freshness for logistics companies...

Found 18 logistics companies:
- 10 enriched (last check: 2025-12-30)
- 8 never enriched

Recommendations based on last_enriched dates:
• 0 companies >30 days stale (none need urgent refresh)
• 3 companies >14 days since last check (medium priority to refresh)
• 10 companies checked recently (<14 days)
• 8 companies never enriched (should prioritize these first)

Options:
(a) Enrich the 8 never-enriched companies (~10 min)
(b) Refresh the 3 medium-stale companies (~3 min)
(c) Refresh all 18 companies (~20 min)
(d) Skip for now

Which would you prefer?
```

```
User: "Option A"

Claude: Enriching 8 never-enriched logistics companies...

[Progress updates]

Enrichment complete ✓

New triggers found:
- Dawn Shipping Group: 2 triggers (1 expansion, 1 capex)
- Global Cold Chain Solutions: 3 triggers (2 expansion, 1 compliance)
- Shinyuu Cold Chain: 1 trigger (1 capex)
- Trans Global (S): 2 triggers (1 contract, 1 capex)
- IPSCOM: 1 trigger (1 expansion)
- Whitebox: 2 triggers (1 expansion, 1 operational)
- SDR Logistics: 1 trigger (1 expansion)
- Marine Port Services: 1 trigger (1 expansion)

Total: 13 new triggers added across 8 companies

Updated priorities:
- Global Cold Chain Solutions promoted to HIGH priority (3 strong triggers)
- Dawn Shipping Group promoted to MEDIUM priority (2 triggers)

All logistics companies now enriched ✓

Next step: Generate prospect packs for newly prioritized companies?
```

**Outcome:**
- 8 companies now have trigger intelligence
- 13 new triggers discovered
- Priorities adjusted based on new data
- Ready for next round of outreach

---

## Workflow 5: Quick Company Lookup

**Scenario:** Banker needs to quickly check company status

```
User: "Status of Supreme Components"

Claude: **Supreme Components International**

**Overview:**
- Sector: Manufacturing & Industrial - Electronics/Semiconductor Distribution
- Current Stage: Enriched
- Priority: High
- Confidence: HIGH

**Key Data:**
- Website: https://www.supreme.com.sg
- 13 global locations, 80+ employees
- Revenue: USD $54M (2021), 201% growth 2019-2022

**Triggers (2 total):**
1. New Japan subsidiary (Jan 2024) - expansion - HIGH strength
2. Expanding to Europe (2024) - expansion - MEDIUM strength

**Banking Needs (Inferred):**
- Trade finance (exports to 100 countries)
- FX hedging (multi-currency operations)
- Cross-border payments
- Working capital

**History:**
- Verified: 2025-12-20
- Last enriched: 2025-12-30
- No outreach sent yet

**Next Action:** Ready for prospect pack generation

Would you like to generate outreach materials for Supreme Components?
```

**Outcome:**
- Quick lookup answered
- All relevant data displayed
- Next action suggested

---

## Workflow 6: Adding a New Lead Manually

**Scenario:** Banker heard about a company from a contact and wants to add it

```
User: "Add new company: Acme Cold Chain, I heard they just won a major tender"

Claude: Adding new lead: Acme Cold Chain

Let me verify this company exists...

[Searches web for "Acme Cold Chain Singapore"]

Found potential match:
- Acme Cold Chain Pte Ltd
- Website: https://www.acme-coldchain.sg
- LinkedIn: https://linkedin.com/company/acme-cold-chain

Is this the correct company?

User: "Yes"

Claude: ✓ Company verified

Creating company record...

A few quick questions:
1. What sector? (Logistics / Manufacturing / F&B / Healthcare / Technology)
2. What was the trigger you mentioned? (tender win details?)

User: "Logistics. They won a S$50M cold storage expansion tender from NTUC."

Claude: ✓ Acme Cold Chain added to companies.csv

**Company Details:**
- company_id: acme-cold-chain
- Sector: Logistics - Cold Chain
- Priority: Medium (pending full enrichment)
- Current Stage: Verified

**Initial Trigger Added:**
- Category: Contract (tender win)
- Description: Won S$50M cold storage expansion tender from NTUC
- Strength: High (pending evidence verification)
- Evidence: [needs link]

Next steps:
- Run full enrichment to find additional triggers?
- Add evidence link for the tender win?
- Generate prospect pack now?

What would you like to do?
```

**Outcome:**
- New company added to pipeline
- Initial trigger captured
- Ready for further enrichment or immediate outreach

---

## Workflow 7: Generating Multiple Prospect Packs

**Scenario:** Banker wants to do batch outreach

```
User: "Generate prospect packs for all high-priority logistics companies without outreach"

Claude: Finding high-priority logistics companies ready for outreach...

Found 5 companies:
1. Yang Kee Logistics (4 triggers, no outreach)
2. Sin Chew Woodpaq (2 triggers, no outreach)
3. EES Freight Services (3 triggers, no outreach)
4. Global Cold Chain Solutions (3 triggers, no outreach)
5. Commonwealth Kokubu Logistics (2 triggers, outreach sent 12 days ago)

Note: Commonwealth Kokubu already has outreach sent. Should I:
(a) Generate packs for the 4 without outreach (~2 min)
(b) Also generate follow-up for Commonwealth Kokubu (5 packs total)
(c) Just show me the list, I'll choose specific ones

User: "Option A"

Claude: Generating 4 prospect packs...

✓ Yang Kee Logistics → /documents/prospect-packs/yang-kee-logistics-2025-12-30.md
✓ Sin Chew Woodpaq → /documents/prospect-packs/sin-chew-woodpaq-2025-12-30.md
✓ EES Freight Services → /documents/prospect-packs/ees-freight-2025-12-30.md
✓ Global Cold Chain Solutions → /documents/prospect-packs/global-cold-chain-2025-12-30.md

All prospect packs generated ✓

Each pack includes:
- Personalized email draft (trigger-specific)
- Call script with 3 discovery questions
- Meeting prep notes

Would you like me to update these companies to "Outreach Prepared" stage?
```

**Outcome:**
- 4 companies ready for outreach
- Consistent, evidence-based messaging
- Batch efficiency (generate multiple in one go)

---

## Workflow 8: Sector Analysis

**Scenario:** Banker wants to understand which sectors are performing best

```
User: "Show me a summary of all sectors"

Claude: **Sector Performance Summary**

| Sector | Total Companies | Enriched | Avg Triggers | High Priority | Outreach Sent |
|--------|----------------|----------|--------------|---------------|---------------|
| Logistics | 18 | 18 (100%) | 2.8 | 7 (39%) | 2 (11%) |
| Manufacturing | 12 | 10 (83%) | 3.1 | 5 (42%) | 0 (0%) |
| Healthcare | 8 | 5 (63%) | 2.4 | 3 (38%) | 1 (13%) |
| F&B | 6 | 6 (100%) | 2.2 | 2 (33%) | 0 (0%) |
| Technology | 4 | 2 (50%) | 1.5 | 1 (25%) | 0 (0%) |

**Insights:**

📊 **Best trigger density:** Manufacturing (3.1 avg triggers per company)
📊 **Most complete coverage:** Logistics & F&B (100% enriched)
📊 **Needs enrichment:** Technology (only 50% enriched)
📊 **Highest conversion potential:** Logistics (7 high-priority targets)

**Recommendations:**
1. Manufacturing sector ready for batch outreach (10 enriched, 0 outreach sent)
2. Technology sector needs enrichment focus (2 companies never enriched)
3. Logistics showing good engagement (2 outreach already sent)

Would you like to dive deeper into any specific sector?
```

**Outcome:**
- Portfolio view across sectors
- Data-driven prioritization
- Strategic insights for planning

---

## Common Commands Reference

### Discovery & Enrichment
- "Scan [source] for [sector] companies"
- "Verify all pending candidates"
- "Verify candidates from [sector]"
- "Enrich [company name]"
- "Enrich all [sector] companies"
- "Enrich companies not checked in [X] weeks"
- "Refresh triggers for [company/sector]"

### Outreach & Engagement
- "Generate prospect pack for [company]"
- "Generate packs for all high-priority [sector] companies"
- "Show me [company name]"
- "Status of [company name]"

### Pipeline Management
- "What should I work on today?"
- "Show me all [sector] companies"
- "Show me companies in [stage] stage"
- "Show me high-priority companies without outreach"
- "Show me companies with stale data"

### Data Updates
- "Add new company: [name]"
- "I met with [company] [yesterday/on date]"
- "I sent outreach to [company]"
- "Move [company] to [stage]"
- "Add note to [company]: [text]"

### Analysis
- "Show me sector summary"
- "Which companies have expansion triggers?"
- "Show me companies needing follow-up"
- "Pipeline summary"

---

## Tips for Effective Use

### 1. Start Broad, Narrow Down
- Scan large sources (E50, tenders) → 50-100 candidates
- Verify to filter → 30-40 companies
- Enrich selectively → 10-20 deep research
- Engage individually → 1 company at a time

### 2. Let Claude Suggest Scope
- If you ask to "enrich logistics companies", Claude will check freshness and suggest optimal scope
- Trust the recommendations (based on data freshness logic)

### 3. Batch Similar Operations
- "Verify all candidates" (not one by one)
- "Generate packs for all high-priority" (not individual)
- "Enrich top 10" (not all 50)

### 4. Use Specific Company Names
- "Show me YCH Group" (not "show me that logistics company")
- Avoid ambiguity - Claude will ask for clarification if needed

### 5. Natural Language Works
- "I met with them yesterday" → Claude infers company from context
- "They need trade finance" → Claude captures banking need
- Conversational, not command-line syntax

### 6. Check Status Before Acting
- "Status of [company]" before generating pack (maybe already sent)
- "What needs attention?" before deciding what to work on
- Let data guide your actions

### 7. Regular Refresh Cadence
- Weekly: Enrich high-priority companies for new triggers
- Monthly: Scan new sources for net-new candidates
- As-needed: Verify new candidates when added

---

## Troubleshooting Common Scenarios

### "I can't find a company"
```
User: "Show me ABC Company"
Claude: "ABC Company not found in companies.csv.
Did you mean: ABCD Company (similar name)?
Or would you like to add ABC Company as a new lead?"
```

### "Enrichment taking too long"
```
User: "Enrich all 50 companies"
Claude: "This will take approximately 50-60 minutes.
Would you prefer to:
(a) Enrich high-priority only (15 companies, ~15 min)
(b) Enrich companies not checked in 30+ days (8 companies, ~8 min)
(c) Proceed with all 50 companies"
```

### "Duplicate company added"
```
Claude: "YCH Group already exists in companies.csv (added 2025-12-20).
Would you like to:
(a) View existing YCH Group record
(b) Update existing record
(c) This is a different company (specify difference)"
```

### "Generated email feels too generic"
```
User: "This email for Supreme Components is too generic"
Claude: "Let me regenerate with more specific trigger focus.
Supreme Components has these triggers:
1. New Japan subsidiary (Jan 2024)
2. Europe expansion (2024)

Should I emphasize:
(a) Japan expansion (trade finance for new subsidiary)
(b) Europe expansion (FX hedging for EUR operations)
(c) Both (comprehensive regional expansion support)"
```

---

## Advanced Workflows (Post-MVP)

### Scheduled Trigger Monitoring
"Monitor [company list] weekly for new triggers"
- Automated enrichment on schedule
- Alert when new high-strength trigger found

### Pipeline Forecasting
"How many companies will be ready for outreach next month?"
- Predictive analytics based on enrichment pace

### Sector Rotation Strategy
"Focus on manufacturing this month, logistics next month"
- Systematic sector coverage planning

### Relationship Handoff
"Assign [company] to [banker name]"
- Multi-user collaboration (when implemented)

These advanced workflows require additional features beyond MVP but demonstrate the system's extensibility.
