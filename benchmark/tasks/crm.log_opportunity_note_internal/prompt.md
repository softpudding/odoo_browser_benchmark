Go to the **CRM** app.

Find the opportunity named **"Bench Note Opp"** (for customer **"Bench Note Co"**) in the pipeline and open its form.

In the chatter at the bottom of the form:

1. Click the **Log note** tab (NOT "Send message"). The chatter opens on **Log note** by default, but make sure the **Log note** tab is the active one before typing.
2. Type the following text exactly into the composer:

   ```
   Customer asked for demo
   ```

3. Click **Log** to post the internal note.

## Rules

- You MUST use **Log note** — do NOT use **Send message**. The internal-note subtype (`mail.mt_note`) is required; a public Send-message post (subtype `mail.mt_comment`) will fail the check.
- Do NOT change any fields on the opportunity form (stage, revenue, probability, customer, etc.).
- Do NOT schedule an activity, mark it Won/Lost, or convert it to a lead.
- Do NOT delete, archive, or rename the opportunity.
- Post exactly **one** note — no duplicates.
