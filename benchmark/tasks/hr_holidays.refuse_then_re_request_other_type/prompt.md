# Refuse a leave and re-request as a different leave type

You are in the Odoo 19 **Time Off** app logged in as **Administrator**
(the leave manager). An employee submitted a vacation request, but
because the dates conflict with HR policy you must refuse it and
create a Sick Time Off request on her behalf for the same dates.

## What to do

1. Navigate to **Time Off → Managers → Time Off** (the manager
   approval view at `/odoo/time-off-approval`).
2. Find the pending request from **Eve Employee** for **Paid Time Off**
   dated **August 10 to August 12, 2026** with the description
   **"Family vacation"**.
3. Open that request and click **Refuse**.
4. On the same refused request, post a chatter message with this
   exact text as its body:

   ```
   Use sick leave instead
   ```

5. Go back to the Managers' **Time Off** list. Click **New** to start
   a fresh leave request and fill it in:
   - **Mode**: `By Employee` (the default works)
   - **Employee**: `Eve Employee`
   - **Time Off Type**: `Sick Time Off`
   - **Dates**: from **August 10, 2026** to **August 12, 2026** (3 days)
   - **Description**: `Sick leave per manager`
6. Save the new request. It must end up in the **To Approve**
   (`confirm`) state — do **not** approve or validate it.

## Rules

- Refuse **only** the Paid Time Off request from Eve Employee — do not
  refuse any other leave.
- The chatter message on the refused leave must contain the exact text
  `Use sick leave instead`.
- The new leave must use **Sick Time Off**, NOT Paid Time Off, and the
  employee on the new leave must be **Eve Employee** (not yourself).
- Leave the new Sick Time Off request in the **To Approve** state — do
  not approve it.
- Do **not** delete any leaves.
