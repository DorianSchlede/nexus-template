# CRM Scoring Fields

> **Source**: HubSpot/Salesforce Best Practices (December 2024)
> **Usage**: Lade diese Ressource für CRM/Airtable Integration

---

## Recommended Custom Fields

### Account/Lead Object

```
FIRMOGRAPHIC:
├── Industry (Picklist)
├── Employee_Count (Number)
├── Annual_Revenue (Number)
├── Geographic_Region (Picklist)
├── Funding_Stage (Picklist)
│   Options: Pre-Seed, Seed, Series A, B, C, D+, Public, Bootstrapped
└── Company_Age (Number/Years)

TECHNOGRAPHIC:
├── Current_Tools_Used (Multi-select)
│   Options: [Your key integrations/competitors]
├── AI_Automation_Maturity (1-10 Scale)
├── Cloud_Infrastructure (Picklist)
│   Options: AWS, GCP, Azure, On-Prem, Hybrid
├── Dev_Team_Size (Number)
└── Tech_Stack_Fit (Calculated or Manual)

BEHAVIORAL (Auto-populated from tracking):
├── Website_Page_Views (Number)
├── Pricing_Page_Visits (Number)
├── Content_Downloads (Number)
├── Demo_Requests (Number)
├── Email_Engagement_Score (Number)
├── Last_Website_Visit (DateTime)
└── Days_Since_Last_Engagement (Calculated)

CALCULATED SCORES:
├── ICP_Fit_Score (Formula)
│   = Firmographic_Score + Technographic_Score
├── Engagement_Score (Formula)
│   = Sum of behavioral signals
├── Total_Lead_Score (Formula)
│   = (ICP_Fit × 0.60) + (Engagement × 0.40)
├── Lead_Grade (Formula)
│   = A/B/C/D/F based on Total_Lead_Score
└── Last_Score_Update (DateTime)
```

---

## Score Calculation Formulas

### ICP Fit Score (0-65 points)

```
Firmographic (40 pts max):
  IF Industry = [Target] THEN 15 ELSE IF Industry = [Adjacent] THEN 10 ELSE 0
  + IF Employee_Count BETWEEN 100 AND 500 THEN 15
    ELSE IF Employee_Count BETWEEN 50 AND 99 OR 501 AND 1000 THEN 10
    ELSE 5
  + IF Funding_Stage IN (Series A, B, C) THEN 10
    ELSE IF Funding_Stage = Seed THEN 5
    ELSE 0

Technographic (25 pts max):
  IF AI_Automation_Maturity >= 7 THEN 15
    ELSE IF AI_Automation_Maturity >= 4 THEN 10
    ELSE 5
  + IF Tech_Stack_Fit = "High" THEN 10
    ELSE IF Tech_Stack_Fit = "Medium" THEN 5
    ELSE 0
```

### Engagement Score (0-35 points)

```
Website_Behavior:
  IF Pricing_Page_Visits > 0 THEN 15 ELSE 0
  + MIN(Page_Views / 10, 10)  // Cap at 10 points

Content_Engagement:
  IF Demo_Request = TRUE THEN 20 ELSE 0
  + MIN(Content_Downloads × 3, 10)  // Cap at 10 points

Email_Engagement:
  IF Email_Engagement_Score > 50 THEN 5
  ELSE IF Email_Engagement_Score > 25 THEN 3
  ELSE 0

Recency_Bonus:
  IF Days_Since_Last_Engagement < 7 THEN 5
  ELSE IF Days_Since_Last_Engagement < 30 THEN 3
  ELSE 0
```

### Lead Grade Assignment

```
IF Total_Lead_Score >= 80 THEN "A"
ELSE IF Total_Lead_Score >= 60 THEN "B"
ELSE IF Total_Lead_Score >= 40 THEN "C"
ELSE IF Total_Lead_Score >= 20 THEN "D"
ELSE "F"
```

---

## Automation Rules

### HubSpot Workflows

```yaml
# High-Priority Lead Alert
Trigger: Total_Lead_Score >= 80
Actions:
  - Set Lead_Grade = "A"
  - Assign to Senior AE (round-robin)
  - Create Task: "Contact within 24h"
  - Send Slack notification to #sales-alerts
  - Add to "Hot Leads" list

# Nurture Sequence
Trigger: Total_Lead_Score BETWEEN 60 AND 79
Actions:
  - Set Lead_Grade = "B"
  - Enroll in "Nurture Sequence"
  - Create Task: "Review in 2 weeks"
  - Add to "Warm Leads" list

# Low Priority Handling
Trigger: Total_Lead_Score < 60
Actions:
  - Set Lead_Grade = "C/D"
  - Add to "Long-term Nurture" list
  - OR Mark as Disqualified if score < 20
```

