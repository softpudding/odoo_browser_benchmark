# Refuse an already-approved leave

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

**Marc Demo** already had an approved leave for his family holiday:
- Description: **Family vacation (tentative)**
- Dates: **July 6 – July 10, 2026**
- Leave type: **Paid Time Off**
- State: **Approved** (validated)

Marc's plans changed — the vacation has to be cancelled entirely.
You need to **refuse / cancel the already-approved leave** so it no
longer counts against Marc's allocation.

## What to do

1. Go to **Time Off → Management → Time Off** (the manager approval
   view) so you can see validated leaves.
2. Find the approved request **Family vacation (tentative)** for
   **Marc Demo**. Because it is already Approved, you cannot just delete
   it — you must use the **Refuse** action on the form.
3. Open the request and click **Refuse** (the statusbar action that
   refuses/cancels an approved leave). The request must move to the
   **Refused** state.

## Rules

- The request **Family vacation (tentative)** must be in the **Refused**
  state at the end (not deleted, not still validated).
- Do **not** just change the dates on the original record — refuse it.
- Do **not** modify any other employee's requests.
- Do **not** create new leave requests.
