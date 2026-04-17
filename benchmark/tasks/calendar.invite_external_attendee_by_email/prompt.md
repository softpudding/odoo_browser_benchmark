Go to the **Calendar** app and create a new calendar event with the following details:

1. **Title**: "Benchmark Strategy Sync"
2. **Start**: May 14, 2026 at 10:00 AM
3. **Stop (End)**: May 14, 2026 at 11:00 AM
4. **Attendees**: invite the external email address `vendor.partner@example.com`.
   - This email does NOT match any existing contact.
   - Click into the Attendees field and type `vendor.partner@example.com`.
   - In the autocomplete dropdown, select the **"Create ..."** option (it may
     read `Create "vendor.partner@example.com"` or `Create and edit...`). This
     creates a new contact on-the-fly for that email.
   - If a "Create Contact" dialog pops up with the typed text as the name,
     set the contact's **Email** to `vendor.partner@example.com` and save
     the dialog.
   - Do NOT pick any existing contact from the dropdown.

Save the event.

**Rules:**
- Do NOT pick an existing partner for the attendee — you must add the external
  email via the "Create ..." option in the autocomplete dropdown so that
  Odoo creates a new partner for this email.
- The new contact's **Email** must be exactly `vendor.partner@example.com`.
- Do NOT set a Location.
- Do NOT set a Description or notes.
- Do NOT make the event recurring.
- Do NOT invite any additional user beyond the default organizer (admin);
  the only attendee you add should be the external email
  `vendor.partner@example.com`.
- Do NOT enable the "All Day" toggle.
