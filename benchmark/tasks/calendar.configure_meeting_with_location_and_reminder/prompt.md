Go to the **Calendar** app and create a new calendar event with the details below.

1. **Title**: `Quarterly Review`
2. **Date**: June 10, 2026
3. **Start time**: 2:00 PM (14:00)
4. **End time**: 4:00 PM (16:00)
5. **Location**: `Conference Room B, Floor 3`
6. **Attendees**: add the two seeded contacts **Alice Attendee** and **Bob Attendee**
   from the Attendees autocomplete (pick the existing internal users — do NOT
   create new ones).
7. **Reminder**: on the event form, open the **Options** tab and add a reminder
   to the **Reminders** field that fires **1 hour before** the event. You may
   pick the pre-existing `Notification - 1 Hours` entry from the autocomplete,
   or pick any other reminder whose duration equals 1 hour (60 minutes).

Save the event.

**Rules:**
- The event title must be exactly `Quarterly Review`.
- The event must be a **one-time** event (no recurrence) and **not all-day**,
  timed from 14:00 to 16:00 local time on 2026-06-10.
- Attendees must include exactly the two existing users Alice Attendee and
  Bob Attendee (do not create new contacts, do not add anyone else beyond the
  organizer who is added automatically).
- The reminder MUST be a `calendar.alarm` attached via the Options tab's
  Reminders many2many field, not text typed into the notes/description.
- Exactly one reminder whose duration equals 1 hour (60 minutes) must be
  linked to the event; do not add other reminders.
- Do NOT schedule any activities in the chatter.
- Do NOT modify any other existing events, contacts, or alarms.
