Open the **Email Marketing** app (URL `/odoo/email-marketing`) and create a new mailing from scratch. Do NOT duplicate any existing mailing — click the **New** button.

There is a pre-seeded mailing list named **`Bench Newsletter Subs`** (with 3 contacts) that you must use.

Fill the new mailing form with EXACTLY these values:

- **Subject**: `Spring Promo`
- **Mailing Type**: keep the default **Email** (do not change this).
- **Recipients**: keep the default **Mailing List** (do not change it to Contact / Lead / any other option).
- **Mailing Lists** (shown below Recipients once `Mailing List` is selected): add the list **`Bench Newsletter Subs`** — type the name and pick the existing row from the autocomplete (do NOT use a "Create …" quick-create item).
- **Mail Body**: in the rich-text body editor (the big content area / iframe below the header fields), write the text: `Save 20%`. Clear any placeholder text first so the final body is exactly this short message.

Then **Schedule** the mailing for a specific date:

1. Click the **Schedule** button in the top control panel (next to the Send button). Do NOT click Send. Do NOT click "Send a Sample Mail".
2. A small dialog titled **"When do you want to send your mailing?"** appears, containing a single **Send on** datetime field.
3. Set the **Send on** datetime to exactly **`05/20/2026 10:00:00`** (i.e. May 20, 2026 at 10:00 AM). Clear any pre-filled value first.
4. Click the primary **Schedule** button at the bottom of that dialog to confirm.

After confirming, the mailing's status changes to **In Queue** and a Scheduled-for date is shown on the form.

Rules:

- **Do NOT click Send** — we want the mailing scheduled for a future date, not sent immediately.
- **Do NOT click "Send a Sample Mail"** (test send).
- **Do NOT change** the Mailing Type away from `Email` or the Recipients away from `Mailing List`.
- The Subject must be exactly `Spring Promo` (no trailing whitespace, no extra words).
- The body must contain `Save 20%` as visible text.
- Use the seeded `Bench Newsletter Subs` list; do NOT create a new mailing list.
- Do NOT create more than one mailing — there must be exactly one `Spring Promo` mailing in the database at the end.
- Do NOT delete any seeded record.
