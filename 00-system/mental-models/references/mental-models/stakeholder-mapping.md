---
name: "Stakeholder Mapping"
tier: 2
description: "Identify all affected parties and their influence/interest levels to manage expectations and build support. Load for Build/Strategy/Process projects with Medium/Complex complexity when multiple teams involved, organizational change required, or political dynamics impact success."
applies_to: ["Build", "Strategy", "Process"]
complexity: ["Medium", "Complex"]
---

# Stakeholder Mapping

## Purpose
Identify everyone affected by the project, understand their interests and influence, and develop strategies to build support and manage resistance.

## Core Insight

**Projects don't fail because of bad technology. They fail because of people.**

- The developer who doesn't want to learn new tools
- The executive who doesn't see the value
- The team that loses resources to your project
- The user who has to change their workflow

**Stakeholder mapping surfaces these people early, before they become blockers.**

---

## The Four Key Questions

### 1. Who Are the Stakeholders?
**Categories to Check:**

**Direct Users:**
- Who will use this daily?
- Who will use this occasionally?
- Who will be forced to use this?

**Decision Makers:**
- Who approves budget?
- Who approves timeline?
- Who can kill this project?

**Influencers:**
- Who do decision makers listen to?
- Who has credibility in this domain?
- Who controls resources you need?

**Affected Parties:**
- Whose workflow changes?
- Who loses resources/power?
- Who gains resources/power?

**Implementers:**
- Who builds this?
- Who maintains this?
- Who trains users?

**External Stakeholders:**
- Customers
- Partners
- Regulators
- Vendors

---

### 2. What Are Their Interests?
**Questions to Ask:**

**Goals:**
- What does this stakeholder want to achieve?
- How does this project help or hurt their goals?
- What's their success criteria?

**Fears:**
- What are they afraid of?
- What could they lose?
- What risks do they see?

**Constraints:**
- What limitations do they face?
- What are they measured on?
- What pressures do they have?

**Hidden Agendas:**
- What are they not saying?
- What political dynamics are at play?
- What past experiences shape their view?

---

### 3. How Much Influence Do They Have?
**Power Sources:**
- Formal authority (can approve/veto)
- Resource control (budget, people, tools)
- Expertise (domain knowledge, credibility)
- Relationships (network, trust)
- Information (knows critical details)

**Influence Levels:**
- **High:** Can kill or greenlight project alone
- **Medium:** Can significantly help or hinder
- **Low:** Limited impact on success

---

### 4. How Interested Are They?
**Interest Levels:**
- **High:** Directly impacted, cares deeply
- **Medium:** Somewhat affected, moderate care
- **Low:** Minimal impact, low engagement

---

## The Power/Interest Matrix

```
                    HIGH INTEREST
                         │
    KEEP SATISFIED       │      MANAGE CLOSELY
    ─────────────────────┼─────────────────────
    (Monitor)            │      (Partner)
                         │
L                        │                     H
O                        │                     I
W                        │                     G
                         │                     H
P                        │
O                        │                     I
W                        │                     N
E                        │                     F
R    MINIMAL EFFORT      │      KEEP INFORMED  L
    ─────────────────────┼─────────────────────  U
    (Ignore)             │      (Communicate)   E
                         │                     N
                    LOW INTEREST              C
                                              E
```

### Quadrant 1: High Power + High Interest → MANAGE CLOSELY
**Who:** Executive sponsor, primary users, key decision makers
**Strategy:**
- Involve in planning
- Regular updates
- Incorporate feedback
- Build partnership

**Example - Lead Qualification:**
- VP of Sales (can kill project, cares deeply)
- Sales Manager (uses daily, measures team on it)

### Quadrant 2: High Power + Low Interest → KEEP SATISFIED
**Who:** Senior executives, budget holders, resource controllers
**Strategy:**
- Keep satisfied but don't overload
- High-level updates
- Show value clearly
- Don't demand too much time

