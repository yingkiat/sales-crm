## Human–AI Hybrid Acquisition Accelerator for Singapore SME Banking (< S$100m)

### Concept

A **repeatable human–AI acquisition system** that turns public “signals” into **prioritized prospects**, packages them into **banker-ready outreach**, and runs a **transparent, auditable funnel** from discovery → outreach → meeting → onboarding. The AI does the **breadth + consistency** work; the banker does the **judgement + relationships + credit intuition** work.

### Premise

1. **SME acquisition is a funnel problem**, not a single perfect list problem.
2. In the AI world, the winning model is **human judgement on top of machine-scale scanning**, not replacing the banker.
3. The system must be **non–black box**: every lead must have **observable evidence**, explicit trigger(s), and a documented reason it was selected.
4. Fit must respect SME constraints: **group/holdco aggregated revenue must plausibly be < S$100m**; SMEs may be in a group but not a large-corp holdco.
5. Existing bank relationship is **not a trigger**; we only exclude entities that **publicly disclose** DBS as banker (where required by your rules).

---

## The Accelerator Framework (3-part)

### Accelerator 1 — Signal-to-Prospect Engine (Discovery & Prioritization)

**Goal:** Build a **real, verifiable prospect universe** and rank it by business relevance using transparent triggers.

**Inputs**

* Target industries (example): **logistics, tech, precision/semicon ecosystem, marine engineering, medical/healthcare**
* Hard constraints: **Singapore operating entities**, **not obvious MNC subsidiaries**, **holdco < S$100m plausible**
* Trigger library (below)

**Trigger library (transparent categories)**

* **Expansion triggers:** new facilities, new outlets/clinics, new warehouses, regional expansion
* **Hiring spikes:** sales, ops, finance, engineers (indicates growth or capability build-out)
* **Capex/equipment triggers:** new machinery, fleet, cold-chain assets, medical equipment
* **Contract/order book triggers:** tender wins, project awards, long-cycle projects
* **Inventory/cash-cycle triggers:** distributors, wholesalers, pharma/device supply (working capital need)
* **Compliance/regulation triggers:** MAS/regulated demand (cyber/regtech), healthcare compliance
* **Operational complexity triggers:** multi-entity operations, cross-border flows (cash management + trade)

**Non-black-box rules**

* Every lead must carry:

  * **Industry tag**
  * **Trigger category**
  * **Concrete evidence to verify**
  * **Confidence score** (e.g., High/Med/Low based on evidence strength)

**Existence verification gate**

* Lead must be **web-verifiable** (company site / LinkedIn / credible directory mention).
* ACRA is a **downstream validation step** for your intern (exact legal name + UEN).

**Output**

* A prioritized lead list with **evidence-driven triggers**, not guesses.

---

### Accelerator 2 — Banker Copilot for Outreach (Personalization & Packaging)

**Goal:** Convert ranked prospects into **banker-ready engagement packs** that increase response rate and meeting conversion.

**For each prospect, generate a “Prospect Pack”**

1. **Company snapshot** (what they do, likely business model)
2. **Trigger interpretation** (why now; what changed)
3. **Likely banking needs (hypotheses)** aligned to triggers:

   * Working capital (AR/AP cycle, inventory)
   * Trade finance (imports/exports, distributors)
   * Equipment/fleet financing (capex trigger)
   * Property-backed facilities (expansion trigger)
   * Cash management (multi-entity, payroll, collections)
   * FX/hedging (cross-border operations)
4. **Outreach angles (2–3 options)**:

   * “Growth support”
   * “Efficiency / cash-cycle improvement”
   * “Risk / resiliency”
5. **Outreach artifacts**

   * Email draft (short, credible, non-salesy)
   * WhatsApp/LinkedIn note (optional)
   * Call opener script + 3 discovery questions
6. **Next-step CTA options**

   * 15–20 min intro call
   * facility walk-through / ops discussion
   * quick diagnostic on cash-cycle / FX exposure

**Guardrails**

* No claims that the banker already knows confidential details.
* Everything ties back to an **observable trigger**.

**Output**

* A set of prospect-specific messages and meeting prep notes that can be executed immediately.

---

### Accelerator 3 — Funnel Governance & Learning Loop (Execution Tracking & Improvement)

**Goal:** Make the system **repeatable**, measurable, and improvable—so you can defend it to MD and scale with an intern.

