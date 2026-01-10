# Generate Prospect Pack Skill

You help the user create banker-ready outreach materials for a specific company.

A "prospect pack" includes:
- Email draft (trigger-specific, 150-200 words)
- Call script with opener + 3 discovery questions
- Meeting prep notes

## IMPORTANT: Always Start by Reading User Parameters

**FIRST STEP - Read user parameters:**
```
Read /data/user-parameters.md
Extract:
- Banking products to mention (default: 3)
- Outreach tone, length, CTA
- Key message
```

---

## Step 1: Find Company Data

**User will specify company name:**
- "Generate prospect pack for YCH Group"
- "Create outreach for Supreme Components"

**Search for company in TWO places:**

### 1a) Check companies.csv

```
Read /data/companies.csv
Look for company_id or common_name match (case-insensitive)
```

**IF found in companies.csv:**
- Read company data:
  - common_name, sector, industry, website, notes
- Read associated triggers from triggers.csv:
  - WHERE company_id = matched_id
  - Get all triggers for this company
- **Continue to Step 2**

### 1b) Check deep_research_leads.md

**IF NOT found in companies.csv:**
```
Read /reference/deep_research_leads.md
Search for company name in markdown tables
Parse company row
```

**Extract from table:**
- Company name (column 1)
- Sub-sector (column 2)
- Growth Signals / Triggers (column with trigger descriptions)
- Banking Needs (column with banking products)
- Key Executives (column with names/roles)

**IF found in deep_research_leads.md:**
- **Continue to Step 2**

### 1c) Company Not Found

**IF NOT found in either location:**
```
"Company not found.

Searched:
- companies.csv: [X] companies, no match
- deep_research_leads.md: 77 companies, no match

Suggestions:
- Check spelling: '[user's input]'
- Try common name (e.g., 'YCH Group' not 'YCH Group Pte Ltd')
- Add company first: 'Scan [company name]'

Which company did you mean?"
```
**STOP**

---

## Step 2: Gather Intelligence

### 2a) Company Background

**From companies.csv OR deep_research_leads.md:**
```
- Company name
- Sector and industry
- Scale indicators (employees, locations, revenue if known)
- Notable achievements (awards, certifications)
```

### 2b) Triggers Analysis

**IF from companies.csv:**
- Read triggers.csv WHERE company_id = matched_id
- Sort by: strength (high first), then date (recent first)
- Select **top 2-3 triggers** for outreach focus

**IF from deep_research_leads.md:**
- Parse triggers from "Growth Signals" column
- Identify 2-3 most significant triggers
- Extract dates if mentioned

**Trigger examples:**
- "RM500M Malaysia investment (Nov 2025)"
- "Acquired Axima for A$34M"
- "New 300,000 sqft facility planned by 2026"

### 2c) Banking Needs Mapping

**Map each trigger category to banking products:**

**Expansion triggers** →
- Primary: Facility financing, Regional expansion loans
- Secondary: Working capital

**Capex triggers** →
- Primary: Equipment financing, Asset-backed lending
- Secondary: Leasing

**Contract/tender triggers** →
- Primary: Project financing, Performance guarantees
- Secondary: Working capital

**M&A triggers** →
- Primary: M&A financing, Acquisition loans
- Secondary: Multi-currency accounts

**Hiring triggers** →
- Primary: Working capital
- Secondary: Payroll financing

**Operational complexity triggers** →
- Primary: Cash management, Multi-currency accounts
- Secondary: FX hedging, Trade finance

**Inventory/trade triggers** →
- Primary: Trade finance, Inventory financing
- Secondary: Receivables financing

**Select top banking needs:**
- Read "Products to Mention" from user-parameters.md (default: 3)
- Choose that many products based on trigger categories
- Prioritize products that match multiple triggers

**Example:**
```
Triggers:
- Expansion: RM500M Malaysia investment
- Capex: US$200M Vietnam hub
- Expansion: YCH DistriPark Tuas

Banking needs selected (3):
1. Facility financing (expansion + capex)
2. Regional expansion loans (Malaysia + Vietnam)
3. Multi-currency treasury (SGD/MYR/VND operations)
```

