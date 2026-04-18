Open the **Email Marketing** app (URL `/odoo/email-marketing`).

Find the existing draft mailing with subject **"Q1 Bulletin Template"** and open it.

Duplicate this mailing and edit the duplicate:

1. Open the mailing **Q1 Bulletin Template**.
2. Click the **gear/cog (Actions)** menu in the top control panel and choose **Duplicate** to create an exact copy.
3. The new draft mailing opens automatically. On that copy:
   - Change the **Subject** to exactly: `Q2 Bulletin Update`
   - Change the **Recipients** dropdown (technical name `mailing_model_id`, the field next to the "Recipients" label) from `Mailing List` to `Contact`.
   - In the recipients filter editor that appears below the Recipients dropdown, click **Add condition** (or **New Rule**) and configure exactly one rule:
     - Field: `Country`
     - Operator: `=` (equals / "is in" — pick the equality option)
     - Value: `Germany`
4. Click the cloud-shaped **Save** icon in the top control panel (or use the Save action) to save the duplicate.

Rules:
- **Do NOT click Send, "Send to All", "Send Now", "Test", or schedule the mailing.** The duplicate must remain in `Draft` state.
- **Do NOT modify the original `Q1 Bulletin Template` mailing in any way** — same subject, same recipients model (Mailing List), still draft.
- The duplicate's Subject must be exactly `Q2 Bulletin Update` (not "Q1 Bulletin Template (copy)").
- The duplicate's Recipients model must be `Contact` (i.e. `res.partner`), with a domain that filters by Country = Germany.
- Do NOT delete the original or the duplicate.
- Do NOT create an entirely new mailing from scratch — you must use the Duplicate action.
