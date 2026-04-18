Go to the **Calendar** app and create a new calendar event with the details below.

1. **Title**: `Q2 Planning Session`
2. **Date**: May 20, 2026
3. **Start time**: 2:00 PM (14:00)
4. **End time**: 3:30 PM (15:30)
5. **Attendees**: add the two seeded contacts **Alice Bench** and **Bob Bench**
   from the Attendees autocomplete (pick the existing contacts — do NOT create
   new ones).
6. **Attach an agenda file** to this event's chatter. Upload the file located at
   `benchmark/tasks/calendar.invite_organize_with_event_agenda_attachment/seed_artifacts/agenda.txt`.
   Use the paperclip icon (**Attach files**) in the chatter panel on the right
   of the event form; the file picker will open a native dialog — select
   `agenda.txt`.

Save the event.

**Rules:**
- The event title must be exactly `Q2 Planning Session`.
- The event must be a **one-time** event (no recurrence), **not all-day**, and
  timed from 14:00 to 15:30 local time on 2026-05-20.
- Attendees must be exactly the two existing contacts Alice Bench and Bob
  Bench — do not create new contacts, do not add anyone else.
- The attachment must be named exactly `agenda.txt` and be linked to this
  calendar event (res_model `calendar.event`). Upload the file through the
  chatter paperclip; do NOT paste the text into the event's description/notes
  field.
- Do NOT set a Location.
- Do NOT schedule any activities.
- Do NOT modify any other existing events or contacts.