### Salesforce Process Builder

```
Rule: Score_Update_Handler
Condition: ISCHANGED(Total_Lead_Score)
Actions:
  1. Recalculate Lead_Grade
  2. IF Lead_Grade changed to "A":
     - Chatter post to Owner
     - Add to High Priority Report
  3. Update Last_Score_Update = NOW()
```

---

## Airtable Implementation

### Table Structure

```
Table: Leads
├── Name (Single line text)
├── Company (Single line text)
├── Email (Email)
├── Industry (Single select)
├── Employee_Count (Number)
├── Funding_Stage (Single select)
├── AI_Maturity (Rating 1-10)
├── Tech_Stack_Fit (Single select: High/Medium/Low)
├── Demo_Requested (Checkbox)
├── Content_Downloads (Number)
├── Pricing_Page_Visited (Checkbox)
│
├── Firmographic_Score (Formula)
│   = (IF({Industry}="SaaS",15,IF({Industry}="FinTech",10,0))
│     + (IF({Employee_Count}>=100 AND {Employee_Count}<=500,15,10))
│     + (IF({Funding_Stage}="Series A",10,5)))
│
├── Engagement_Score (Formula)
│   = (IF({Demo_Requested},20,0)
│     + (IF({Pricing_Page_Visited},15,0))
│     + ({Content_Downloads}*3))
│
├── Total_Score (Formula)
│   = ({Firmographic_Score}*0.6)+({Engagement_Score}*0.4)
│
├── Lead_Grade (Formula)
│   = IF({Total_Score}>=80,"A",
│       IF({Total_Score}>=60,"B",
│         IF({Total_Score}>=40,"C","D")))
│
└── Status (Single select: New/Contacted/Qualified/Disqualified)
```

### Airtable Automations

```
Automation 1: High Score Alert
Trigger: When record matches conditions
         Total_Score >= 80
Actions:
  - Send Slack message to #sales
  - Update Status to "Hot"
  - Send email to assigned rep

Automation 2: Weekly Scoring Report
Trigger: Every Monday 9am
Actions:
  - Find records where Lead_Grade = "A" or "B"
  - Send summary email to sales team
```

---

## Negative Scoring

### Disqualification Signals

```
Anti-ICP Indicators (subtract points):
  IF Industry = [Excluded] THEN -20
  IF Employee_Count < 20 THEN -15
  IF Email_Domain = [Personal domains] THEN -10
  IF Competitor_Employee = TRUE THEN -50 (auto-disqualify)
  IF Last_Engagement > 90 days THEN -10
```

---

## Reporting Dashboard

### Key Metrics to Track

| Metric | Formula | Target |
|--------|---------|--------|
| Lead Volume by Grade | COUNT by Lead_Grade | Monitor distribution |
| Conversion by Grade | Won / Total by Grade | A > 30%, B > 15% |
| Score Accuracy | Predicted vs Actual Win | >70% correlation |
| Time to Contact (A) | First contact - Created | <24 hours |
| Disqualification Rate | DQ'd / Total | ~20% |

### Weekly Review Questions

1. Are A-grade leads converting at expected rate?
2. Are we contacting A-leads within 24h?
3. What's the score distribution of closed-won vs closed-lost?
4. Are there patterns in disqualified leads we should update ICP for?

---

## Sources

- [Understand the Lead Scoring Tool | HubSpot](https://knowledge.hubspot.com/scoring/understand-the-lead-scoring-tool)
- [Lead Scoring: How to Find Best Prospects | Salesforce](https://www.salesforce.com/blog/lead-scoring/)
- [What is Lead Scoring | MediaJunction](https://www.mediajunction.com/blog/what-is-lead-scoring)
- [Build a Lead Scoring Model in 9 Steps | Act-On](https://act-on.com/learn/blog/lead-scoring-model-building-a-framework-to-drive-conversion/)
- [Lead Scoring Examples | UserMotion](https://usermotion.com/blog/lead-scoring-examples)
- [The Best Lead Scoring Criteria | Breadcrumbs](https://breadcrumbs.io/blog/5-tried-tested-lead-scoring-criteria-2021/)
- [Account Scoring Guide | CaptivateIQ](https://www.captivateiq.com/blog/account-scoring)