### 2d) Contact Information

**IF available (from companies.csv notes OR deep_research_leads.md key executives):**
- Use recipient name and title
- Example: "Dr. Robert Yap (Executive Chairman)"

**IF NOT available:**
- Use generic: "Dear CEO" or "Dear Leadership Team"
- (Per user-parameters.md: "anything for now")

---

## Step 3: Load Template

**Read:** /data/templates/outreach-email-template.md

**Template has placeholders:**
```
{{SUBJECT_HOOK}}
{{COMPANY_NAME}}
{{RECIPIENT_NAME}}
{{OPENING_PARAGRAPH}}
{{BANKING_NEEDS_PARAGRAPH}}
{{CALL_TO_ACTION}}
{{CALL_OPENER}}
{{DISCOVERY_Q1}}, {{DISCOVERY_Q2}}, {{DISCOVERY_Q3}}
{{COMPANY_BACKGROUND}}
{{KEY_TRIGGERS}}
{{BANKING_NEEDS}}
{{MEETING_QUESTIONS}}
```

---

## Step 4: Fill Template with Company-Specific Data

### 4a) Email Subject

**Format:**
```
"Supporting [Company]'s [Trigger Theme] - [Primary Banking Need]"
```

**Examples:**
- "Supporting YCH Group's Regional Expansion - Facility Financing"
- "Supporting Supreme Components' International Growth - Trade Finance"
- "Supporting Yang Kee Logistics' M&A Strategy - Acquisition Financing"

**Trigger theme:**
- Expansion → "Regional Expansion"
- Capex → "Facility Development" or "Equipment Investment"
- M&A → "M&A Strategy" or "Acquisition Plans"
- Contract → "Project Growth"

### 4b) Recipient Name

**Use:**
- Actual name if available: "Dear Dr. Robert Yap,"
- OR fallback: "Dear CEO," or "Dear Leadership Team,"

### 4c) Opening Paragraph (Trigger Reference)

**Format:**
```
"I've been following [Company]'s [impressive/notable/recent] [theme], particularly [specific trigger 1] and [specific trigger 2] [announced/reported] in [timeframe]."
```

**Include:**
- Reference to 1-2 specific triggers
- Mention dates or amounts (shows research)
- Professional but personal tone

**Example:**
```
"I've been following YCH Group's impressive regional expansion, particularly your RM500M investment in Malaysia and US$200M Vietnam hub groundbreaking announced in November 2025."
```

**Important:**
- Must be SPECIFIC (not generic)
- Reference real triggers with real details
- Show you've done research (not mass email)

### 4d) Banking Needs Paragraph

**Format:**
```
"Given [trigger context], I thought it would be valuable to explore how [Your Bank] can support your [next phase/continued/ongoing] [growth/expansion/operations] with:

• [Banking Product 1] - [Specific value proposition tied to trigger]
• [Banking Product 2] - [Specific value proposition tied to trigger]
• [Banking Product 3] - [Specific value proposition tied to trigger]
```

**Example:**
```
"Given the scale of your facility development across APAC, I thought it would be valuable to explore how [Your Bank] can support your next phase of growth with:

• Facility financing - Structured solutions for large-scale warehouse and distribution center development
• Regional expansion loans - Flexible financing for your Malaysia and Vietnam hubs
• Multi-currency treasury - Optimize cash management across SGD/MYR/VND operations"
```

**Each product line should:**
- State the product clearly
- Add specific context (not generic)
- Tie back to a trigger (Malaysia expansion → regional loans)

### 4e) Call to Action

**Use from user-parameters.md:**
- Tone: Low commitment
- CTA: 15-20 min intro call (default)

**Format:**
```
"Would you have 20 minutes in the coming week for a brief conversation about [specific topic]?"
```

**Examples:**
- "...for a brief conversation about supporting YCH's continued expansion?"
- "...to discuss how we can support your cross-border growth?"
- "...to explore financing options for your facility development?"

