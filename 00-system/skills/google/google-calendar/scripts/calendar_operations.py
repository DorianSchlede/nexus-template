#!/usr/bin/env python3
"""
Google Calendar Operations

All operations for Google Calendar:
- list: List upcoming events
- get: Get event details
- calendars: List calendars
- search: Search events
- freebusy: Check availability
- find-slots: Find available meeting slots
- create: Create new event
- quick-add: Create event from natural language
- update: Update existing event
- delete: Delete event
- add-attendees: Add attendees to event
- remove-attendees: Remove attendees from event
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Find Nexus root
def find_nexus_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()

NEXUS_ROOT = find_nexus_root()

# Import from google-master shared auth
sys.path.insert(0, str(NEXUS_ROOT / "00-system" / "skills" / "google" / "google-master" / "scripts"))
from google_auth import get_credentials, get_service as _get_service, check_dependencies

def get_service():
    """Get authenticated Google Calendar service."""
    return _get_service('calendar')

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def parse_datetime(dt_str):
    """Parse datetime string to RFC3339 format."""
    if not dt_str:
        return None

    # If already has timezone info, return as-is
    if 'T' in dt_str and ('+' in dt_str or 'Z' in dt_str):
        return dt_str

    # Parse common formats
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(dt_str, fmt)
            return dt.isoformat()
        except ValueError:
            continue

    return dt_str

def format_event_time(event):
    """Format event start/end times for display."""
    start = event.get('start', {})
    end = event.get('end', {})

    # All-day event
    if 'date' in start:
        start_str = start['date']
        end_str = end.get('date', '')
        return f"{start_str} (all day)"

    # Timed event
    start_dt = start.get('dateTime', '')
    end_dt = end.get('dateTime', '')

    if start_dt:
        try:
            start_parsed = datetime.fromisoformat(start_dt.replace('Z', '+00:00'))
            end_parsed = datetime.fromisoformat(end_dt.replace('Z', '+00:00')) if end_dt else None

            start_str = start_parsed.strftime("%Y-%m-%d %H:%M")
            if end_parsed:
                if start_parsed.date() == end_parsed.date():
                    end_str = end_parsed.strftime("%H:%M")
                else:
                    end_str = end_parsed.strftime("%Y-%m-%d %H:%M")
                return f"{start_str} - {end_str}"
            return start_str
        except:
            pass

    return start_dt or start.get('date', 'Unknown')

def get_now_rfc3339():
    """Get current time in RFC3339 format."""
    return datetime.utcnow().isoformat() + 'Z'

# =============================================================================
# LIST/SEARCH OPERATIONS
# =============================================================================

def list_events(calendar_id='primary', time_min=None, time_max=None,
                max_results=10, query=None, single_events=True):
    """
    List upcoming events.

    Args:
        calendar_id: Calendar ID ('primary' for main calendar)
        time_min: Start of time range (RFC3339 or parseable string)
        time_max: End of time range (RFC3339 or parseable string)
        max_results: Maximum number of events to return
        query: Free text search query
        single_events: If True, expand recurring events into instances

    Returns:
        List of events
    """
    service = get_service()

    params = {
        'calendarId': calendar_id,
        'maxResults': max_results,
        'singleEvents': single_events,
        'orderBy': 'startTime' if single_events else 'updated',
    }

    if time_min:
        params['timeMin'] = parse_datetime(time_min) or get_now_rfc3339()
    else:
        params['timeMin'] = get_now_rfc3339()

    if time_max:
        params['timeMax'] = parse_datetime(time_max)

    if query:
        params['q'] = query

    results = service.events().list(**params).execute()
    events = results.get('items', [])

    return [
        {
            'id': event['id'],
            'summary': event.get('summary', '(No title)'),
            'start': event.get('start', {}),
            'end': event.get('end', {}),
            'location': event.get('location', ''),
            'description': event.get('description', ''),
            'attendees': event.get('attendees', []),
            'htmlLink': event.get('htmlLink', ''),
            'status': event.get('status', ''),
            'recurrence': event.get('recurrence', []),
        }
        for event in events
    ]

def get_event(event_id, calendar_id='primary'):
    """
    Get details of a specific event.

    Args:
        event_id: The event ID
        calendar_id: Calendar ID

    Returns:
        Event details
    """
    service = get_service()

    event = service.events().get(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()

    return {
        'id': event['id'],
        'summary': event.get('summary', '(No title)'),
        'start': event.get('start', {}),
        'end': event.get('end', {}),
        'location': event.get('location', ''),
        'description': event.get('description', ''),
        'attendees': event.get('attendees', []),
        'organizer': event.get('organizer', {}),
        'creator': event.get('creator', {}),
        'htmlLink': event.get('htmlLink', ''),
        'status': event.get('status', ''),
        'recurrence': event.get('recurrence', []),
        'reminders': event.get('reminders', {}),
        'created': event.get('created', ''),
        'updated': event.get('updated', ''),
    }

def list_calendars():
    """
    List all calendars the user has access to.

    Returns:
        List of calendars with id, summary, and access role
    """
    service = get_service()

    results = service.calendarList().list().execute()
    calendars = results.get('items', [])

    return [
        {
            'id': cal['id'],
            'summary': cal.get('summary', ''),
            'description': cal.get('description', ''),
            'primary': cal.get('primary', False),
            'accessRole': cal.get('accessRole', ''),
            'backgroundColor': cal.get('backgroundColor', ''),
            'timeZone': cal.get('timeZone', ''),
        }
        for cal in calendars
    ]

def search_events(query, calendar_id='primary', max_results=10,
                  time_min=None, time_max=None):
    """
    Search events by keyword.

    Args:
        query: Search query
        calendar_id: Calendar ID
        max_results: Maximum results
        time_min: Start of time range
        time_max: End of time range

    Returns:
        List of matching events
    """
    return list_events(
        calendar_id=calendar_id,
        time_min=time_min,
        time_max=time_max,
        max_results=max_results,
        query=query
    )

def get_freebusy(time_min, time_max, calendars=None):
    """
    Check availability (free/busy) for a time range.

    Args:
        time_min: Start of time range
        time_max: End of time range
        calendars: List of calendar IDs to check (default: ['primary'])

    Returns:
        Free/busy information for each calendar
    """
    service = get_service()

    if calendars is None:
        calendars = ['primary']

    body = {
        'timeMin': parse_datetime(time_min),
        'timeMax': parse_datetime(time_max),
        'items': [{'id': cal_id} for cal_id in calendars]
    }

    results = service.freebusy().query(body=body).execute()

    freebusy = {}
    for cal_id, data in results.get('calendars', {}).items():
        busy_periods = data.get('busy', [])
        freebusy[cal_id] = {
            'busy': busy_periods,
            'is_free': len(busy_periods) == 0
        }

    return freebusy

def find_slots(duration_minutes, time_min, time_max, calendar_id='primary',
               working_hours=(9, 17), slot_interval=30):
    """
    Find available meeting slots within a time range.

    Args:
        duration_minutes: Required meeting duration
        time_min: Start of search range
        time_max: End of search range
        calendar_id: Calendar to check
        working_hours: Tuple of (start_hour, end_hour) for business hours
        slot_interval: Interval between slot start times in minutes

    Returns:
        List of available time slots
    """
    service = get_service()

    # Parse time range
    start_dt = datetime.fromisoformat(parse_datetime(time_min).replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(parse_datetime(time_max).replace('Z', '+00:00'))

    # Get busy periods
    freebusy_result = get_freebusy(time_min, time_max, [calendar_id])
    busy_periods = freebusy_result.get(calendar_id, {}).get('busy', [])

    # Parse busy periods
    busy_ranges = []
    for period in busy_periods:
        busy_start = datetime.fromisoformat(period['start'].replace('Z', '+00:00'))
        busy_end = datetime.fromisoformat(period['end'].replace('Z', '+00:00'))
        busy_ranges.append((busy_start, busy_end))

    # Find available slots
    available_slots = []
    current = start_dt
    duration = timedelta(minutes=duration_minutes)
    interval = timedelta(minutes=slot_interval)

    while current + duration <= end_dt:
        slot_end = current + duration

        # Check if within working hours
        if working_hours:
            if current.hour < working_hours[0] or slot_end.hour > working_hours[1]:
                current += interval
                continue
            # Skip weekends
            if current.weekday() >= 5:
                current += interval
                continue

        # Check if slot conflicts with any busy period
        is_available = True
        for busy_start, busy_end in busy_ranges:
            # Check for overlap
            if current < busy_end and slot_end > busy_start:
                is_available = False
                break

        if is_available:
            available_slots.append({
                'start': current.isoformat(),
                'end': slot_end.isoformat(),
                'duration_minutes': duration_minutes
            })

        current += interval

    return available_slots

# =============================================================================
# CREATE/UPDATE/DELETE OPERATIONS
# =============================================================================

def create_event(summary, start, end, calendar_id='primary',
                 description=None, location=None, attendees=None,
                 reminders=None, recurrence=None, all_day=False,
                 timezone=None):
    """
    Create a new calendar event.

    Args:
        summary: Event title
        start: Start time (ISO format or datetime string)
        end: End time (ISO format or datetime string)
        calendar_id: Calendar ID
        description: Event description
        location: Event location
        attendees: List of email addresses
        reminders: Dict with 'popup' and/or 'email' keys (minutes before)
        recurrence: List of RRULE strings (e.g., ['RRULE:FREQ=WEEKLY;COUNT=10'])
        all_day: If True, create an all-day event
        timezone: Timezone for the event

    Returns:
        Created event details
    """
    service = get_service()

    event = {
        'summary': summary,
    }

    # Handle all-day vs timed events
    if all_day:
        event['start'] = {'date': start[:10]}  # Just the date part
        event['end'] = {'date': end[:10]}
    else:
        # Get default timezone from calendar if not provided
        if not timezone:
            try:
                cal_info = service.calendars().get(calendarId=calendar_id).execute()
                timezone = cal_info.get('timeZone', 'UTC')
            except:
                timezone = 'UTC'

        start_dt = {'dateTime': parse_datetime(start), 'timeZone': timezone}
        end_dt = {'dateTime': parse_datetime(end), 'timeZone': timezone}
        event['start'] = start_dt
        event['end'] = end_dt

    if description:
        event['description'] = description

    if location:
        event['location'] = location

    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]

    if reminders:
        override_reminders = []
        if 'popup' in reminders:
            override_reminders.append({'method': 'popup', 'minutes': reminders['popup']})
        if 'email' in reminders:
            override_reminders.append({'method': 'email', 'minutes': reminders['email']})

        if override_reminders:
            event['reminders'] = {
                'useDefault': False,
                'overrides': override_reminders
            }

    if recurrence:
        event['recurrence'] = recurrence if isinstance(recurrence, list) else [recurrence]

    result = service.events().insert(
        calendarId=calendar_id,
        body=event,
        sendUpdates='all' if attendees else 'none'
    ).execute()

    return {
        'id': result['id'],
        'summary': result.get('summary', ''),
        'start': result.get('start', {}),
        'end': result.get('end', {}),
        'htmlLink': result.get('htmlLink', ''),
        'status': 'created',
        'attendees_notified': bool(attendees)
    }

def quick_add(text, calendar_id='primary'):
    """
    Create an event from natural language text.

    Args:
        text: Natural language event description
              (e.g., "Meeting with John tomorrow at 3pm")
        calendar_id: Calendar ID

    Returns:
        Created event details
    """
    service = get_service()

    result = service.events().quickAdd(
        calendarId=calendar_id,
        text=text
    ).execute()

    return {
        'id': result['id'],
        'summary': result.get('summary', ''),
        'start': result.get('start', {}),
        'end': result.get('end', {}),
        'htmlLink': result.get('htmlLink', ''),
        'status': 'created'
    }

def update_event(event_id, calendar_id='primary', summary=None, start=None,
                 end=None, description=None, location=None,
                 reminders=None, all_day=None):
    """
    Update an existing event.

    Args:
        event_id: Event ID to update
        calendar_id: Calendar ID
        summary: New title (optional)
        start: New start time (optional)
        end: New end time (optional)
        description: New description (optional)
        location: New location (optional)
        reminders: New reminders (optional)
        all_day: Convert to/from all-day event (optional)

    Returns:
        Updated event details
    """
    service = get_service()

    # Get existing event
    event = service.events().get(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()

    # Apply updates
    if summary is not None:
        event['summary'] = summary

    if start is not None:
        if all_day:
            event['start'] = {'date': start[:10]}
        else:
            event['start'] = {'dateTime': parse_datetime(start)}

    if end is not None:
        if all_day:
            event['end'] = {'date': end[:10]}
        else:
            event['end'] = {'dateTime': parse_datetime(end)}

    if description is not None:
        event['description'] = description

    if location is not None:
        event['location'] = location

    if reminders is not None:
        override_reminders = []
        if 'popup' in reminders:
            override_reminders.append({'method': 'popup', 'minutes': reminders['popup']})
        if 'email' in reminders:
            override_reminders.append({'method': 'email', 'minutes': reminders['email']})

        event['reminders'] = {
            'useDefault': False if override_reminders else True,
            'overrides': override_reminders
        }

    # Check if event has attendees
    has_attendees = bool(event.get('attendees'))

    result = service.events().update(
        calendarId=calendar_id,
        eventId=event_id,
        body=event,
        sendUpdates='all' if has_attendees else 'none'
    ).execute()

    return {
        'id': result['id'],
        'summary': result.get('summary', ''),
        'start': result.get('start', {}),
        'end': result.get('end', {}),
        'htmlLink': result.get('htmlLink', ''),
        'status': 'updated',
        'attendees_notified': has_attendees
    }

def delete_event(event_id, calendar_id='primary', notify_attendees=True):
    """
    Delete an event.

    Args:
        event_id: Event ID to delete
        calendar_id: Calendar ID
        notify_attendees: Whether to notify attendees of cancellation

    Returns:
        Deletion status
    """
    service = get_service()

    # Get event first to check for attendees
    try:
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        has_attendees = bool(event.get('attendees'))
        event_summary = event.get('summary', '(No title)')
    except:
        has_attendees = False
        event_summary = '(Unknown)'

    service.events().delete(
        calendarId=calendar_id,
        eventId=event_id,
        sendUpdates='all' if (notify_attendees and has_attendees) else 'none'
    ).execute()

    return {
        'event_id': event_id,
        'summary': event_summary,
        'status': 'deleted',
        'attendees_notified': notify_attendees and has_attendees
    }

# =============================================================================
# ATTENDEE OPERATIONS
# =============================================================================

def add_attendees(event_id, attendees, calendar_id='primary'):
    """
    Add attendees to an existing event.

    Args:
        event_id: Event ID
        attendees: List of email addresses to add
        calendar_id: Calendar ID

    Returns:
        Updated event with new attendees
    """
    service = get_service()

    # Get existing event
    event = service.events().get(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()

    # Add new attendees
    existing_attendees = event.get('attendees', [])
    existing_emails = {a['email'] for a in existing_attendees}

    for email in attendees:
        if email not in existing_emails:
            existing_attendees.append({'email': email})

    event['attendees'] = existing_attendees

    result = service.events().update(
        calendarId=calendar_id,
        eventId=event_id,
        body=event,
        sendUpdates='all'
    ).execute()

    return {
        'id': result['id'],
        'summary': result.get('summary', ''),
        'attendees': result.get('attendees', []),
        'status': 'attendees_added',
        'added': attendees
    }

def remove_attendees(event_id, emails, calendar_id='primary'):
    """
    Remove attendees from an event.

    Args:
        event_id: Event ID
        emails: List of email addresses to remove
        calendar_id: Calendar ID

    Returns:
        Updated event
    """
    service = get_service()

    # Get existing event
    event = service.events().get(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()

    # Remove specified attendees
    emails_to_remove = set(emails)
    event['attendees'] = [
        a for a in event.get('attendees', [])
        if a['email'] not in emails_to_remove
    ]

    result = service.events().update(
        calendarId=calendar_id,
        eventId=event_id,
        body=event,
        sendUpdates='all'
    ).execute()

    return {
        'id': result['id'],
        'summary': result.get('summary', ''),
        'attendees': result.get('attendees', []),
        'status': 'attendees_removed',
        'removed': emails
    }

# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    # Fix Windows encoding for emoji output
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="Google Calendar Operations")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List events
    list_parser = subparsers.add_parser("list", help="List upcoming events")
    list_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    list_parser.add_argument("--max", type=int, default=10, help="Max results")
    list_parser.add_argument("--from", dest="time_min", help="Start date/time")
    list_parser.add_argument("--to", dest="time_max", help="End date/time")
    list_parser.add_argument("--query", "-q", help="Search query")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Get event
    get_parser = subparsers.add_parser("get", help="Get event details")
    get_parser.add_argument("event_id", help="Event ID")
    get_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    get_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # List calendars
    cals_parser = subparsers.add_parser("calendars", help="List calendars")
    cals_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Search events
    search_parser = subparsers.add_parser("search", help="Search events")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    search_parser.add_argument("--max", type=int, default=10, help="Max results")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Free/busy
    freebusy_parser = subparsers.add_parser("freebusy", help="Check availability")
    freebusy_parser.add_argument("--from", dest="time_min", required=True, help="Start date/time")
    freebusy_parser.add_argument("--to", dest="time_max", required=True, help="End date/time")
    freebusy_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID(s), comma-separated")
    freebusy_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Find slots
    slots_parser = subparsers.add_parser("find-slots", help="Find available meeting slots")
    slots_parser.add_argument("--duration", type=int, required=True, help="Meeting duration in minutes")
    slots_parser.add_argument("--from", dest="time_min", required=True, help="Start date/time")
    slots_parser.add_argument("--to", dest="time_max", required=True, help="End date/time")
    slots_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    slots_parser.add_argument("--hours", default="9-17", help="Working hours (e.g., 9-17)")
    slots_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Create event
    create_parser = subparsers.add_parser("create", help="Create event")
    create_parser.add_argument("--summary", "-s", required=True, help="Event title")
    create_parser.add_argument("--start", required=True, help="Start date/time")
    create_parser.add_argument("--end", required=True, help="End date/time")
    create_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    create_parser.add_argument("--description", "-d", help="Description")
    create_parser.add_argument("--location", "-l", help="Location")
    create_parser.add_argument("--attendees", "-a", help="Attendees (comma-separated emails)")
    create_parser.add_argument("--reminder-popup", type=int, help="Popup reminder (minutes before)")
    create_parser.add_argument("--reminder-email", type=int, help="Email reminder (minutes before)")
    create_parser.add_argument("--recurrence", help="Recurrence rule (e.g., RRULE:FREQ=WEEKLY)")
    create_parser.add_argument("--all-day", action="store_true", help="Create all-day event")
    create_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    create_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Quick add
    quick_parser = subparsers.add_parser("quick-add", help="Create event from natural language")
    quick_parser.add_argument("text", help="Event description (e.g., 'Meeting with John tomorrow at 3pm')")
    quick_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    quick_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    quick_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Update event
    update_parser = subparsers.add_parser("update", help="Update event")
    update_parser.add_argument("event_id", help="Event ID")
    update_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    update_parser.add_argument("--summary", "-s", help="New title")
    update_parser.add_argument("--start", help="New start date/time")
    update_parser.add_argument("--end", help="New end date/time")
    update_parser.add_argument("--description", "-d", help="New description")
    update_parser.add_argument("--location", "-l", help="New location")
    update_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    update_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Delete event
    delete_parser = subparsers.add_parser("delete", help="Delete event")
    delete_parser.add_argument("event_id", help="Event ID")
    delete_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    delete_parser.add_argument("--no-notify", action="store_true", help="Don't notify attendees")
    delete_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")

    # Add attendees
    add_att_parser = subparsers.add_parser("add-attendees", help="Add attendees to event")
    add_att_parser.add_argument("event_id", help="Event ID")
    add_att_parser.add_argument("--attendees", "-a", required=True, help="Emails (comma-separated)")
    add_att_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    add_att_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")

    # Remove attendees
    rm_att_parser = subparsers.add_parser("remove-attendees", help="Remove attendees from event")
    rm_att_parser.add_argument("event_id", help="Event ID")
    rm_att_parser.add_argument("--attendees", "-a", required=True, help="Emails (comma-separated)")
    rm_att_parser.add_argument("--calendar", "-c", default="primary", help="Calendar ID")
    rm_att_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if not check_dependencies():
        print("[ERROR] Missing dependencies. Run:")
        print("  pip install google-auth google-auth-oauthlib google-api-python-client")
        sys.exit(1)

    try:
        if args.command == "list":
            result = list_events(
                calendar_id=args.calendar,
                time_min=args.time_min,
                time_max=args.time_max,
                max_results=args.max,
                query=args.query
            )
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                if not result:
                    print("No upcoming events found.")
                else:
                    for event in result:
                        print(f"• {event['summary']}")
                        print(f"  Time: {format_event_time(event)}")
                        if event['location']:
                            print(f"  Location: {event['location']}")
                        if event['attendees']:
                            att_emails = [a.get('email', '') for a in event['attendees'][:3]]
                            more = f" (+{len(event['attendees'])-3} more)" if len(event['attendees']) > 3 else ""
                            print(f"  Attendees: {', '.join(att_emails)}{more}")
                        print(f"  ID: {event['id']}")
                        print()

        elif args.command == "get":
            result = get_event(args.event_id, args.calendar)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Title: {result['summary']}")
                print(f"Time: {format_event_time(result)}")
                if result['location']:
                    print(f"Location: {result['location']}")
                if result['description']:
                    print(f"Description: {result['description']}")
                if result['attendees']:
                    print("Attendees:")
                    for att in result['attendees']:
                        status = att.get('responseStatus', 'unknown')
                        print(f"  • {att['email']} ({status})")
                if result['recurrence']:
                    print(f"Recurrence: {result['recurrence']}")
                print(f"Link: {result['htmlLink']}")
                print(f"ID: {result['id']}")

        elif args.command == "calendars":
            result = list_calendars()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for cal in result:
                    primary = " (primary)" if cal['primary'] else ""
                    print(f"• {cal['summary']}{primary}")
                    print(f"  ID: {cal['id']}")
                    print(f"  Access: {cal['accessRole']}")
                    print()

        elif args.command == "search":
            result = search_events(args.query, args.calendar, args.max)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                if not result:
                    print(f"No events found matching '{args.query}'")
                else:
                    for event in result:
                        print(f"• {event['summary']}")
                        print(f"  Time: {format_event_time(event)}")
                        print(f"  ID: {event['id']}")
                        print()

        elif args.command == "freebusy":
            calendars = args.calendar.split(',')
            result = get_freebusy(args.time_min, args.time_max, calendars)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for cal_id, data in result.items():
                    status = "Free" if data['is_free'] else "Busy"
                    print(f"• {cal_id}: {status}")
                    if data['busy']:
                        for period in data['busy']:
                            print(f"  Busy: {period['start']} - {period['end']}")

        elif args.command == "find-slots":
            working_hours = tuple(map(int, args.hours.split('-')))
            result = find_slots(
                duration_minutes=args.duration,
                time_min=args.time_min,
                time_max=args.time_max,
                calendar_id=args.calendar,
                working_hours=working_hours
            )
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                if not result:
                    print("No available slots found in the specified range.")
                else:
                    print(f"Found {len(result)} available {args.duration}-minute slots:")
                    for slot in result[:10]:  # Show first 10
                        start = datetime.fromisoformat(slot['start'].replace('Z', '+00:00'))
                        print(f"  • {start.strftime('%Y-%m-%d %H:%M')} - {slot['end'].split('T')[1][:5]}")
                    if len(result) > 10:
                        print(f"  ... and {len(result) - 10} more slots")

        elif args.command == "create":
            # Build reminders dict
            reminders = {}
            if args.reminder_popup:
                reminders['popup'] = args.reminder_popup
            if args.reminder_email:
                reminders['email'] = args.reminder_email

            # Parse attendees
            attendees = args.attendees.split(',') if args.attendees else None

            # Show preview
            print("\n" + "=" * 50)
            print("📅 EVENT PREVIEW")
            print("=" * 50)
            print(f"Title: {args.summary}")
            print(f"Start: {args.start}")
            print(f"End: {args.end}")
            if args.location:
                print(f"Location: {args.location}")
            if args.description:
                print(f"Description: {args.description}")
            if attendees:
                print(f"Attendees: {', '.join(attendees)}")
                print("⚠️  Attendees will receive a calendar invite!")
            if reminders:
                print(f"Reminders: {reminders}")
            if args.recurrence:
                print(f"Recurrence: {args.recurrence}")
            if args.all_day:
                print("Type: All-day event")
            print("=" * 50)

            # Confirm
            if not args.yes:
                confirm = input("\n⚠️  Create this event? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("❌ Event creation cancelled.")
                    sys.exit(0)

            result = create_event(
                summary=args.summary,
                start=args.start,
                end=args.end,
                calendar_id=args.calendar,
                description=args.description,
                location=args.location,
                attendees=attendees,
                reminders=reminders if reminders else None,
                recurrence=args.recurrence,
                all_day=args.all_day
            )

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Event created!")
                print(f"Title: {result['summary']}")
                print(f"Link: {result['htmlLink']}")
                print(f"ID: {result['id']}")
                if result.get('attendees_notified'):
                    print("📧 Invites sent to attendees")

        elif args.command == "quick-add":
            # Show preview
            print("\n" + "=" * 50)
            print("📅 QUICK ADD EVENT")
            print("=" * 50)
            print(f"Input: {args.text}")
            print("(Google will parse this automatically)")
            print("=" * 50)

            if not args.yes:
                confirm = input("\n⚠️  Create this event? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("❌ Event creation cancelled.")
                    sys.exit(0)

            result = quick_add(args.text, args.calendar)

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Event created!")
                print(f"Title: {result['summary']}")
                print(f"Time: {format_event_time(result)}")
                print(f"Link: {result['htmlLink']}")
                print(f"ID: {result['id']}")

        elif args.command == "update":
            # Get current event
            current = get_event(args.event_id, args.calendar)

            # Show what will change
            print("\n" + "=" * 50)
            print("📅 UPDATE EVENT")
            print("=" * 50)
            print(f"Current: {current['summary']}")
            print(f"Time: {format_event_time(current)}")
            print("-" * 50)
            print("Changes:")
            if args.summary:
                print(f"  Title: {current['summary']} → {args.summary}")
            if args.start:
                print(f"  Start: → {args.start}")
            if args.end:
                print(f"  End: → {args.end}")
            if args.description:
                print(f"  Description: → {args.description}")
            if args.location:
                print(f"  Location: → {args.location}")
            if current.get('attendees'):
                print("⚠️  Attendees will be notified of changes!")
            print("=" * 50)

            if not args.yes:
                confirm = input("\n⚠️  Apply these changes? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("❌ Update cancelled.")
                    sys.exit(0)

            result = update_event(
                event_id=args.event_id,
                calendar_id=args.calendar,
                summary=args.summary,
                start=args.start,
                end=args.end,
                description=args.description,
                location=args.location
            )

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n✅ Event updated!")
                print(f"Title: {result['summary']}")
                print(f"Link: {result['htmlLink']}")
                if result.get('attendees_notified'):
                    print("📧 Attendees notified of changes")

        elif args.command == "delete":
            # Get event info
            current = get_event(args.event_id, args.calendar)

            print("\n" + "=" * 50)
            print("🗑️  DELETE EVENT")
            print("=" * 50)
            print(f"Title: {current['summary']}")
            print(f"Time: {format_event_time(current)}")
            if current.get('attendees'):
                print(f"Attendees: {len(current['attendees'])} people")
                if not args.no_notify:
                    print("⚠️  Attendees will be notified of cancellation!")
            print("=" * 50)

            if not args.yes:
                confirm = input("\n⚠️  Delete this event? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("❌ Deletion cancelled.")
                    sys.exit(0)

            result = delete_event(
                args.event_id,
                args.calendar,
                notify_attendees=not args.no_notify
            )

            print(f"\n✅ Event deleted: {result['summary']}")
            if result.get('attendees_notified'):
                print("📧 Attendees notified of cancellation")

        elif args.command == "add-attendees":
            attendees = args.attendees.split(',')
            current = get_event(args.event_id, args.calendar)

            print("\n" + "=" * 50)
            print("👥 ADD ATTENDEES")
            print("=" * 50)
            print(f"Event: {current['summary']}")
            print(f"Adding: {', '.join(attendees)}")
            print("⚠️  New attendees will receive calendar invites!")
            print("=" * 50)

            if not args.yes:
                confirm = input("\n⚠️  Add these attendees? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("❌ Cancelled.")
                    sys.exit(0)

            result = add_attendees(args.event_id, attendees, args.calendar)
            print(f"\n✅ Added {len(attendees)} attendee(s)")
            print("📧 Invites sent")

        elif args.command == "remove-attendees":
            attendees = args.attendees.split(',')
            current = get_event(args.event_id, args.calendar)

            print("\n" + "=" * 50)
            print("👥 REMOVE ATTENDEES")
            print("=" * 50)
            print(f"Event: {current['summary']}")
            print(f"Removing: {', '.join(attendees)}")
            print("=" * 50)

            if not args.yes:
                confirm = input("\n⚠️  Remove these attendees? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("❌ Cancelled.")
                    sys.exit(0)

            result = remove_attendees(args.event_id, attendees, args.calendar)
            print(f"\n✅ Removed {len(attendees)} attendee(s)")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
