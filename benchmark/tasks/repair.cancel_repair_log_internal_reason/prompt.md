Go to the **Repairs** app (URL `/odoo/repairs`).

Open the existing repair order **`RO/CANCEL/0001`** for customer **`Cancel Cordelia`** on product **`Bench Cooler Compressor`**. It is in the **Confirmed** stage.

Do the following two things on this repair order:

1. **Log an internal note** in the chatter at the bottom of the form. Click **Log note** (NOT *Send message* — the note must be internal-only and not emailed to the customer), then type exactly:

   ```
   Customer requested cancellation - replacement parts no longer needed
   ```

   Click **Log** (or press Enter) to post the note.

2. **Cancel the repair order**: in the top control panel button strip, click the **Cancel Repair** button. The state badge should change to **Cancelled**.

## Rules

- The chatter post must be a **Log note** (subtype *Note*), not a public *Send message*. Do not click "Send message".
- The note text must be exactly the sentence above (a single line, no extra punctuation).
- Do not start the repair (do not click "Start Repair") and do not mark it as Repaired.
- Do not delete the repair order.
- Do not create any new repair orders, products, or partners.
- Do not modify the existing repair line.
