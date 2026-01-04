#!/usr/bin/env python3
"""
Generate PIPELINE_REPORT.md from companies.csv and engagement.csv
Usage: python generate_report.py
"""

import csv
from datetime import datetime, timedelta
from collections import defaultdict

def read_csv(filepath):
    """Read CSV file and return list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def safe_get(row, key, default=''):
    """Safely get value from dict"""
    return row.get(key, default).strip() if row.get(key) else default

def parse_date(date_str):
    """Parse date string to datetime, return None if invalid"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except:
        return None

def main():
    # Read data
    companies = read_csv('data/companies.csv')
    engagement = read_csv('data/engagement.csv')

    # Create engagement lookup
    engagement_map = {e['company_id']: e for e in engagement}

    # Get today's date
    today = datetime.now()
    week_from_now = today + timedelta(days=7)

    # Initialize counters
    total_companies = len(companies)
    engaged_companies = len(engagement)

    status_counts = defaultdict(int)
    sector_counts = defaultdict(int)

    qualified_leads = []
    contacted_leads = []
    kiv_leads = []
    actions_this_week = []
    overdue_actions = []

    # Process engagement data
    for eng in engagement:
        status = safe_get(eng, 'engagement_status')
        status_counts[status] += 1

        company_id = eng['company_id']
        company = next((c for c in companies if c['company_id'] == company_id), None)

        if not company:
            continue

        # Categorize by status
        if status == 'qualified':
            qualified_leads.append((eng, company))
        elif status == 'contacted':
            contacted_leads.append((eng, company))
        elif status == 'kiv':
            kiv_leads.append((eng, company))

        # Check next actions
        next_date = parse_date(safe_get(eng, 'next_action_date'))
        if next_date:
            if next_date < today:
                overdue_actions.append((eng, company))
            elif next_date <= week_from_now:
                actions_this_week.append((eng, company))

    # Count sectors
    for company in companies:
        sector = safe_get(company, 'sector')
        sector_counts[sector] += 1

    # Generate report
    report = f"""# SME Banking Pipeline Report
**Generated:** {today.strftime('%Y-%m-%d %H:%M')}

---

## Executive Summary

- **Total Companies:** {total_companies}
- **Engaged Companies:** {engaged_companies} ({int(engaged_companies/total_companies*100)}% of pipeline)
- **Not Yet Contacted:** {total_companies - engaged_companies}

### Engagement Breakdown
"""

    # Status breakdown
    for status in ['qualified', 'contacted', 'kiv', 'no_contact', 'rejected', 'tagged_elsewhere']:
        count = status_counts.get(status, 0)
        if count > 0:
            report += f"- **{status.replace('_', ' ').title()}:** {count}\n"

    report += "\n---\n\n"

    # Qualified Leads
    report += "## 🎯 Qualified Leads (Ready to Close)\n\n"
    if qualified_leads:
        report += "| Company | Contact | Revenue | Next Action | Date | Notes |\n"
        report += "|---------|---------|---------|-------------|------|-------|\n"
        for eng, company in qualified_leads:
            report += f"| **{safe_get(company, 'common_name')}** "
            report += f"| {safe_get(eng, 'contact_name') or 'TBD'} "
            report += f"| {safe_get(company, 'annual_revenue') or 'Unknown'} "
            report += f"| {safe_get(eng, 'next_action') or 'None'} "
            report += f"| {safe_get(eng, 'next_action_date') or '-'} "
            report += f"| {safe_get(eng, 'engagement_notes')[:50]}... |\n"
    else:
        report += "*No qualified leads yet. Continue outreach to contacted companies.*\n"

    report += "\n---\n\n"

    # Actions This Week
    report += "## 📅 Actions This Week\n\n"
    if actions_this_week:
        report += "| Company | Status | Next Action | Due Date | Contact |\n"
        report += "|---------|--------|-------------|----------|----------|\n"
        for eng, company in sorted(actions_this_week, key=lambda x: parse_date(safe_get(x[0], 'next_action_date')) or today):
            report += f"| **{safe_get(company, 'common_name')}** "
            report += f"| {safe_get(eng, 'engagement_status')} "
            report += f"| {safe_get(eng, 'next_action')} "
            report += f"| {safe_get(eng, 'next_action_date')} "
            report += f"| {safe_get(eng, 'contact_name') or 'TBD'} |\n"
    else:
        report += "*No actions scheduled for this week.*\n"

    report += "\n---\n\n"

    # Overdue Actions
    report += "## ⚠️ Overdue Actions\n\n"
    if overdue_actions:
        report += "| Company | Status | Next Action | Was Due | Days Overdue |\n"
        report += "|---------|--------|-------------|---------|-------------|\n"
        for eng, company in sorted(overdue_actions, key=lambda x: parse_date(safe_get(x[0], 'next_action_date')) or today):
            due_date = parse_date(safe_get(eng, 'next_action_date'))
            days_overdue = (today - due_date).days if due_date else 0
            report += f"| **{safe_get(company, 'common_name')}** "
            report += f"| {safe_get(eng, 'engagement_status')} "
            report += f"| {safe_get(eng, 'next_action')} "
            report += f"| {safe_get(eng, 'next_action_date')} "
            report += f"| {days_overdue} days |\n"
    else:
        report += "*✅ No overdue actions! Great job staying on top of follow-ups.*\n"

    report += "\n---\n\n"

    # Contacted Leads
    report += "## 📞 Contacted (In Progress)\n\n"
    if contacted_leads:
        report += "| Company | Contact | Last Contact | Next Action | Existing Bank |\n"
        report += "|---------|---------|--------------|-------------|---------------|\n"
        for eng, company in contacted_leads:
            report += f"| **{safe_get(company, 'common_name')}** "
            report += f"| {safe_get(eng, 'contact_name') or 'TBD'} "
            report += f"| {safe_get(eng, 'last_contact_date') or '-'} "
            report += f"| {safe_get(eng, 'next_action') or 'TBD'} "
            report += f"| {safe_get(eng, 'existing_banker') or 'Unknown'} |\n"
    else:
        report += "*No companies in contacted status. Start reaching out to prospects!*\n"

    report += "\n---\n\n"

    # KIV Leads
    report += "## 🔖 Keep In View (Future Opportunities)\n\n"
    if kiv_leads:
        report += "| Company | Existing Bank | Revisit Date | Reason |\n"
        report += "|---------|---------------|--------------|--------|\n"
        for eng, company in kiv_leads:
            report += f"| **{safe_get(company, 'common_name')}** "
            report += f"| {safe_get(eng, 'existing_banker') or 'Unknown'} "
            report += f"| {safe_get(eng, 'next_action_date') or 'TBD'} "
            report += f"| {safe_get(eng, 'engagement_notes')[:60]}... |\n"
    else:
        report += "*No KIV opportunities.*\n"

    report += "\n---\n\n"

    # Sector Distribution
    report += "## 📊 Pipeline by Sector\n\n"
    report += "| Sector | Companies | % of Pipeline |\n"
    report += "|--------|-----------|---------------|\n"
    for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
        pct = int(count / total_companies * 100)
        report += f"| {sector} | {count} | {pct}% |\n"

    report += "\n---\n\n"

    # Not Yet Contacted
    not_contacted = [c for c in companies if c['company_id'] not in engagement_map]
    report += f"## 🆕 Not Yet Contacted ({len(not_contacted)} companies)\n\n"
    if not_contacted:
        report += "| Company | Sector | Revenue | Priority |\n"
        report += "|---------|--------|---------|----------|\n"
        for company in not_contacted[:10]:  # Show first 10
            report += f"| {safe_get(company, 'common_name')} "
            report += f"| {safe_get(company, 'sector')} "
            report += f"| {safe_get(company, 'annual_revenue') or 'Unknown'} "
            report += f"| {safe_get(company, 'priority')} |\n"
        if len(not_contacted) > 10:
            report += f"\n*...and {len(not_contacted) - 10} more companies.*\n"

    report += "\n---\n\n"

    # Quick Commands
    report += """## 🛠️ Quick Commands

**Update engagement:**
```
"Update [Company] - contacted, spoke with [Name], next action: [action], date: [YYYY-MM-DD]"
"Mark [Company] as qualified - meeting scheduled"
"Add [Company] to KIV - existing bank is [Bank], revisit [date]"
```

**Generate reports:**
```
python generate_report.py
```

**View in browser:**
```
Open dashboard.html
```

---

*Auto-generated from companies.csv and engagement.csv*
"""

    # Write report
    with open('PIPELINE_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"PIPELINE_REPORT.md generated successfully!")
    print(f"   Total companies: {total_companies}")
    print(f"   Engaged: {engaged_companies}")
    print(f"   Qualified leads: {len(qualified_leads)}")
    print(f"   Actions this week: {len(actions_this_week)}")
    print(f"   Overdue: {len(overdue_actions)}")

if __name__ == '__main__':
    main()
