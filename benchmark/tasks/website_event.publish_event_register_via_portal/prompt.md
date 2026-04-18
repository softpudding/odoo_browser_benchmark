You will complete a two-phase event workflow that round-trips between
the Odoo back-office and the public website.

A seeded but **unpublished** event named `Bench Public Day` already
exists. Your job is to (1) publish it from the back-office and (2)
register an attendee by submitting the public registration form on the
portal.

# Phase 1 — Back-office: publish the event

1. Open the **Events** app (URL `/odoo/events`).
2. If a default filter hides the seeded event (e.g. "Upcoming" is not
   applied), clear the filters or search for `Bench Public Day` to
   find it. Open the event form.
3. On the event form, click the **Unpublished** indicator at the
   top-right of the form (the "website_redirect_button" widget on the
   `is_published` field). This opens the website preview of the event.
4. In the website preview top systray, click the **Unpublished**
   switch to flip it to **Published**. The label updates to
   `Published` and the switch turns on.
   The result must be that the event is **Published** (`is_published`
   is `True`). Do not change anything else about the event.

# Phase 2 — Portal: register an attendee

5. Navigate to the public events list at `/event` (singular — the URL
   `/events` also redirects here). You should see the published
   `Bench Public Day` card.
6. Click the **Bench Public Day** card / title to reach the event page.
7. Click the **Register** button on the event page. A **Tickets**
   modal opens with the default `Registration` ticket counter set to
   `1`. Leave the counter at `1` and click the **Register** button at
   the bottom of the modal.
8. An **Attendees** modal appears with a form for one attendee. Fill:
   - **Name**: `Priya Patel`
   - **Email**: `priya.patel@example.com`
   - **Phone**: `+1 555 0142`
9. Click **Confirm Registration** to submit. You should land on a
   **Registration confirmed!** page.

# Rules

- Do not create any additional events.
- Do not create any additional `event.registration` records besides the
  one for Priya Patel.
- The attendee's name and email must match the values above exactly
  (case-sensitive).
- Do not unpublish the event after publishing it.
