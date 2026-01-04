# Verify Leads Skill

You help the user qualify candidate companies by verifying their existence and applying business exclusion rules.

This skill moves candidates from **pending** status to either:
- **Verified** → moved to companies.csv (qualified prospects)
- **Dropped** → marked in candidates.csv with reason (excluded)

## IMPORTANT: Always Start by Reading User Parameters

**FIRST STEP - Read user parameters:**
```
Read /data/user-parameters.md
Extract:
- Exclusions (SGX, MNC, public DBS, holdco, size)
- Target sectors
```

---

## Step 1: Check for Uncommitted Changes

**Before starting verification:**
```
Check git status for uncommitted changes in:
- candidates.csv
- companies.csv

IF uncommitted changes exist:
  "You have uncommitted changes in [files].
   Commit before verifying? (yes/no)"

IF user says yes:
  Wait for user to commit ("commit this")
  Then proceed

IF user says no:
  Proceed with verification
```

---

## Step 2: Read Candidates to Verify

**Read /data/candidates.csv**

**Filter:**
- WHERE status='pending'
- Optional: If user specified sector (e.g., "Verify logistics candidates"), filter by source or company name pattern

**Count pending candidates**

**IF 0 pending candidates:**
```
"No pending candidates to verify.

Current candidates.csv status:
- [X] already verified
- [Y] already dropped

Add new candidates with: 'Scan [company]' or 'Find [criteria]'"
```
**STOP**

**IF > 0 pending candidates:**
```
"Found [N] pending candidates to verify.
Processing..."
```
**Continue to Step 3**

---

## Step 3: Verify Each Candidate

**For EACH candidate with status='pending':**

### 3a) Existence Verification

**Check website:**
```
Search: "[company_name] official website Singapore"
Look for official domain
```

**Check LinkedIn:**
```
Search: "[company_name] LinkedIn company"
Look for linkedin.com/company/[name]
```

**IF NEITHER website NOR LinkedIn found:**
- Mark as dropped
- Reason: "No website/LinkedIn found"
- **SKIP to next candidate**

**IF website OR LinkedIn found:**
- Continue to 3b

### 3b) MNC Subsidiary Check

**Look for patterns in website/search results:**
```
1. "[Company] subsidiary of [Parent MNC]"
2. "[Company] part of [Global Group]"
3. Website footer: "A [MNC] company"
4. About page mentions international parent
5. Global brand names (FedEx, DHL, UPS, Siemens, ABB, Schneider, etc.)
```

**Common MNC patterns to watch:**
- Courier: FedEx, DHL, UPS, TNT
- Logistics: DB Schenker, Kuehne+Nagel, DSV
- Industrial: Siemens, ABB, Schneider Electric
- Consulting: Accenture, IBM, Deloitte, PwC
- Tech: Microsoft, Oracle, SAP, Salesforce

**IF MNC subsidiary:**
- Mark as dropped
- Reason: "MNC subsidiary of [Parent]"
- **SKIP to next candidate**

**IF not MNC:**
- Continue to 3c

### 3c) Public DBS Mention Check

**Search:**
```
"[company_name] DBS bank"
"[company_name] banking partner"
```

**Look for explicit mentions in:**
- Press releases
- News articles (Business Times, Straits Times)
- Company announcements

**Key phrases:**
```
- "banking partner DBS"
- "facility from DBS"
- "financed by DBS"
- "DBS provided loan"
- "supported by DBS Bank"
```

**IMPORTANT:**
- Must be PUBLIC disclosure (article, press release)
- Don't exclude based on speculation or rumors
- If mentioned as one of many banks (not exclusive) → maybe OK, ask user

**IF clear public DBS mention:**
- Mark as dropped
- Reason: "Public DBS banker mention"
- **SKIP to next candidate**

**IF no DBS mention OR unclear:**
- Continue to 3d

### 3d) Holdco / Size Plausibility Check

**Look for signals:**

**Red flags for >S$100M:**
- "Holdings" or "Group" in legal name
- Listed parent company
- Wide regional presence (>5 countries, >20 locations)
- Employee count >1,000
- Multiple subsidiaries across industries
- Revenue publicly disclosed >S$100M

**Search:**
```
"[company_name] revenue"
"[company_name] group structure"
"[company_name] parent company"
```

**Decision logic:**
```
IF obvious signals (listed parent, disclosed revenue >100M, massive scale):
  Mark as dropped
  Reason: "Holdco revenue >S$100M"
  SKIP to next candidate

IF some signals but unclear (e.g., "Holdings" in name but no other info):
  Flag for review but DON'T auto-drop
  Set holdco_flag='yes' in companies.csv
  Continue to 3e (let user decide later)

IF no signals:
  Set holdco_flag='no'
  Continue to 3e
```

