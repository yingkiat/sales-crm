# Data Schema Documentation

## Overview

All data is stored in CSV files for human readability and version control. This document defines the schema for each CSV and the relationships between them.

---

## candidates.csv

**Purpose:** Unverified leads from broad scanning (top of funnel)

**Location:** `/data/candidates.csv`

**Lifecycle:** Created by scan-leads skill → Processed by verify-leads skill → Moved to companies.csv OR marked as dropped

### Schema

| Column | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| candidate_id | string | Yes | Unique identifier (format: CAND###) | CAND001 |
| company_name | string | Yes | Company name as found in source | Acme Logistics Pte Ltd |
| source | string | Yes | Where this candidate was found | E50 2024 Awards |
| initial_trigger | string | No | First trigger observed (if any) | Won cold chain tender Dec 2024 |
| date_added | date | Yes | When added to candidates (YYYY-MM-DD) | 2025-12-30 |
| status | enum | Yes | pending / verified / dropped | pending |
| drop_reason | string | No | Why dropped (if status=dropped) | No website found |

### Sample Data

```csv
candidate_id,company_name,source,initial_trigger,date_added,status,drop_reason
CAND001,Acme Logistics Pte Ltd,E50 2024 Awards,E50 Rank #28,2025-12-30,pending,
CAND002,Beta Manufacturing,Tender search Dec 2024,Won precision engineering tender,2025-12-30,verified,
CAND003,Gamma Holdings Pte Ltd,E50 2024 Awards,,2025-12-30,dropped,MNC subsidiary - parent is SGX-listed
```

### Business Rules

**Status transitions:**
- pending → verified (passes existence + qualification checks)
- pending → dropped (fails checks or exclusion criteria)

**Drop reasons (standard values):**
- "No website found"
- "No LinkedIn company page"
- "MNC subsidiary"
- "SGX-listed company"
- "Public DBS banker mention"
- "Holdco revenue >S$100M"
- "Not Singapore entity"

---

## companies.csv

**Purpose:** Verified, qualified companies (middle to bottom of funnel)

**Location:** `/data/companies.csv`

**Lifecycle:** Created by verify-leads skill → Enriched by enrich-company skill → Updated through pipeline stages

### Schema

| Column | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| company_id | string | Yes | Unique identifier (kebab-case of company name) | ych-group |
| legal_name | string | No | Full legal name (if known) | YCH Group Pte Ltd |
| common_name | string | Yes | Display name | YCH Group |
| website | string | Yes | Official website URL | https://www.ych.com |
| linkedin | string | No | LinkedIn company page URL | https://linkedin.com/company/ych-group |
| uen | string | No | Singapore UEN (after ACRA verification) | 198201234K |
| sector | enum | Yes | Primary sector | Logistics |
| industry | string | No | Sub-sector / industry specialization | 3PL/4PL |
| priority | enum | Yes | high / medium / low | high |
| confidence | enum | Yes | HIGH / MEDIUM / LOW (data quality rating) | HIGH |
| holdco_flag | enum | No | yes / no / unknown (part of larger group?) | no |
| date_verified | date | Yes | When existence was verified (YYYY-MM-DD) | 2025-12-20 |
| last_enriched | string | Yes | When triggers were last researched (YYYY-MM-DD or "never") | 2025-12-30 |
| current_stage | enum | Yes | Pipeline stage | enriched |
| assigned_to | string | No | Owner (for multi-user future) | banker1 |
| notes | string | No | Free-form notes | E50 consistent winner, 2M sqft facilities |

### Sector Values

- Manufacturing & Industrial
- Logistics, Supply Chain & Trade
- F&B, Retail & Consumer
- Healthcare, Wellness & Life Sciences
- Technology & Professional Services

### Current Stage Values

Aligned to Accelerator framework pipeline:

1. candidate (should not appear in companies.csv - belongs in candidates.csv)
2. verified - Existence verified, basic qualification passed
3. enriched - Triggers researched and added
4. acra_verified - UEN confirmed via ACRA
5. outreach_prepared - Prospect pack generated
6. outreach_sent - Email/call made
7. response_received - Prospect responded
8. meeting_held - Discovery meeting completed
9. needs_confirmed - Banking needs validated
10. proposal_sent - Formal proposal submitted
11. onboarding - Account opening in progress
12. dropped - No longer pursuing (with notes explaining why)

### Sample Data

```csv
company_id,legal_name,common_name,website,linkedin,uen,sector,industry,priority,confidence,holdco_flag,date_verified,last_enriched,current_stage,assigned_to,notes
ych-group,YCH Group Pte Ltd,YCH Group,https://www.ych.com,https://linkedin.com/company/ych-group,,Logistics,3PL/4PL,high,HIGH,no,2025-12-20,2025-12-30,enriched,banker1,2M sqft Supply Chain City; active regional expansion
supreme-comp,Supreme Components International Pte Ltd,Supreme Components,https://www.supreme.com.sg,https://linkedin.com/company/supreme-components,,Manufacturing & Industrial,Electronics/Semiconductor,high,HIGH,no,2025-12-20,2025-12-30,enriched,,E50 12-time winner; 201% growth 2019-2022
acme-logistics,Acme Logistics Pte Ltd,Acme Logistics,https://www.acme-logistics.sg,,,Logistics,Cold Chain,medium,MEDIUM,unknown,2025-12-30,never,verified,,Recently verified; needs enrichment
```

### Business Rules

**Priority calculation (suggested):**
- High: Multiple high-strength triggers + priority sector + large scale signals
- Medium: Some triggers + relevant sector
- Low: Minimal triggers or lower-priority sector

**Confidence rating:**
- HIGH: Multiple data sources, recent information, award verification (E50, etc.)
- MEDIUM: Single source or older data
- LOW: Limited public information, unverified claims

---

## triggers.csv

**Purpose:** Evidence-based growth signals per company (enriched intelligence)

**Location:** `/data/triggers.csv`

**Lifecycle:** Created/updated by enrich-company skill → Referenced by generate-prospect-pack skill

### Schema

| Column | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| trigger_id | string | Yes | Unique identifier (format: T###) | T001 |
| company_id | string | Yes | Foreign key to companies.csv | ych-group |
| category | enum | Yes | Trigger category (7 types) | expansion |
| description | string | Yes | Specific, observable trigger | RM500M Malaysia investment |
| evidence_link | string | No | URL to verify (press release, article, etc.) | https://www.businesstimes.com.sg/... |
| date_observed | string | No | When trigger occurred (YYYY-MM or YYYY) | 2025-11 |
| strength | enum | Yes | high / medium / low | high |
| date_added | date | Yes | When added to triggers.csv (YYYY-MM-DD) | 2025-12-30 |
| added_by | string | No | How detected (skill name or "manual") | enrich-company skill |

### Trigger Categories

From Accelerator framework:

1. **expansion** - New facilities, outlets, regional expansion, JVs
2. **hiring** - Sales, ops, finance, engineer hiring spikes
3. **capex** - New machinery, fleet, equipment, cold chain, medical devices
4. **contract** - Tender wins, project awards, long-cycle contracts
5. **inventory** - Distributor/wholesaler signals, seasonal inventory buildup
6. **compliance** - MAS/regulatory requirements, certifications, regtech
7. **operational** - Multi-entity operations, cross-border flows, complexity

### Strength Rating Guidelines

**High:**
- Official company announcement (press release, website news)
- Credible news source (Business Times, Straits Times, Channel NewsAsia)
- Award recognition requiring verification (E50, SME 500)
- Recent (within 12 months)

**Medium:**
- Secondary reporting (industry blogs, aggregator sites)
- Inferred from LinkedIn job postings
- Moderately recent (12-18 months)

**Low:**
- Unverified directories
- Outdated (>18 months)
- Weak source quality

### Sample Data

```csv
trigger_id,company_id,category,description,evidence_link,date_observed,strength,date_added,added_by
T001,ych-group,expansion,RM500M Malaysia investment,https://www.businesstimes.com.sg/companies-markets/ych-group-invests-rm500m-malaysia,2025-11,high,2025-12-30,enrich-company skill
T002,ych-group,capex,US$200M Vietnam hub groundbreaking,https://www.ych.com/news/vietnam-expansion,2025-11,high,2025-12-30,enrich-company skill
T003,ych-group,expansion,YCH DistriPark Tuas opening,https://www.straitstimes.com/business/ych-opens-distripark,2025-11,high,2025-12-30,enrich-company skill
T004,supreme-comp,expansion,New Japan subsidiary,https://www.supreme.com.sg/news/japan-expansion,2024-01,high,2025-12-30,manual
T005,supreme-comp,expansion,Expanding to Europe,,2024,medium,2025-12-30,manual
```

### Banking Needs Mapping (Reference)

**Not stored in CSV** - this is logic in generate-prospect-pack skill:

| Trigger Category | Primary Banking Needs | Secondary Banking Needs |
|------------------|----------------------|------------------------|
| expansion | Facility financing, Regional expansion loans | Working capital, Multi-currency accounts |
| hiring | Working capital | Payroll financing, Equipment leasing (office) |
| capex | Equipment financing, Asset-backed lending | Leasing, Vendor financing |
| contract | Project financing, Performance guarantees | Working capital, Trade finance |
| inventory | Trade finance, Inventory financing | Receivables financing, Working capital |
| compliance | Technology loans, Compliance financing | Working capital |
| operational | Cash management, Multi-currency accounts | FX hedging, Trade finance |

---

## Relationships Between Tables

### Primary Key / Foreign Key

```
candidates.csv                    companies.csv                   triggers.csv
┌─────────────┐                  ┌─────────────┐                ┌─────────────┐
│candidate_id │                  │ company_id  │◄───────────────│ company_id  │
│    (PK)     │                  │    (PK)     │                │    (FK)     │
└─────────────┘                  └─────────────┘                └─────────────┘
```

**Join examples:**

Get all triggers for a company:
```
SELECT * FROM triggers WHERE company_id = 'ych-group'
```

Get company details with trigger count:
```
SELECT companies.common_name, COUNT(triggers.trigger_id) as trigger_count
FROM companies
LEFT JOIN triggers ON companies.company_id = triggers.company_id
GROUP BY companies.company_id
```

### Data Flow

```
scan-leads
    ↓
candidates.csv (status=pending)
    ↓
verify-leads
    ↓
companies.csv (current_stage=verified, last_enriched=never)
    ↓
enrich-company
    ↓
triggers.csv (new rows added)
companies.csv (last_enriched updated)
    ↓
generate-prospect-pack
    ↓
/documents/prospect-packs/[company]-[date].md
```

---

## Future Schema Extensions

### banking_needs.csv (Post-MVP)

Track banking product opportunities per company:

| Column | Type | Description |
|--------|------|-------------|
| need_id | string | Unique identifier |
| company_id | string | Foreign key to companies.csv |
| banking_product | enum | Trade finance, Equipment financing, etc. |
| priority | enum | high / medium / low |
| status | enum | identified / discussed / proposed / closed / declined |
| estimated_value | decimal | Estimated facility size (S$) |
| notes | string | Free-form notes |

### activities.csv (Post-MVP)

Timeline of interactions per company:

| Column | Type | Description |
|--------|------|-------------|
| activity_id | string | Unique identifier |
| company_id | string | Foreign key to companies.csv |
| date | date | When activity occurred |
| type | enum | outreach_email / call / meeting / proposal / etc. |
| outcome | string | Result of activity |
| next_action | string | Planned follow-up |
| document_link | string | Link to meeting notes or email draft |
| logged_by | string | User who logged this |

### contacts.csv (Post-MVP)

Key people at each company:

| Column | Type | Description |
|--------|------|-------------|
| contact_id | string | Unique identifier |
| company_id | string | Foreign key to companies.csv |
| name | string | Full name |
| role | string | Job title |
| linkedin | string | LinkedIn profile URL |
| email | string | Email address (if known) |
| phone | string | Phone number (if known) |
| notes | string | Relationship notes |
| last_contact_date | date | Most recent interaction |

---

## Data Validation Rules

### Required Fields Validation

**candidates.csv:**
- candidate_id, company_name, source, date_added, status are mandatory
- If status=dropped, drop_reason must be populated

**companies.csv:**
- company_id, common_name, website, sector, priority, confidence, date_verified, last_enriched, current_stage are mandatory
- last_enriched can be "never" or YYYY-MM-DD format

**triggers.csv:**
- trigger_id, company_id, category, description, strength, date_added are mandatory
- evidence_link strongly recommended (but not required for older triggers)

### Data Integrity Checks

**Foreign key integrity:**
- Every triggers.company_id must exist in companies.csv
- (Post-MVP: activities.company_id, banking_needs.company_id, contacts.company_id)

**Enum validation:**
- sector must be one of 5 defined sectors
- priority must be high/medium/low
- trigger category must be one of 7 categories
- current_stage must be valid pipeline stage

**Date format:**
- All dates in YYYY-MM-DD format
- date_observed can be YYYY-MM or YYYY (less precision acceptable)

### Uniqueness Constraints

- candidate_id must be unique in candidates.csv
- company_id must be unique in companies.csv
- trigger_id must be unique in triggers.csv
- company_id in companies.csv should not duplicate company_name (case-insensitive)

---

## CSV Formatting Standards

### Header Row
- First row contains column names
- Column names match schema exactly (case-sensitive)
- No spaces in column names (use underscores)

### Data Rows
- No empty rows
- Fields with commas must be quoted: "Description with, comma"
- Fields with quotes must escape quotes: "He said ""hello"""
- Empty fields represented as empty string (not NULL, not "null")

### Character Encoding
- UTF-8 encoding (to support Singapore company names with special characters)

### Line Endings
- Windows (CRLF) or Unix (LF) both acceptable
- Git will normalize line endings

---

## Migration and Seed Data

### Initial Population

The 77 companies from `reference/deep_research_leads.md` should be:

1. Added directly to companies.csv (skip candidates.csv since already verified)
2. Populated with triggers from the reference document
3. Set with:
   - date_verified = date of import
   - last_enriched = date of import
   - current_stage = enriched (since they already have triggers)
   - priority/confidence based on reference doc ratings

### Sample Migration Script Logic

```
For each company in deep_research_leads.md:
  1. Create company_id (kebab-case from common name)
  2. Extract: sector, industry, confidence level, key people
  3. Add row to companies.csv
  4. For each trigger in "Growth Signals" column:
     - Create trigger_id (T### sequential)
     - Parse trigger category
     - Extract description
     - Add row to triggers.csv
```

---

## Backup and Export Strategy

### Git-Based Backup
- Every commit is a backup point
- Can revert to any previous state
- Remote repository (GitHub) is off-site backup

### Export Formats
- CSVs are already export-ready (open in Excel, import to other CRMs)
- Documents folder contains markdown (human-readable, portable)

### Data Portability
- No proprietary formats
- No vendor lock-in
- Easy to migrate to traditional CRM later if needed
