# CRM Business Parameters

## Hunting Strategy: 4-Track Approach

**Track 1: New-to-Bank (NTB)**
- Target industries: Logistics, Tech, Precision Engineering, Healthcare, Marine
- Focus: Greenfield acquisition, capture wallet before competitors
- Products: Full suite (lending, trade finance, working capital)

**Track 2: Dormant Accounts**
- Target: Existing customers with inactive/minimal activity
- Focus: Reactivation plays, lower barrier than cold outreach
- Products: Re-engagement based on new triggers

**Track 3: Strategic Accounts (Wallet Growth)**
- Target: Existing portfolio accounts with strong wallet expansion potential
- Focus: Deep wallet share growth (cross-sell, upsell, share-of-wallet)
- Products: Opportunistic based on expansion moments

**Track 4: Cash Management Focus (Product-Led)**
- Target: Companies with operational complexity (multi-entity, cross-border, high transaction volumes)
- Focus: Fee income via cash management solutions
- Products: Cash mgmt, multi-currency accounts, FX hedging (non-credit products)

## Target Profile

**Geography:** Singapore (operating entities only)

**Company Size:**
- Revenue: S$30M - S$100M (holdco aggregated)
- Employee range: 50-500 employees (proxy indicator)
- **Note:** Size guidelines are flexible based on product opportunity (e.g., cash mgmt doesn't require size constraints)

**Target Sectors (Priority Order):**
1. Logistics, Supply Chain & Trade
2. Manufacturing & Industrial
3. Healthcare, Wellness & Life Sciences
4. F&B, Retail & Consumer
5. Technology & Professional Services

## Exclusions (Guidelines - Context-Dependent)

**These are guidelines, not hard rules. Consider the hunting track and product opportunity:**

**MNC Subsidiaries:**
- **Traditional exclusion:** Obvious MNC subsidiaries (FedEx, DHL, Siemens) for credit products
- **Exception:** MNC subsidiaries may qualify for non-credit products (cash management, FX, treasury)
- **Rationale:** Cash mgmt/FX opportunities don't require credit evaluation - product fit matters more than ownership structure
- **Example:** UMW Equipment (Sime Darby subsidiary) qualified for cash management opportunity

**Ceased Operations / Pivoting Entities:**
- **Traditional exclusion:** Companies that have closed operations
- **Exception:** Entities still ACRA-registered and pivoting to new brand/business model
- **Rationale:** Transition periods create cash mgmt needs (property holdings, restructuring, new ventures)
- **Example:** Gong Cha Singapore (ceased bubble tea ops, pivoting) qualified for property/cash mgmt opportunity

**Other Exclusions:**
- Government agencies / Statutory boards (applies to all tracks)
- Holdco revenue obviously >S$100M (flexible for Track 4 - cash mgmt)

**Note on Existing Banking Relationships:**
- Existing customers are NOT excluded - they're explicitly targeted in Track 2 (Dormant) and Track 3 (Strategic)
- Even for Track 1 (NTB), a partial banking relationship doesn't exclude wallet expansion opportunities

## Priority Scoring Criteria

**High Priority:**
- New to bank (no existing banking relationship)
- Company size close to S$40-100M revenue range

**Low Priority:**
- Media companies

**Note:** Skills do NOT auto-calculate priority. User assigns priority based on these criteria during data entry.

## Active Market Opportunities (Macro Events)

**Track time-sensitive market disruptions that create acquisition opportunities**

### Current Active Opportunities

#### 1. HSBC SME Exit (Q1 2026) - HIGH PRIORITY
- **Event:** HSBC exiting Singapore SME banking segment
- **Target segment:** Companies with US$10-50M annual turnover (~S$13.5M-67.5M)
- **Overlap with our focus:** Direct overlap with S$30-67M range (sweet spot for acquisition)
- **Opportunity type:** Pre-qualified prospects forced to switch banks
- **Timeline:** Q1 2026 (act now before competitors)
- **Strategic value:**
  - Customers already banked = creditworthy, proven track record
  - Forced switching moment = low competitive friction
  - HSBC not defending = easier wallet capture
  - First mover advantage = build relationships before crowded pitch
- **Action items for skills:**
  - When scanning/verifying companies: Actively search for HSBC relationships
  - When enriching companies: Flag HSBC clients as HIGH priority
  - When generating outreach: Reference transition support ("We understand banking transitions...")
  - Search patterns: "HSBC facility [company]", "HSBC trade finance [company]", annual reports mentioning HSBC
- **Recording:**
  - Document HSBC relationships in `existing_banker` field (engagement.csv)
  - Tag companies with note: "HSBC exit opportunity"
- **Status:** ACTIVE (as of Jan 2026)

---

### Template for Future Opportunities

**Copy this template when adding new macro events:**

#### [N]. [Event Name] ([Timeline]) - [PRIORITY LEVEL]
- **Event:** [Description of market event/disruption]
- **Target segment:** [Specific company characteristics affected]
- **Overlap with our focus:** [How this intersects with our hunting strategy]
- **Opportunity type:** [What acquisition play this enables]
- **Timeline:** [When to act]
- **Strategic value:**
  - [Key advantage 1]
  - [Key advantage 2]
  - [Key advantage 3]
- **Action items for skills:**
  - [How scanning should adapt]
  - [How verification should adapt]
  - [How enrichment should adapt]
  - [How outreach should adapt]
- **Recording:** [How to document in CSVs]
- **Status:** ACTIVE / MONITORING / RESOLVED / ARCHIVED

---

### Example Future Events to Monitor

**Bank Exits/Mergers:**
- Other international banks exiting Singapore SME
- Local bank mergers creating client uncertainty
- Foreign banks pivoting away from certain sectors

**Regulatory Changes:**
- MAS compliance requirements (e.g., AML, reporting)
- Industry-specific regulations (healthcare licensing, logistics permits)
- Tax incentive changes affecting certain sectors

**Economic Disruptions:**
- Interest rate shifts creating refinancing opportunities
- Sector booms (e.g., healthcare post-pandemic, green tech subsidies)
- Supply chain disruptions requiring working capital support

**Competitive Intelligence:**
- Competitor banks cutting back on certain sectors
- New bank entrants disrupting pricing
- Industry consolidation creating M&A needs

**Usage Notes:**
- Review and update this section monthly
- Archive resolved opportunities (don't delete - useful for pattern learning)
- Skills should check this section during research to prioritize accordingly
- Expired opportunities should be moved to ARCHIVED status with resolution date

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

## Current Banker Identification

**IMPORTANT: Extract company's existing banking relationships from news**

When researching companies, actively search for mentions of their current banker:

**Search patterns:**
- "[company name] facility [bank name]"
- "[company name] financing [bank name]"
- "[company name] loan [bank name]"
- "[company name] banking partner"
- "[company name] trade finance"

**Look for indicators in news articles:**
- "Secured S$XXM facility from [Bank Name]"
- "Partnership with [Bank Name] for trade finance"
- "Refinanced with [Bank Name]"
- "Syndicated loan led by [Bank Name]"
- "[Bank Name] provided working capital"

**Common Singapore banks to watch for:**
- OCBC, UOB, Standard Chartered, HSBC, Maybank, CIMB, ANZ, Citibank

**Record in companies.csv:**
- If banker mentioned in news → record in appropriate field
- If no banker mentioned → leave blank (not "unknown")
- If multiple banks mentioned → record primary/main banker only

**Strategic value:**
- Knowing current banker helps determine Track assignment
- No banking relationship mentioned = likely Track 1 (NTB) candidate
- Competitor bank mentioned = opportunity for wallet capture
- Existing relationship = Track 2 or Track 3 play

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

**Key Message:** Understanding SME growth challenges, providing tailored banking solutions

**Recipient Name:** Use actual name if available, generic fallback ("Dear CEO") if not

---

*Last updated: 2026-01-18*
