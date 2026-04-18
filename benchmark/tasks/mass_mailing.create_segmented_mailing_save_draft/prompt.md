Create a new email mailing in the Email Marketing app and save it as a draft.

Steps:
1. Open the Email Marketing app (URL `/odoo/email-marketing` or main menu "Email Marketing").
2. Click **New** to create a new mailing.
3. Fill the form:
   - **Subject:** `Berlin April Bulletin`
   - **Recipients:** select `Contact` from the Recipients dropdown (the field next to the "Recipients" label, technical name `mailing_model_id`). After picking `Contact`, the recipients filter section shows a domain editor.
   - **Filter recipients to Berlin only:** below the Recipients dropdown, the domain editor reads "Match all records". Click **Add condition** (or the **New Rule** link), then configure exactly one rule:
     - Field: `City`
     - Operator: `=` (equals)
     - Value: `Berlin`
   - The record-count line under the editor must show **2 record(s)** once the filter is applied.
4. Open the **Mail Body** tab and type this text into the email body editor:
   `Hello Berlin team — here is our April bulletin.`
5. Click the cloud-shaped **Save** icon in the top control panel (or use the Save action) to save the mailing.

Rules:
- **Do not click Send, "Send to All", "Test", or schedule the mailing.** The mailing must remain in `Draft` state at the end.
- The Subject must be exactly `Berlin April Bulletin`.
- The Recipients model must be `Contact` (i.e. `res.partner`), not `Mailing List` (the default).
- The body must contain the literal text `Berlin team`.
- Do not modify or delete the existing Berlin / Munich seed contacts.
- Create only this one mailing.
