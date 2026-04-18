Open the **Email Marketing** app (URL `/odoo/email-marketing`).

There is a seeded mailing **"Bench Newsletter V1"** that has already been sent (state = Sent). You need to produce a follow-up mailing by **Duplicating** it rather than creating one from scratch, then editing the copy and sending it.

Steps:

1. Navigate to **Email Marketing → Mailings** and open the mailing whose Subject is exactly **`Bench Newsletter V1`**.
2. Click the **gear / cog (Actions)** menu in the top control panel and choose **Duplicate**. The duplicate form opens automatically — the rest of the edits happen on the duplicate, **not** on the original.
3. On the duplicate:
   - Change the **Subject** to exactly: `Bench Newsletter V2 Spring Special`
   - Confirm the **Recipients** selector is set to **Mailing List** (it is copied from the original — leave it on `Mailing List`, do NOT switch it to `Contact` / `Lead` / any other option).
   - In the **Mailing Lists** field below Recipients, add the list **`Bench Subscribers`**. (The duplicate starts with no mailing list attached — you must explicitly add `Bench Subscribers`.)
   - Keep the **Sender Name / From** value and the email body exactly as copied from the original — do NOT clear or rewrite them.
4. Click the **Send** button in the top control panel. This launches the mailing immediately.
   - If a confirmation dialog appears (e.g. "Ready to send this mass mailing to … recipients?"), click **Send** / **OK** to confirm.

Rules:

- **Do NOT click "Send a Sample Mail"** (test send) and **do NOT click "Schedule"** — we want the mailing launched, not tested, not deferred.
- **Do NOT modify the original `Bench Newsletter V1` mailing**. Its subject, state, and sent date must stay as-is.
- The duplicate's Subject must be exactly `Bench Newsletter V2 Spring Special`, not `Bench Newsletter V1 (copy)` and not anything else.
- **Do NOT create an entirely new mailing from scratch** — use the Duplicate action on the existing V1 record.
- **Do NOT click Duplicate more than once**. After the first Duplicate, the form already shows the new draft copy; click the Save (cloud icon) once after editing if the form is not auto-saved, then click **Send**.
- Do NOT delete either mailing.