**Example:**
- CFO (controls budget, doesn't care about details)
- CTO (has authority, delegates to team)

### Quadrant 3: Low Power + High Interest → KEEP INFORMED
**Who:** End users, support teams, adjacent teams
**Strategy:**
- Communicate regularly
- Get feedback
- Address concerns
- Build advocates

**Example:**
- Sales reps (use daily, no veto power)
- Customer success team (affected by lead quality)

### Quadrant 4: Low Power + Low Interest → MINIMAL EFFORT
**Who:** Distant teams, peripherally affected people
**Strategy:**
- General updates
- Don't invest heavily
- Monitor for changes

**Example:**
- Accounting team (minor reporting impact)
- IT security (standard review, no special concerns)

---

## Stakeholder Analysis Template

```markdown
## Stakeholder Map

### Stakeholder: [Name/Role]

**Quadrant:** Manage Closely | Keep Satisfied | Keep Informed | Minimal Effort

**Interest Level:** High | Medium | Low
- What they care about: [...]
- How project affects them: [...]

**Influence Level:** High | Medium | Low
- Power source: [Authority/Resources/Expertise/Relationships]
- Can they kill project? Yes/No

**Position:**
- [ ] Champion (actively supports)
- [ ] Supporter (generally positive)
- [ ] Neutral (no strong opinion)
- [ ] Skeptic (has concerns)
- [ ] Blocker (actively opposes)

**Interests:**
- Goals: [What they want to achieve]
- Fears: [What they're worried about]
- Constraints: [What limits them]

**Engagement Strategy:**
- Communication frequency: [Daily/Weekly/Monthly]
- Communication method: [1-on-1/Email/Slack/Meetings]
- Key messages: [What to emphasize]
- Actions: [Specific steps to build support]

**Risks:**
- What could turn them into blocker: [...]
- Early warning signs: [...]
- Mitigation: [...]
```

---

## Example Application - Lead Qualification System

### Stakeholder 1: VP of Sales (Sarah)
**Quadrant:** MANAGE CLOSELY (High Power + High Interest)

**Interest:** High - Measures team performance, needs qualified leads
**Influence:** High - Can kill project with one email

**Position:** Skeptic (has concerns)
- Concerned AI won't understand sales nuance
- Worried about team pushback
- Burned by previous "AI solutions"

**Engagement Strategy:**
- Weekly 1-on-1 demos
- Show explainability (how AI scores)
- Involve in defining success criteria
- Quick win: Start with highest-confidence leads only

**Risk:** If accuracy <80% in first month, she'll shut it down
**Mitigation:** Set realistic expectations, start with narrow scope

---

### Stakeholder 2: Sales Manager (Mike)
**Quadrant:** MANAGE CLOSELY (Medium Power + High Interest)

**Interest:** High - Uses daily, measured on conversion rates
**Influence:** Medium - Sarah listens to him heavily

**Position:** Supporter (wants better leads)
- Frustrated with current manual process
- Wants to focus team on high-value leads
- Concerned about learning curve

**Engagement Strategy:**
- Include in design sessions
- Make him internal champion
- Train him first, he trains team
- Give him override ability (builds trust)

**Risk:** If system slows down workflow, he'll complain to Sarah
**Mitigation:** Optimize for speed, integrate seamlessly

---

### Stakeholder 3: CFO (David)
**Quadrant:** KEEP SATISFIED (High Power + Low Interest)

**Interest:** Low - Cares about ROI, not details
**Influence:** High - Controls budget

**Position:** Neutral (will approve if Sarah wants it)

**Engagement Strategy:**
- Monthly ROI dashboard
- Show cost savings (time saved)
- Keep updates high-level
- Don't request meetings

**Risk:** If costs overrun, he'll question value
**Mitigation:** Budget buffer, show value early

---

### Stakeholder 4: Sales Reps (Team of 12)
**Quadrant:** KEEP INFORMED (Low Power + High Interest)

**Interest:** High - Daily users, workflow changes
**Influence:** Low individually, Medium collectively (can revolt)

**Position:** Mixed (3 champions, 6 neutral, 3 skeptics)

**Engagement Strategy:**
- Weekly demo sessions
- Slack channel for feedback
- Highlight early wins
- Address concerns publicly

**Risk:** If 3 skeptics are vocal, can turn others against it
**Mitigation:** Win over 1-2 skeptics early, make them champions

---

### Stakeholder 5: Marketing Team (Lead Source)
**Quadrant:** KEEP INFORMED (Low Power + Medium Interest)

**Interest:** Medium - Want to know if their leads are good
**Influence:** Low - Can't block, but can complain

**Position:** Neutral (curious about scores)

**Engagement Strategy:**
- Monthly report: Lead quality by source
- Show which campaigns generate best leads
- Frame as helping them optimize

**Risk:** If scores show their leads are bad, political tension
**Mitigation:** Private feedback first, help them improve

---

## Stakeholder Engagement Strategies

### Building Champions
**Who:** Supporters and high-interest stakeholders
**How:**
- Involve early in design
- Give them influence
- Celebrate their contributions
- Make them co-creators

**Example:**
- Sales Manager designs qualification criteria
- Sales rep tests prototype, gives name to feature
- "Mike's Smart Score" feature named after him

---

### Converting Skeptics
**Who:** People with concerns but not blockers
**How:**
- Listen first (understand their fears)
- Address root cause (not just symptoms)
- Show don't tell (demo beats slides)
- Give them control (veto, override, influence)

**Example:**
- Skeptical sales rep: "AI won't understand our business"
- Solution: Let them train AI with their examples
- Result: They feel ownership, become advocate

---

### Neutralizing Blockers
**Who:** People actively opposed
**How:**
- Understand their real concern (often hidden)
- Find win-win (how project helps them)
- Reduce their risk (give them control/veto)
- Go around if necessary (escalate to their boss)

**Example:**
- IT security blocks "untrusted AI"
- Real concern: Liability if AI leaks data
- Solution: On-premise deployment, no data leaves firewall
- Result: Concern addressed, blocker becomes supporter

---

### Managing Up (High Power Stakeholders)
**Principles:**
- **No surprises:** Bad news early, in private
- **Make them look good:** Frame wins as their vision
- **Respect their time:** Concise updates, clear asks
- **Show value:** Metrics they care about

**Bad:** "We're 60% done with the AI model!"
**Good:** "Sarah, your focus on lead quality is working. Early tests show 15% higher conversion on AI-scored leads. CFO will see ROI in Q2."

---

## Common Patterns

### The Hidden Veto
**Pattern:** Someone with informal power kills project quietly
**Example:** CTO's trusted engineer says "this won't work", CTO pulls support
**Detection:** Ask "Who does [decision maker] trust?"
**Solution:** Win over the trusted advisor first

### The Absent Sponsor
**Pattern:** Executive sponsor too busy to engage
**Example:** VP approved project but never responds to updates
**Detection:** Sponsor doesn't attend meetings, doesn't read updates
**Solution:** Find active sponsor (their delegate) or escalate

### The Skeptic Coalition
**Pattern:** Multiple skeptics amplify each other's concerns
**Example:** 3 sales reps complain together, seem like "the whole team"
**Detection:** Same concerns from multiple people, coordination
**Solution:** Win over one, coalition weakens

### The Surprise Stakeholder
**Pattern:** Late-discovered stakeholder with veto power
**Example:** "Oh, compliance needs to approve? Nobody told us!"
**Detection:** New requirement appears mid-project
**Solution:** Broad stakeholder scan upfront, ask "Who else?"

---

## When to Use

**Best For:**
- ✅ Projects involving multiple teams
- ✅ Organizational change initiatives
- ✅ High political complexity
- ✅ Projects requiring adoption/behavior change
- ✅ Cross-functional initiatives
- ✅ Any project where "people problems" > "technical problems"

**Not Ideal For:**
- ❌ Solo projects (no stakeholders)
- ❌ Pure technical work (no human adoption)
- ❌ Low-stakes experiments (overkill)
- ❌ Well-understood, routine projects

**Best Timing:**
- ✅ Very early (before planning)
- ✅ When scope/approach changes (new stakeholders?)
- ✅ When blockers emerge (map and strategize)
- ✅ Before major milestones (ensure support)

**Combines Well With:**
- **Pre-Mortem** - "Which stakeholder killed the project?"
- **SWOT Analysis** - Stakeholders are opportunities and threats
- **Design Thinking** - Empathize phase maps user stakeholders
- **Systems Thinking** - Stakeholders are system components

---

## Quick Stakeholder Scan (5 Minutes)

**Fast version for simple projects:**

1. **List 5-10 key people**
   - Who decides?
   - Who uses?
   - Who's affected?

2. **Quick Power/Interest Rating**
   - H/M/L for each

3. **Identify Critical Few (2-3 people)**
   - Who can kill this?
   - Who must champion this?

4. **One Strategy Each**
   - What's the one thing you need from them?
   - What's the one thing they need from you?

**Example:**
```
1. Sarah (VP Sales) - High/High → Need her approval → Show ROI
2. Mike (Manager) - Med/High → Need him to champion → Make him co-designer
3. David (CFO) - High/Low → Need budget → Monthly ROI update
```

---

**Remember:** Every project is a people project. Technology is the easy part!