**Keep it:**
- Low pressure
- Specific (not "discuss banking services")
- Time-bound (20 minutes, coming week)

### 4f) Call Script Opener

**Format:**
```
"Hi [Name], I'm [Banker Name] from [Your Bank] SME Banking. I've been following [Company]'s recent [trigger 1] and [trigger 2]. I thought it would be valuable to have a brief conversation about how we can support your [growth/expansion/operations]. Do you have 15 minutes now or would another time work better?"
```

**Adjust tone:**
- Cold call: More tentative ("would another time work better?")
- Warm intro: More direct ("I'd love to hear about your plans")

### 4g) Discovery Questions (3 questions, trigger-specific)

**Based on trigger categories, generate relevant questions:**

**Expansion triggers:**
```
"Tell me about your expansion plans for [region/facility]. What's the timeline?"
"How are you financing the [Malaysia/Vietnam/regional] expansion currently?"
"What challenges are you facing with the [new facility/regional] rollout?"
```

**Capex triggers:**
```
"What's driving your equipment/fleet investment right now?"
"How are you managing the cash flow for [equipment/facility] acquisition?"
"Are you considering leasing vs purchase for the new [equipment]?"
```

**M&A triggers:**
```
"Are you considering additional acquisitions in the near term?"
"How did you finance the [Acme] acquisition?"
"What's your integration strategy for the acquired entities?"
```

**Contract/project triggers:**
```
"How are you managing working capital for the [project name] project?"
"What's the payment cycle for the [NTUC/client] contract?"
"Are you handling this project alone or with partners?"
```

**General discovery questions (always useful):**
```
"Who's your current banking partner? How's that relationship?"
"What's your biggest financial challenge right now?"
"How do you make decisions about bringing on new banking partners?"
```

**Select 3 questions:**
- 2 trigger-specific
- 1 relationship/decision-making

### 4h) Meeting Prep Notes

**Company Background:**
```
- [Sector] - [Industry]
- [Scale indicators: employees, locations, revenue]
- [Notable achievements: awards, certifications, milestones]
- [Years established, if known]
```

**Key Triggers:**
```
1. [Category] - [Description] ([Date])
   Evidence: [Link if available]
2. [Category] - [Description] ([Date])
   Evidence: [Link if available]
3. [Category] - [Description] ([Date])
   Evidence: [Link if available]
```

**Banking Needs Hypotheses:**
```
Primary needs (based on triggers):
- [Product 1]: [Rationale tied to specific trigger]
- [Product 2]: [Rationale tied to specific trigger]
- [Product 3]: [Rationale tied to specific trigger]

Secondary needs (potential):
- [Additional products that might be relevant]
```

**Meeting Questions:**
```
[The 3 discovery questions from call script]

Plus:
- Current banking relationship (who, satisfaction, gaps)
- Decision-making process (who's involved, timeline)
- Immediate vs future needs (what's urgent?)
```

---

## Step 5: Save Document

**Filename:**
```
/documents/prospect-packs/[company-id]-[YYYY-MM-DD].md
```

**Examples:**
- `/documents/prospect-packs/ych-group-2025-12-30.md`
- `/documents/prospect-packs/supreme-components-2025-12-30.md`

**Document structure:**
```markdown
# Prospect Pack: [Company Name]

**Generated:** [Date]
**Sector:** [Sector] - [Industry]
**Triggers Used:** [N] ([categories])

---

## Email Draft

Subject: [filled subject]

Dear [filled recipient],

[filled opening paragraph]

[filled banking needs paragraph]

[filled CTA]

Best regards,
[Your name]

---

## Call Script

**Opener:**
[filled call opener]

**Discovery Questions:**
1. [Q1]
2. [Q2]
3. [Q3]

---

## Meeting Prep Notes

**Company Background:**
[filled background]

**Key Triggers:**
[filled triggers with evidence]

**Banking Needs Hypotheses:**
[filled banking needs]

**Questions to Ask:**
[filled meeting questions]

**Current Banking Relationship:**
- Who: [To be discovered]
- Satisfaction: [To be discovered]
- Decision-making: [To be discovered]

---

*Generated by Sales CRM AI*
```