### 3e) Sector Validation

**Check if company's sector is in target sectors (from user-parameters.md):**
- Logistics, Supply Chain & Trade
- Manufacturing & Industrial
- Healthcare, Wellness & Life Sciences
- F&B, Retail & Consumer
- Technology & Professional Services

**IF sector not in target list:**
- Mark as dropped
- Reason: "Out of target sectors ([sector])"
- **SKIP to next candidate**

**IF sector in target list OR unknown:**
- Continue to 3f

### 3f) Extract Company Details (Passed All Checks)

**If candidate passed all exclusion checks:**

**Step 3f-1: ACRA Lookup (UEN + Paid-up Capital)**

Search for ACRA data using WebSearch:
```
Search query: "[Legal Name] UEN Singapore ACRA paid-up capital"

Look for results from:
- companies.sg
- sgpbusiness.com
- recordowl.com
- opengovsg.com

Extract:
- UEN (Unique Entity Number) - 9-10 digit code
- Paid-up Capital - SGD amount
- Company Status - Live/Struck Off
- Incorporation Date (optional)

Format paid-up capital as: "S$XXM" or "S$XX.XM"
Examples: "S$10.7M", "S$1M", "S$500K"

IF no ACRA data found:
  Leave UEN and paid_up_capital empty
  Continue with other details
```

**Step 3f-2: Extract from website/LinkedIn:**
```
- Legal name (if found, e.g., "[Name] Pte Ltd")
- Website URL
- LinkedIn URL
- Annual revenue (if publicly disclosed; otherwise estimate with "~" prefix)
  Format: "S$XXM" (declared) or "~S$XXM" (estimated)
  Examples: "S$45M", "~S$30M", "S$400M+"
  Use paid-up capital as reference if available (typical 5-20x multiplier)
- Sector (from user-parameters.md target list)
- Industry (sub-sector, e.g., "3PL/4PL", "Electronics", "Medical Devices")
```

**Set defaults:**
```
- priority = medium (user will adjust later if needed)
- confidence = MEDIUM (can upgrade to HIGH if award-winning, etc.)
- date_verified = today (YYYY-MM-DD)
- last_enriched = never
- current_stage = verified
```

**Generate company_id:**
```
- Kebab-case from company name
- Example: "YCH Group" → "ych-group"
- Example: "Supreme Components International" → "supreme-components-international"
```

**Add to companies.csv:**

**CRITICAL CSV FORMAT REQUIREMENT:**
- ALL 18 columns must be present for every row
- Empty fields must use empty string (consecutive commas: ,,)
- NEVER skip columns - preserve column order exactly
- UEN, paid_up_capital, and annual_revenue fields may be empty - must still include comma placeholders
- **VALIDATION: Every row must have exactly 17 commas (18 fields total)**

**New column order:**
```
company_id,legal_name,common_name,website,linkedin,uen,paid_up_capital,annual_revenue,sector,industry,priority,confidence,holdco_flag,date_verified,last_enriched,current_stage,assigned_to,notes
```

**Example with all fields:**
```csv
ych-group,YCH Group Pte Ltd,YCH Group,https://www.ych.com,https://linkedin.com/company/ych-group,198003684Z,S$10.7M,~S$80M,Logistics,3PL/4PL,medium,HIGH,no,2025-12-30,never,verified,,Company notes here
```
^ 17 commas = 18 fields ✓

**Example with missing website/LinkedIn/UEN but with paid-up capital:**
```csv
example-company,Example Company Pte Ltd,Example Company,,,200104742C,S$1M,~S$20M,Manufacturing,Electronics,medium,HIGH,no,2025-12-30,never,verified,,Award winner
```
^ Count after common_name: 3 empty fields (website, linkedin, uen) = 3 commas, then paid_up_capital = 17 commas total ✓

**Example with all financial fields empty:**
```csv
new-company,New Company Pte Ltd,New Company,https://example.com,,,,~S$15M,Technology,SaaS,medium,MEDIUM,no,2025-12-30,never,verified,,
```
^ Count after common_name: website (filled), then 3 empty fields (linkedin, uen, paid_up_capital) = 3 commas before annual_revenue = 17 commas total ✓

**CSV Row Construction Checklist:**
Before writing each row, verify the structure:
1. company_id (field 1)
2. legal_name (field 2)
3. common_name (field 3)
4. website (field 4) - may be empty
5. linkedin (field 5) - may be empty
6. uen (field 6) - may be empty
7. paid_up_capital (field 7) - may be empty
8. annual_revenue (field 8) - may be empty
9. sector (field 9)
10. industry (field 10)
11. priority (field 11)
12. confidence (field 12)
13. holdco_flag (field 13)
14. date_verified (field 14)
15. last_enriched (field 15)
16. current_stage (field 16)
17. assigned_to (field 17) - usually empty
18. notes (field 18) - may be empty

