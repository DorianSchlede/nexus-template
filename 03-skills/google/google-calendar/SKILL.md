---
name: google-calendar
version: 1.0
description: "Read, create, and manage Google Calendar events. Load when user mentions 'google calendar', 'calendar', 'schedule', 'meeting', 'event', 'appointment', 'book time', 'check availability', 'find slots', 'free time', or references scheduling/calendar operations."
---

## Purpose

Automate Google Calendar operations including listing events, checking availability, creating meetings, and managing attendees. Particularly useful for sales teams scheduling calls, finding available slots to propose to clients, and managing recurring meetings.

# Google Calendar

Read, create, and manage Google Calendar events via OAuth authentication.

---

## CRITICAL SAFETY RULES

**These rules are MANDATORY and must NEVER be bypassed:**

### 1. NEVER Create Events Without Explicit Approval
- **ALWAYS** show the user the complete event details before creating
- **ALWAYS** ask for explicit confirmation: "Create this event? (yes/no)"
- **NEVER** auto-create events, even if user says "schedule a meeting"
- **NEVER** create multiple events in a loop without per-event confirmation

### 2. Calendar Invites Alert Attendees
- When an event has attendees, creating/updating/deleting it sends notifications
- **ALWAYS** warn the user: "Attendees will receive a calendar invite!"
- Consider the impact before modifying events with external participants

### 3. Recurring Events Need Extra Care
- Modifying a recurring event can affect all instances
- **WARN** user when working with recurring events
- Ask whether to modify single instance or all occurrences

### 4. Confirm Deletions
- **ALWAYS** show event details before deleting
- If event has attendees: "Attendees will be notified of cancellation"
- **REQUIRE** explicit confirmation before delete

### 5. Safe Operations (No Confirmation Needed)
These do NOT require confirmation:
- List events
- Get event details
- List calendars
- Search events
- Check availability (freebusy)
- Find available slots

---

## Pre-Flight Check (ALWAYS RUN FIRST)

```bash
python3 00-system/skills/google/google-master/scripts/google_auth.py --check --service calendar
```