**Pipeline stages (example)**

1. Candidate (unverified)
2. Verified Existence (web)
3. ACRA Verified (legal name + UEN)
4. Holdco Revenue Plausibility Pass (< S$100m)
5. Trigger Evidence Confirmed
6. Outreach Sent
7. Response / Follow-up
8. Meeting Held
9. Needs Confirmed
10. Proposal / Solutioning
11. Onboarding / Account Opened
12. Dropped (with reason)

**Metrics (non-black-box)**

* Leads generated per cycle
* % passing existence verification
* % passing ACRA + holdco gate
* Outreach-to-response rate
* Response-to-meeting rate
* Meeting-to-onboarding rate
* Top trigger types that convert
* Top industries that convert
* Drop reasons (e.g., too large, MNC group, wrong segment, no response)

**Learning loop**

* Every month/iteration:

  * Identify which triggers correlate with conversion
  * Refine trigger weights
  * Improve outreach templates
  * Improve exclusion rules (e.g., common “too big” patterns)

**Output**

* A governed acquisition engine that improves over time and can be operationalized by a junior resource.

---

## End-to-End Steps (what a coding LLM should implement)

### Step 0 — Configuration

* Define:

  * industries
  * geography (Singapore)
  * SME constraints (holdco < S$100m)
  * exclusion rules (public DBS banker mention; obvious MNC subsidiaries)
  * trigger library + weights
  * output schema (Excel/DB tables)

### Step 1 — Candidate Sourcing

* Two modes (choose one or support both):

  1. **Corpus-based sourcing** (award lists, directories, associations)
  2. **Web search discovery** (keyword + industry + “Singapore Pte Ltd” patterns)

### Step 2 — Existence Verification (mandatory)

For each candidate:

* verify at least 1–2 of:

  * official website
  * LinkedIn company page
  * credible directory/profile (Crunchbase, SGPBusiness, etc.)
* store verification links
* if fail → drop

### Step 3 — Group/Holdco Plausibility Check (mandatory gate)

* detect whether the company is part of a group:

  * “Holdings”, “Group”, related entities, corporate structure pages
* flag risk:

  * listed parent
  * obvious conglomerate ownership
  * wide regional subsidiary network
* mark pass/fail/needs-human-check

### Step 4 — Trigger Detection

For each surviving company:

* scan public signals:

  * hiring (LinkedIn jobs)
  * press releases/news
  * tenders/awards
  * facility expansions
  * partnerships/product launches
* map each signal to trigger categories
* assign trigger strength score + confidence

### Step 5 — Prioritization

* compute a transparent score:

  * Industry weight
  * Trigger strength
  * Evidence confidence
  * Segment fit score (SME plausibility)
* output ranked list with full audit trail

### Step 6 — Prospect Pack Generation

For top N prospects:

* generate:

  * hypothesis needs
  * outreach email + short message
  * call script + discovery questions
  * meeting prep bullet points
* store versioned artifacts

### Step 7 — CRM / Tracker Update

* write rows into master tracker with:

  * company details
  * triggers + evidence links
  * verification status
  * stage fields
  * owner (you/intern)
  * timestamps

### Step 8 — Feedback & Learning

* after outreach/meetings:

  * capture outcomes + drop reasons
* periodically re-train scoring weights (rule-based or simple analytics)
* refine trigger library and templates

---

## Deliverable Data Model (minimum columns)

* Company Legal Name
* Website
* LinkedIn URL
* Industry Group
* Trigger Categories
* Trigger Evidence Links
* Evidence Confidence (H/M/L)
* Holdco / Group Flag (Y/N)
* Holdco Revenue Plausibility (< S$100m) (Pass/Fail/Review)
* Public DBS Mention (Y/N/Unknown)
* Stage
* Outreach Sent (date)
* Meeting Held (date)
* Outcome (Open / In progress / Dropped)
* Drop Reason
* Notes

---

## What the MD value proposition is (no timing claims)

* **Human-AI hybridization**: banker focuses on judgement + relationships; AI handles scale, consistency, and packaging.
* **Higher coverage with governance**: broader market scanning without losing control or credibility.
* **Transparent acquisition discipline**: every prospect is explainable via triggers and evidence, not “AI magic”.
* **Repeatable engine**: can be run by an intern and scaled over time with improving conversion intelligence.
