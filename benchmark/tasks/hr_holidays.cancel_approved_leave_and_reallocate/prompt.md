# Cancel an approved leave and re-submit with corrected dates

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

**Marc Demo** already had an approved leave for his family holiday:
- Description: **Family vacation (tentative)**
- Dates: **July 6 – July 10, 2026**
- Leave type: **Paid Time Off**
- State: **Approved** (validated)

Marc's plans changed — his family can only travel **one week later**.
You need to **cancel the approved request** and submit a **new request**
for the corrected dates.

## What to do

1. Go to **Time Off → Management → Time Off** (the manager approval
   view).
2. Find the approved request **Family vacation (tentative)** for
   **Marc Demo**. Since it is already Approved, you cannot just edit the
   dates — you must first take it out of Approved state.
3. Open the approved request and click **Refuse** (or the action that
   cancels / refuses an approved leave). The request should move to
   the **Refused** state.
4. Create a brand-new leave request (use **New** / **New Time Off**
   in the manager view) with:
   - **Employee**: `Marc Demo`
   - **Time Off Type**: `Paid Time Off`
   - **Dates**: `July 13 – July 17, 2026` (exactly 5 working days later)
   - **Description**: `Family vacation (confirmed)`
5. Save and **Approve** (validate) the new request so it ends in the
   **Approved** state.

## Rules

- The original request **Family vacation (tentative)** must be in
  **Refused** state at the end (not deleted, not still validated).
- Do **not** just change the dates on the original record — it is
  already approved, and the correct workflow is refuse-then-replace.
- The new request **Family vacation (confirmed)** must be:
  - For **Marc Demo**.
  - Dates **July 13–17, 2026** (5 calendar days).
  - Type **Paid Time Off**.
  - State **Approved / Validated**.
- Do **not** modify any other employee's requests.
- Do **not** create multiple replacement requests.