**Exit codes:**
- **0**: Ready to use - proceed with user request
- **1**: Need to login - run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
- **2**: Missing credentials or dependencies - see [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

---

## Quick Reference

### List Upcoming Events
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py list --max 10
```

### List Today's Events
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py list --from "today" --to "tomorrow"
```

### List This Week's Events
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py list --from "2025-12-16" --to "2025-12-20"
```

### Get Event Details
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py get <event_id>
```

### List Calendars
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py calendars
```

### Search Events
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py search "sales call"
```

### Check Availability
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py freebusy --from "2025-12-16T09:00" --to "2025-12-16T17:00"
```

### Find Available Slots (Sales Priority)
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py find-slots --duration 30 --from "2025-12-16" --to "2025-12-20" --hours "9-17"
```

### Create Event
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py create \
  --summary "Sales Call with Acme Corp" \
  --start "2025-12-16T14:00" \
  --end "2025-12-16T14:30" \
  --attendees "john@acme.com" \
  --reminder-popup 15
```

### Quick Add (Natural Language)
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py quick-add "Meeting with John tomorrow at 3pm"
```

### Update Event
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py update <event_id> \
  --start "2025-12-17T15:00" \
  --end "2025-12-17T15:30"
```

### Delete Event
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py delete <event_id>
```

### Add Attendees
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py add-attendees <event_id> --attendees "user@example.com"
```

### Remove Attendees
```bash
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py remove-attendees <event_id> --attendees "user@example.com"
```

---

## Common Workflows (Sales-Focused)

### Check Today's Schedule

User: "What's on my calendar today?"

1. List events for today
2. Summarize meetings with times and attendees
3. Highlight any gaps for potential meetings

```python
from calendar_operations import list_events
from datetime import datetime, timedelta

today = datetime.now().strftime("%Y-%m-%d")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

events = list_events(time_min=today, time_max=tomorrow)

for event in events:
    print(f"{event['summary']} - {event['start']}")
```

### Find Available Slots for Client

User: "Find 30-minute slots this week for a client call"

```python
from calendar_operations import find_slots

slots = find_slots(
    duration_minutes=30,
    time_min="2025-12-16",
    time_max="2025-12-20",
    working_hours=(9, 17)
)

print("Available slots:")
for slot in slots[:5]:
    print(f"  {slot['start']} - {slot['end']}")
```

### Schedule a Sales Call

User: "Schedule a call with john@acme.com tomorrow at 2pm"

```python
from calendar_operations import create_event

event = create_event(
    summary="Sales Call - Acme Corp",
    start="2025-12-17T14:00",
    end="2025-12-17T14:30",
    attendees=["john@acme.com"],
    reminders={'popup': 15},
    description="Discovery call to discuss needs"
)

print(f"Created: {event['htmlLink']}")
```

### Reschedule a Meeting

User: "Move the Acme call to Thursday at 3pm"

```python
from calendar_operations import update_event

result = update_event(
    event_id="abc123",
    start="2025-12-19T15:00",
    end="2025-12-19T15:30"
)
# Attendees are automatically notified
```

### Set Up Recurring Check-ins

User: "Set up weekly calls with the client every Tuesday at 10am"

```python
from calendar_operations import create_event

event = create_event(
    summary="Weekly Check-in - Acme Corp",
    start="2025-12-17T10:00",
    end="2025-12-17T10:30",
    attendees=["john@acme.com"],
    recurrence=["RRULE:FREQ=WEEKLY;BYDAY=TU;COUNT=12"],
    reminders={'popup': 15}
)
```

### Check If Free for a Meeting

User: "Am I free Thursday at 2pm?"

```python
from calendar_operations import get_freebusy

result = get_freebusy(
    time_min="2025-12-19T14:00",
    time_max="2025-12-19T15:00"
)

if result['primary']['is_free']:
    print("Yes, that time is available!")
else:
    print("You have a conflict during that time")
```

---

## Available Operations

| Operation | Function | Description |
|-----------|----------|-------------|
| **List** | `list_events()` | List upcoming events with filters |
| **Get** | `get_event()` | Get full event details |
| **Calendars** | `list_calendars()` | List all accessible calendars |
| **Search** | `search_events()` | Search events by keyword |
| **FreeBusy** | `get_freebusy()` | Check availability for time range |
| **Find Slots** | `find_slots()` | Find available meeting slots |
| **Create** | `create_event()` | Create new event |
| **Quick Add** | `quick_add()` | Create from natural language |
| **Update** | `update_event()` | Modify existing event |
| **Delete** | `delete_event()` | Delete event |
| **Add Attendees** | `add_attendees()` | Add people to event |
| **Remove Attendees** | `remove_attendees()` | Remove people from event |

---

## Recurrence Rules

Use RRULE format for recurring events:

| Pattern | RRULE |
|---------|-------|
| Daily | `RRULE:FREQ=DAILY` |
| Weekly | `RRULE:FREQ=WEEKLY` |
| Every Tuesday | `RRULE:FREQ=WEEKLY;BYDAY=TU` |
| Bi-weekly | `RRULE:FREQ=WEEKLY;INTERVAL=2` |
| Monthly | `RRULE:FREQ=MONTHLY` |
| 10 occurrences | `RRULE:FREQ=WEEKLY;COUNT=10` |
| Until date | `RRULE:FREQ=WEEKLY;UNTIL=20251231T000000Z` |

---

## Error Handling

See [../google-master/references/error-handling.md](../google-master/references/error-handling.md) for common errors and solutions.

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Run `google_auth.py --login` |
| 403 Forbidden | No access to calendar | Check calendar sharing settings |
| 404 Not Found | Wrong event/calendar ID | Verify the ID is correct |
| "Access blocked" | User not in test users | Add to OAuth consent screen test users |
| Rate limit exceeded | Too many requests | Wait and retry |

---

## Python Import Usage

```python
import sys
sys.path.insert(0, "03-skills/google-calendar/scripts")

from calendar_operations import (
    list_events,
    get_event,
    list_calendars,
    search_events,
    get_freebusy,
    find_slots,
    create_event,
    quick_add,
    update_event,
    delete_event,
    add_attendees,
    remove_attendees
)

# List upcoming events
events = list_events(max_results=5)

# Find available 30-min slots
slots = find_slots(
    duration_minutes=30,
    time_min="2025-12-16",
    time_max="2025-12-20"
)

# Create event with attendee
event = create_event(
    summary="Sales Call",
    start="2025-12-17T14:00",
    end="2025-12-17T14:30",
    attendees=["client@company.com"],
    reminders={'popup': 15}
)

# Check availability
freebusy = get_freebusy(
    time_min="2025-12-17T09:00",
    time_max="2025-12-17T17:00"
)
```

---

## Calendar Selection

By default, all operations use the primary calendar. To use a different calendar:

```bash
# List events from a specific calendar
python calendar_operations.py list --calendar "work@group.calendar.google.com"

# Create event on specific calendar
python calendar_operations.py create --calendar "sales@company.com" --summary "Team Meeting" ...
```

To find available calendar IDs:
```bash
python calendar_operations.py calendars
```

---

## Setup

First-time setup: [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

**Quick start:**
1. `pip install google-auth google-auth-oauthlib google-api-python-client`
2. Create OAuth credentials in Google Cloud Console (enable Google Calendar API, choose "Desktop app")
3. Add to `.env` file at Nexus root:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_PROJECT_ID=your-project-id
   ```
4. Run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`

---

## Security Notes

### Permission Scope

- **Read permissions** - Can view all calendars and events
- **Write permissions** - Can create, modify, delete events
- **Tokens stored locally** - In `01-memory/integrations/google-token.json`

### Data Privacy

- Event data is processed locally, not stored
- Tokens grant access only to the authenticated user's calendars
- Sharing the skill does NOT give others access to your calendar
- Each team member authenticates with their own Google account
