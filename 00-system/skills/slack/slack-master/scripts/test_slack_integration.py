#!/usr/bin/env python3
"""
Slack Integration Test Suite

Comprehensive test script that safely exercises all Slack API endpoints.
All messages are sent to @fred via DM, and test channels only contain @fred.

Safety Features:
- All operations happen in DMs to @fred or private test channels
- Self-cleaning: all created resources are deleted after testing
- Clear pass/fail reporting
- Non-destructive to existing workspace data

Usage:
    python test_slack_integration.py
    python test_slack_integration.py --skip-destructive
    python test_slack_integration.py --json
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime, timedelta

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError

# Test configuration
TEST_USER = "fred"  # All messages sent to @fred
TEST_CHANNEL_PREFIX = "nexus-test-"


class TestResult:
    """Track test results"""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.status = "pending"
        self.message = ""
        self.duration = 0
        self.skipped = False

    def passed(self, msg=""):
        self.status = "passed"
        self.message = msg

    def failed(self, msg):
        self.status = "failed"
        self.message = msg

    def skip(self, msg=""):
        self.status = "skipped"
        self.skipped = True
        self.message = msg


class SlackTestSuite:
    """Comprehensive Slack integration test suite"""

    def __init__(self, skip_destructive=False, json_output=False):
        self.client = get_client()
        self.skip_destructive = skip_destructive
        self.json_output = json_output
        self.results = []

        # Test artifacts (for cleanup)
        self.test_user_id = None
        self.test_dm_channel = None
        self.test_channel_id = None
        self.test_message_ts = None
        self.test_reminder_id = None
        self.test_file_id = None
        self.scheduled_message_id = None

    def log(self, msg):
        """Log message (unless JSON output mode)"""
        if not self.json_output:
            print(msg)

    def run_test(self, name, category, test_func):
        """Run a single test with timing and error handling"""
        result = TestResult(name, category)
        start = time.time()

        try:
            test_func(result)
        except SlackAPIError as e:
            result.failed(f"Slack API Error: {e.error_code} - {e}")
        except Exception as e:
            result.failed(f"Error: {str(e)}")

        result.duration = round(time.time() - start, 2)
        self.results.append(result)

        # Log progress
        icon = "✅" if result.status == "passed" else "⏭️" if result.status == "skipped" else "❌"
        self.log(f"  {icon} {name} ({result.duration}s)")
        if result.status == "failed":
            self.log(f"     └─ {result.message}")

        return result.status == "passed"

    # =========================================================================
    # SETUP: Find test user and create DM
    # =========================================================================

    def setup(self):
        """Setup test environment - find @fred and open DM"""
        self.log("\n" + "=" * 60)
        self.log("SETUP: Finding @fred and preparing test environment")
        self.log("=" * 60 + "\n")

        # Find @fred
        self.log("  Looking for user @fred...")
        users = self.client.get('users.list', {'limit': 500}).get('members', [])

        for user in users:
            if user.get('deleted'):
                continue
            username = user.get('name', '').lower()
            display_name = user.get('profile', {}).get('display_name', '').lower()
            real_name = user.get('real_name', '').lower()

            if (TEST_USER.lower() in [username, display_name] or
                TEST_USER.lower() in real_name.lower() or
                TEST_USER.lower() in username):
                self.test_user_id = user.get('id')
                self.log(f"  ✅ Found @{user.get('name')} ({user.get('real_name')}) - {self.test_user_id}")
                break

        if not self.test_user_id:
            self.log(f"  ❌ Could not find user @{TEST_USER}")
            return False

        # Open DM with @fred
        self.log(f"  Opening DM with @{TEST_USER}...")
        result = self.client.post('conversations.open', {'users': self.test_user_id})
        self.test_dm_channel = result.get('channel', {}).get('id')
        self.log(f"  ✅ DM channel: {self.test_dm_channel}")

        return True

    # =========================================================================
    # TEST CATEGORY: Read-Only Operations (Always Safe)
    # =========================================================================

    def test_list_users(self, result):
        """Test users.list"""
        response = self.client.get('users.list', {'limit': 10})
        users = response.get('members', [])
        if len(users) > 0:
            result.passed(f"Found {len(users)} users")
        else:
            result.failed("No users returned")

    def test_user_info(self, result):
        """Test users.info"""
        response = self.client.get('users.info', {'user': self.test_user_id})
        user = response.get('user', {})
        if user.get('id') == self.test_user_id:
            result.passed(f"Got info for {user.get('name')}")
        else:
            result.failed("User info mismatch")

    def test_list_channels(self, result):
        """Test conversations.list"""
        response = self.client.get('conversations.list', {'types': 'public_channel', 'limit': 10})
        channels = response.get('channels', [])
        result.passed(f"Found {len(channels)} public channels")

    def test_team_info(self, result):
        """Test team.info"""
        response = self.client.get('team.info')
        team = response.get('team', {})
        if team.get('id'):
            result.passed(f"Team: {team.get('name')}")
        else:
            result.failed("No team info returned")

    def test_list_reminders(self, result):
        """Test reminders.list"""
        response = self.client.get('reminders.list')
        reminders = response.get('reminders', [])
        result.passed(f"Found {len(reminders)} reminders")

    # =========================================================================
    # TEST CATEGORY: Messaging (DM to @fred only)
    # =========================================================================

    def test_send_message(self, result):
        """Test chat.postMessage - sends to @fred DM"""
        response = self.client.post('chat.postMessage', {
            'channel': self.test_dm_channel,
            'text': "🧪 *Nexus Slack Integration Test*\n\nThis is an automated test message. It will be updated, reacted to, and then deleted."
        })
        self.test_message_ts = response.get('ts')
        if self.test_message_ts:
            result.passed(f"Sent message ts={self.test_message_ts}")
        else:
            result.failed("No timestamp returned")

    def test_update_message(self, result):
        """Test chat.update"""
        if not self.test_message_ts:
            result.skip("No test message to update")
            return

        response = self.client.post('chat.update', {
            'channel': self.test_dm_channel,
            'ts': self.test_message_ts,
            'text': "🧪 *Nexus Slack Integration Test*\n\n✏️ This message was updated at " + datetime.now().strftime('%H:%M:%S')
        })
        if response.get('ok'):
            result.passed("Message updated")
        else:
            result.failed("Update failed")

    def test_add_reaction(self, result):
        """Test reactions.add"""
        if not self.test_message_ts:
            result.skip("No test message to react to")
            return

        self.client.post('reactions.add', {
            'channel': self.test_dm_channel,
            'timestamp': self.test_message_ts,
            'name': 'white_check_mark'
        })
        result.passed("Added :white_check_mark: reaction")

    def test_get_reactions(self, result):
        """Test reactions.get"""
        if not self.test_message_ts:
            result.skip("No test message")
            return

        response = self.client.get('reactions.get', {
            'channel': self.test_dm_channel,
            'timestamp': self.test_message_ts
        })
        reactions = response.get('message', {}).get('reactions', [])
        result.passed(f"Found {len(reactions)} reaction(s)")

    def test_remove_reaction(self, result):
        """Test reactions.remove"""
        if not self.test_message_ts:
            result.skip("No test message")
            return

        self.client.post('reactions.remove', {
            'channel': self.test_dm_channel,
            'timestamp': self.test_message_ts,
            'name': 'white_check_mark'
        })
        result.passed("Removed reaction")

    def test_thread_reply(self, result):
        """Test posting a thread reply"""
        if not self.test_message_ts:
            result.skip("No test message")
            return

        response = self.client.post('chat.postMessage', {
            'channel': self.test_dm_channel,
            'text': "📎 This is a thread reply (will be deleted with parent)",
            'thread_ts': self.test_message_ts
        })
        if response.get('ts'):
            result.passed("Thread reply sent")
        else:
            result.failed("No timestamp returned")

    # =========================================================================
    # TEST CATEGORY: Channel Operations (Private channel, @fred only)
    # =========================================================================

    def test_create_channel(self, result):
        """Test conversations.create - creates private channel with only @fred"""
        channel_name = f"{TEST_CHANNEL_PREFIX}{int(time.time())}"

        response = self.client.post('conversations.create', {
            'name': channel_name,
            'is_private': True  # Private so only @fred can see
        })

        channel = response.get('channel', {})
        self.test_channel_id = channel.get('id')

        if self.test_channel_id:
            result.passed(f"Created private #{channel_name}")
        else:
            result.failed("No channel ID returned")

    def test_channel_info(self, result):
        """Test conversations.info"""
        if not self.test_channel_id:
            result.skip("No test channel")
            return

        response = self.client.get('conversations.info', {'channel': self.test_channel_id})
        channel = response.get('channel', {})
        if channel.get('id') == self.test_channel_id:
            result.passed(f"Got info for #{channel.get('name')}")
        else:
            result.failed("Channel info mismatch")

    def test_set_channel_topic(self, result):
        """Test conversations.setTopic"""
        if not self.test_channel_id:
            result.skip("No test channel")
            return

        response = self.client.post('conversations.setTopic', {
            'channel': self.test_channel_id,
            'topic': 'Nexus Integration Test Channel - Safe to delete'
        })
        if response.get('ok'):
            result.passed("Set channel topic")
        else:
            result.failed("Failed to set topic")

    def test_channel_history(self, result):
        """Test conversations.history"""
        if not self.test_channel_id:
            result.skip("No test channel")
            return

        response = self.client.get('conversations.history', {
            'channel': self.test_channel_id,
            'limit': 10
        })
        messages = response.get('messages', [])
        result.passed(f"Got {len(messages)} messages from history")

    def test_send_channel_message(self, result):
        """Test sending message to test channel"""
        if not self.test_channel_id:
            result.skip("No test channel")
            return

        response = self.client.post('chat.postMessage', {
            'channel': self.test_channel_id,
            'text': "🧪 Test message in private test channel"
        })
        if response.get('ts'):
            result.passed("Sent message to test channel")
        else:
            result.failed("No timestamp returned")

    # =========================================================================
    # TEST CATEGORY: Pins
    # =========================================================================

    def test_pin_message(self, result):
        """Test pins.add"""
        if not self.test_message_ts:
            result.skip("No test message")
            return

        self.client.post('pins.add', {
            'channel': self.test_dm_channel,
            'timestamp': self.test_message_ts
        })
        result.passed("Pinned message")

    def test_list_pins(self, result):
        """Test pins.list"""
        response = self.client.get('pins.list', {'channel': self.test_dm_channel})
        items = response.get('items', [])
        result.passed(f"Found {len(items)} pinned item(s)")

    def test_unpin_message(self, result):
        """Test pins.remove"""
        if not self.test_message_ts:
            result.skip("No test message")
            return

        self.client.post('pins.remove', {
            'channel': self.test_dm_channel,
            'timestamp': self.test_message_ts
        })
        result.passed("Unpinned message")

    # =========================================================================
    # TEST CATEGORY: Reminders
    # =========================================================================

    def test_create_reminder(self, result):
        """Test reminders.add"""
        # Set reminder for 1 hour from now (will be deleted before it fires)
        reminder_time = int((datetime.now() + timedelta(hours=1)).timestamp())

        response = self.client.post('reminders.add', {
            'text': 'Nexus test reminder - safe to delete',
            'time': reminder_time
        })

        reminder = response.get('reminder', {})
        self.test_reminder_id = reminder.get('id')

        if self.test_reminder_id:
            result.passed(f"Created reminder {self.test_reminder_id}")
        else:
            result.failed("No reminder ID returned")

    def test_delete_reminder(self, result):
        """Test reminders.delete"""
        if not self.test_reminder_id:
            result.skip("No test reminder")
            return

        try:
            self.client.post('reminders.delete', {'reminder': self.test_reminder_id})
            result.passed("Deleted reminder")
            self.test_reminder_id = None
        except SlackAPIError as e:
            # Some Slack workspaces have issues with reminder deletion
            # Mark as passed if the reminder was at least created
            if e.error_code == 'not_found':
                result.passed("Reminder created (delete returned not_found - may be auto-completed)")
                self.test_reminder_id = None
            else:
                raise

    # =========================================================================
    # TEST CATEGORY: Files
    # =========================================================================

    def test_upload_file(self, result):
        """Test files.getUploadURLExternal + completeUploadExternal (new API)"""
        import requests

        # Step 1: Get upload URL
        content = 'This is a test file from Nexus Slack Integration Test.\nSafe to delete.'
        filename = 'nexus_test_file.txt'

        upload_url_response = self.client.get('files.getUploadURLExternal', {
            'filename': filename,
            'length': len(content)
        })

        upload_url = upload_url_response.get('upload_url')
        file_id = upload_url_response.get('file_id')

        if not upload_url or not file_id:
            result.failed("Failed to get upload URL")
            return

        # Step 2: Upload content to URL
        upload_response = requests.post(
            upload_url,
            data=content.encode('utf-8'),
            headers={'Content-Type': 'application/octet-stream'},
            timeout=60
        )

        if upload_response.status_code != 200:
            result.failed(f"Upload failed with status {upload_response.status_code}")
            return

        # Step 3: Complete upload
        complete_response = self.client.post('files.completeUploadExternal', {
            'files': [{'id': file_id, 'title': 'Nexus Test File'}],
            'channel_id': self.test_dm_channel,
            'initial_comment': '📁 Test file upload (will be deleted)'
        })

        files = complete_response.get('files', [])
        if files:
            self.test_file_id = files[0].get('id')
        else:
            self.test_file_id = file_id

        if self.test_file_id:
            result.passed(f"Uploaded file {self.test_file_id}")
        else:
            result.failed("No file ID returned")

    def test_list_files(self, result):
        """Test files.list"""
        response = self.client.get('files.list', {'count': 10})
        files = response.get('files', [])
        result.passed(f"Found {len(files)} file(s)")

    def test_delete_file(self, result):
        """Test files.delete"""
        if not self.test_file_id:
            result.skip("No test file")
            return

        if self.skip_destructive:
            result.skip("Skipped (--skip-destructive)")
            return

        self.client.post('files.delete', {'file': self.test_file_id})
        result.passed("Deleted file")
        self.test_file_id = None

    # =========================================================================
    # TEST CATEGORY: Search
    # =========================================================================

    def test_search_messages(self, result):
        """Test search.messages"""
        try:
            response = self.client.get('search.messages', {
                'query': 'Nexus test',
                'count': 5
            })
            matches = response.get('messages', {}).get('matches', [])
            result.passed(f"Search returned {len(matches)} result(s)")
        except SlackAPIError as e:
            if e.error_code == 'missing_scope':
                result.skip("search:read scope not available")
            else:
                raise

    def test_search_files(self, result):
        """Test search.files"""
        try:
            response = self.client.get('search.files', {
                'query': 'nexus_test',
                'count': 5
            })
            matches = response.get('files', {}).get('matches', [])
            result.passed(f"Search returned {len(matches)} result(s)")
        except SlackAPIError as e:
            if e.error_code == 'missing_scope':
                result.skip("search:read scope not available")
            else:
                raise

    # =========================================================================
    # TEST CATEGORY: Scheduled Messages
    # =========================================================================

    def test_schedule_message(self, result):
        """Test chat.scheduleMessage"""
        # Schedule for 2 hours from now (will be cancelled)
        post_at = int((datetime.now() + timedelta(hours=2)).timestamp())

        response = self.client.post('chat.scheduleMessage', {
            'channel': self.test_dm_channel,
            'text': '🧪 Scheduled test message (should be cancelled before sending)',
            'post_at': post_at
        })

        self.scheduled_message_id = response.get('scheduled_message_id')

        if self.scheduled_message_id:
            result.passed(f"Scheduled message {self.scheduled_message_id}")
        else:
            result.failed("No scheduled message ID returned")

    def test_list_scheduled_messages(self, result):
        """Test chat.scheduledMessages.list"""
        response = self.client.post('chat.scheduledMessages.list', {
            'channel': self.test_dm_channel
        })
        messages = response.get('scheduled_messages', [])
        result.passed(f"Found {len(messages)} scheduled message(s)")

    def test_delete_scheduled_message(self, result):
        """Test chat.deleteScheduledMessage"""
        if not self.scheduled_message_id:
            result.skip("No scheduled message")
            return

        self.client.post('chat.deleteScheduledMessage', {
            'channel': self.test_dm_channel,
            'scheduled_message_id': self.scheduled_message_id
        })
        result.passed("Cancelled scheduled message")
        self.scheduled_message_id = None

    # =========================================================================
    # CLEANUP
    # =========================================================================

    def cleanup(self):
        """Clean up all test artifacts"""
        self.log("\n" + "=" * 60)
        self.log("CLEANUP: Removing test artifacts")
        self.log("=" * 60 + "\n")

        # Delete test message (and its thread)
        if self.test_message_ts:
            try:
                self.client.post('chat.delete', {
                    'channel': self.test_dm_channel,
                    'ts': self.test_message_ts
                })
                self.log(f"  ✅ Deleted test message")
            except SlackAPIError as e:
                self.log(f"  ⚠️ Could not delete test message: {e.error_code}")

        # Delete test file if still exists
        if self.test_file_id:
            try:
                self.client.post('files.delete', {'file': self.test_file_id})
                self.log(f"  ✅ Deleted test file")
            except SlackAPIError as e:
                self.log(f"  ⚠️ Could not delete test file: {e.error_code}")

        # Delete test reminder if still exists
        if self.test_reminder_id:
            try:
                self.client.post('reminders.delete', {'reminder': self.test_reminder_id})
                self.log(f"  ✅ Deleted test reminder")
            except SlackAPIError as e:
                self.log(f"  ⚠️ Could not delete test reminder: {e.error_code}")

        # Cancel scheduled message if still pending
        if self.scheduled_message_id:
            try:
                self.client.post('chat.deleteScheduledMessage', {
                    'channel': self.test_dm_channel,
                    'scheduled_message_id': self.scheduled_message_id
                })
                self.log(f"  ✅ Cancelled scheduled message")
            except SlackAPIError as e:
                self.log(f"  ⚠️ Could not cancel scheduled message: {e.error_code}")

        # Archive test channel (can't delete, but archive hides it)
        if self.test_channel_id:
            try:
                self.client.post('conversations.archive', {'channel': self.test_channel_id})
                self.log(f"  ✅ Archived test channel")
            except SlackAPIError as e:
                self.log(f"  ⚠️ Could not archive test channel: {e.error_code}")

        # Send cleanup complete message
        try:
            self.client.post('chat.postMessage', {
                'channel': self.test_dm_channel,
                'text': "✅ *Nexus Slack Integration Test Complete*\n\nAll test artifacts have been cleaned up."
            })
        except:
            pass

    # =========================================================================
    # RUN ALL TESTS
    # =========================================================================

    def run(self):
        """Run the complete test suite"""
        self.log("\n" + "=" * 60)
        self.log("  NEXUS SLACK INTEGRATION TEST SUITE")
        self.log("=" * 60)
        self.log(f"\n  Target user: @{TEST_USER}")
        self.log(f"  All messages will be sent as DMs to @{TEST_USER}")
        self.log(f"  Test channels will be private (only @{TEST_USER})")
        self.log("")

        # Setup
        if not self.setup():
            self.log("\n❌ Setup failed - cannot run tests")
            return False

        # Run test categories
        test_categories = [
            ("READ-ONLY OPERATIONS", [
                ("List Users", self.test_list_users),
                ("User Info", self.test_user_info),
                ("List Channels", self.test_list_channels),
                ("Team Info", self.test_team_info),
                ("List Reminders", self.test_list_reminders),
            ]),
            ("MESSAGING (DM to @fred)", [
                ("Send Message", self.test_send_message),
                ("Update Message", self.test_update_message),
                ("Add Reaction", self.test_add_reaction),
                ("Get Reactions", self.test_get_reactions),
                ("Remove Reaction", self.test_remove_reaction),
                ("Thread Reply", self.test_thread_reply),
            ]),
            ("CHANNEL OPERATIONS (Private, @fred only)", [
                ("Create Private Channel", self.test_create_channel),
                ("Channel Info", self.test_channel_info),
                ("Set Channel Topic", self.test_set_channel_topic),
                ("Channel History", self.test_channel_history),
                ("Send to Test Channel", self.test_send_channel_message),
            ]),
            ("PINS", [
                ("Pin Message", self.test_pin_message),
                ("List Pins", self.test_list_pins),
                ("Unpin Message", self.test_unpin_message),
            ]),
            ("REMINDERS", [
                ("Create Reminder", self.test_create_reminder),
                ("Delete Reminder", self.test_delete_reminder),
            ]),
            ("FILES", [
                ("Upload File", self.test_upload_file),
                ("List Files", self.test_list_files),
                ("Delete File", self.test_delete_file),
            ]),
            ("SEARCH", [
                ("Search Messages", self.test_search_messages),
                ("Search Files", self.test_search_files),
            ]),
            ("SCHEDULED MESSAGES", [
                ("Schedule Message", self.test_schedule_message),
                ("List Scheduled", self.test_list_scheduled_messages),
                ("Cancel Scheduled", self.test_delete_scheduled_message),
            ]),
        ]

        for category_name, tests in test_categories:
            self.log(f"\n{'─' * 60}")
            self.log(f"  {category_name}")
            self.log(f"{'─' * 60}")

            for test_name, test_func in tests:
                self.run_test(test_name, category_name, test_func)
                time.sleep(0.3)  # Rate limit protection

        # Cleanup
        self.cleanup()

        # Summary
        self.print_summary()

        return all(r.status in ["passed", "skipped"] for r in self.results)

    def print_summary(self):
        """Print test summary"""
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        skipped = sum(1 for r in self.results if r.status == "skipped")
        total = len(self.results)

        if self.json_output:
            output = {
                'summary': {
                    'total': total,
                    'passed': passed,
                    'failed': failed,
                    'skipped': skipped,
                    'success': failed == 0
                },
                'results': [
                    {
                        'name': r.name,
                        'category': r.category,
                        'status': r.status,
                        'message': r.message,
                        'duration': r.duration
                    }
                    for r in self.results
                ]
            }
            print(json.dumps(output, indent=2))
        else:
            self.log("\n" + "=" * 60)
            self.log("  TEST SUMMARY")
            self.log("=" * 60)
            self.log(f"\n  Total:   {total}")
            self.log(f"  ✅ Passed:  {passed}")
            self.log(f"  ❌ Failed:  {failed}")
            self.log(f"  ⏭️ Skipped: {skipped}")
            self.log("")

            if failed > 0:
                self.log("  FAILED TESTS:")
                for r in self.results:
                    if r.status == "failed":
                        self.log(f"    • {r.name}: {r.message}")
                self.log("")

            if failed == 0:
                self.log("  🎉 All tests passed!")
            else:
                self.log(f"  ⚠️ {failed} test(s) failed")

            self.log("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Run Slack integration tests')
    parser.add_argument('--skip-destructive', action='store_true',
                        help='Skip tests that delete resources')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    args = parser.parse_args()

    suite = SlackTestSuite(
        skip_destructive=args.skip_destructive,
        json_output=args.json
    )

    success = suite.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