**Post-Write Validation:**
After writing each row, mentally count: should have exactly 17 commas

**Update candidates.csv:**
```
Change status from 'pending' to 'verified'
```

**Progress update:**
```
"✓ [Company Name] verified → moved to companies.csv"
```

### 3g) If Dropped (Failed Any Check)

**Update candidates.csv:**
```
Change status from 'pending' to 'dropped'
Add drop_reason = [reason from checks above]
```

**Progress update:**
```
"✗ [Company Name] dropped: [reason]"
```

---

## Step 4: Summary Report

**After processing all candidates:**

**Count results:**
```
- Total processed: [N]
- Verified: [X] (moved to companies.csv)
- Dropped: [Y]
```

**Breakdown of drop reasons:**
```
Dropped candidates ([Y] total):
- [A] No website/LinkedIn found
- [B] MNC subsidiaries
- [C] Public DBS banker mentions
- [D] Holdco revenue >S$100M
- [E] Out of target sectors
```

**Report format:**
```
Verification complete: [N] candidates processed

✓ [X] companies verified → moved to companies.csv
  - [List company names]

✗ [Y] companies dropped:
  - [A] No website/LinkedIn: [names]
  - [B] MNC subsidiaries: [names]
  - [C] Public DBS mentions: [names]
  - [D] Holdco >S$100M: [names]
  - [E] Out of target sectors: [names]

[X] verified companies ready for enrichment or outreach.

Next step: Generate prospect packs? OR Commit these changes?
```

---

## Step 5: Next Step Suggestions

```
"Next steps:
- Generate prospect packs: 'Generate prospect pack for [company]'
- Enrich with more triggers: (future feature)
- Commit changes: 'Commit the verified companies'
- Review holdco flags: (if any flagged for review)"
```

---

## Error Handling

**IF candidates.csv is empty (no rows):**
```
"candidates.csv is empty. No candidates to verify.

Add candidates first:
- Specific company: 'Scan [company name]'
- Broad search: 'Find [N] [sector] companies with [trigger]'"
```

**IF all candidates already verified or dropped:**
```
"All candidates already processed:
- [X] verified (in companies.csv)
- [Y] dropped

Current status: All candidates have been reviewed.

Add new candidates to verify more companies."
```

**IF candidates.csv is malformed:**
```
"Error reading candidates.csv. Please check file format.

Expected headers:
candidate_id,company_name,source,initial_trigger,date_added,status,drop_reason

If file is corrupted, restore from git history or create new file."
```

---

## Important Notes

**DO NOT auto-commit:**
- Update candidates.csv (status changed)
- Add rows to companies.csv
- User will commit separately with "commit this" command

**Holdco flag handling:**
- If uncertain about size, set holdco_flag='yes' but don't drop
- User can review these later
- Document the signals found in notes column

**Confidence ratings:**
```
HIGH: Award winners (E50, SME 500), press coverage, verified data
MEDIUM: Basic verification, some public info
LOW: Minimal public information, sparse data
```

**Priority defaults:**
- Set to 'medium' during verification
- User can adjust later based on triggers/needs
- Don't auto-assign 'high' or 'low' during verification

**Progress updates:**
- For large batches (>10 candidates), show progress every 5 companies
- Example: "Verified 5/20 candidates..."
- Keeps user informed for long operations

**Edge cases:**
- Company name variations (e.g., "YCH" vs "YCH Group") → ask user if same company
- Similar names to existing companies → check for duplicates before adding
- No clear sector → ask user to classify

**Sector classification:**
- Use best judgment from website/LinkedIn business description
- If unclear, set to closest match from target sectors list
- User can correct later if needed

---

## Validation Checklist

Before considering a candidate "verified":
- [ ] Website OR LinkedIn exists
- [ ] NOT MNC subsidiary
- [ ] NO public DBS banker mention
- [ ] Holdco plausibility pass (or flagged for review)
- [ ] Sector in target list (or user-approved)
- [ ] company_id generated (unique, kebab-case)
- [ ] Row added to companies.csv
- [ ] candidates.csv status updated to 'verified'

Before marking a candidate "dropped":
- [ ] Failed at least one exclusion check
- [ ] Drop reason clearly documented
- [ ] candidates.csv status updated to 'dropped'
- [ ] drop_reason column populated

---

You are now ready to help the user verify and qualify candidate companies for their SME banking pipeline.
