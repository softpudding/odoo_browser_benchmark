Add a sponsor to an existing event and publish the event.

# Phase 1 — Open the event

1. Open the **Events** app (URL `/odoo/events`).
2. Clear any default filter (e.g. "Upcoming") or search for `Bench Conf 2026`
   if it isn't visible in the kanban / list.
3. Open the event **`Bench Conf 2026`**.

# Phase 2 — Add the sponsor

4. On the event form, click the **Sponsors** smart button in the stat-button
   row at the top of the form. This opens the list / kanban of sponsors for
   this event (empty for the seeded event).
5. Click **New** to open a blank sponsor form.
6. Fill the sponsor fields:
   - **Partner**: `Bench Sponsor Inc` (pick the existing partner with that
     exact name from the autocomplete dropdown — do NOT create a new one).
   - **Sponsorship Level**: `Silver` (pick the existing sponsor level from
     the autocomplete dropdown — do NOT create a new level).
7. Save the sponsor.
8. Go back to the **Bench Conf 2026** event form (use the breadcrumb).

# Phase 3 — Publish the event

9. On the event form, click the **Unpublished** indicator at the top-right
   of the form (the `website_redirect_button` widget on the `is_published`
   field). This opens the website preview of the event.
10. In the website preview top systray, click the **Unpublished** switch to
    flip it to **Published**. The label updates to `Published` and the
    switch turns on.

The final state must be: `event.event.is_published = True` on
`Bench Conf 2026`, with one `event.sponsor` row linked to it whose partner
is `Bench Sponsor Inc` and whose `sponsor_type_id` is `Silver`.

# Rules

- Do NOT create more than one sponsor on this event.
- Do NOT create any new `res.partner` or `event.sponsor.type` records — the
  partner `Bench Sponsor Inc` and the sponsor level `Silver` already exist,
  use them as-is.
- Do NOT create any other events or registrations.
- Do NOT change other fields on the event (dates, name, etc.).