---

## Step 6: Report to User

**Display email draft in chat:**
```
Prospect pack generated for [Company Name]

---

Subject: [subject line]

Dear [recipient],

[email body]

Best regards,
[Your name]

---

✓ Full prospect pack saved to: /documents/prospect-packs/[filename]

Pack includes:
- Email draft (above)
- Call script with 3 discovery questions
- Meeting prep notes (company background, triggers, banking needs)

Ready to send? Or need edits?
```

**DO NOT commit** - just create document and report

---

## Step 7: Next Step Suggestions

```
"Next steps:
- Send email and log activity: (future feature)
- Generate pack for another company: 'Generate prospect pack for [name]'
- Commit: 'Commit the prospect pack'
- Edit manually: Open the file and customize as needed"
```

---

## Error Handling

**IF company has no triggers:**
```
"Warning: No triggers found for [Company].

I can still generate a prospect pack, but the email will be more generic without specific trigger references.

Options:
1. Proceed anyway (generic outreach)
2. Scan/enrich company first: 'Scan [company]' to find triggers
3. Cancel

What would you like to do?"
```

**IF template file missing:**
```
"Error: Template not found at /data/templates/outreach-email-template.md

Please create the template file or restore from git history.

Template should include placeholders:
{{SUBJECT_HOOK}}, {{COMPANY_NAME}}, {{RECIPIENT_NAME}}, etc.

Cannot generate prospect pack without template."
```

**IF company in companies.csv but no triggers.csv entries:**
```
"[Company] found in companies.csv but no triggers in triggers.csv.

This company was verified but not enriched yet.

Options:
1. Generate generic pack (not recommended)
2. Enrich first: 'Scan [company]' to add triggers
3. Check deep_research_leads.md: May have existing trigger data

What would you like to do?"
```

**IF /documents/prospect-packs/ folder doesn't exist:**
```
Create the folder automatically:
mkdir -p /documents/prospect-packs/

Then save file
```

---

## Important Notes

**DO NOT auto-commit:**
- Create document only
- User will commit with "commit the prospect pack" or "commit this"

**Email tone (from user-parameters.md):**
- Professional but relationship-focused
- Singapore business culture context
- Not salesy or pushy
- Shows genuine research and understanding

**Email length (from user-parameters.md):**
- Target: 150-200 words
- Don't exceed 250 words (too long)
- Don't go below 100 words (too brief, seems generic)

**Key message (from user-parameters.md):**
- "[Your Bank] understands SME growth challenges"
- Position as partner, not just vendor
- Focus on growth support, not product push

**Trigger specificity:**
- ALWAYS reference actual triggers with real details
- Mention amounts (RM500M), dates (Nov 2025), specifics (Malaysia, Vietnam)
- Never use vague language like "recent expansion" without details

**Banking products:**
- Read count from user-parameters.md (default: 3)
- Don't list all products (overwhelming)
- Each product line must have specific context, not just product name

**Discovery questions quality:**
- Must be relevant to company's triggers
- Open-ended (not yes/no)
- Show you've done research
- Lead to needs discussion naturally

**Multiple packs:**
- User can generate packs for same company multiple times
- Filename includes date to avoid overwrite
- Each pack is a snapshot for that date

**Customization:**
- User can manually edit generated pack before sending
- Template itself can be edited by user (in /data/templates/)
- Skills will use updated template automatically

---

## Quality Checklist

Before saving prospect pack, verify:
- [ ] Email subject is specific (not generic)
- [ ] Opening paragraph references actual triggers with details
- [ ] Banking needs are tied to specific triggers
- [ ] CTA is clear and low-commitment
- [ ] Discovery questions are trigger-relevant
- [ ] Meeting prep notes include evidence links
- [ ] Document saved with correct filename format
- [ ] Email length is 150-200 words (approximately)
- [ ] Tone is professional + relationship-focused

---

You are now ready to help the user generate professional, evidence-based outreach materials for their SME banking prospects.
