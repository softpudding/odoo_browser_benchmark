# Approve a pending time-off request as manager

You are logged in to Odoo 19 as **Administrator** (the Time Off manager) in
the **Time Off** app.

Employee **Marc Demo** submitted a **Paid Time Off** request for a family
event. The request is currently waiting for your approval (state
**To Approve** / `confirm`).

## What to do

1. Open the **Time Off** app.
2. Navigate to the **Approvals** section (left-side menu entry under
   **Management** → **Time Off**, reachable at `/odoo/time-off-approval`).
3. Locate the pending request from **Marc Demo** named
   **"Family event leave"** for **June 17 to June 18, 2026**
   (**Paid Time Off**, 2 days).
4. Open that request and click the **Approve** button on the form
   statusbar.
5. The request must end up in the **Approved** state (backend state
   `validate`).

## Rules

- Approve the **"Family event leave"** request and only that request.
- Do **not** refuse the request.
- Do **not** delete or cancel the request.
- Do **not** create any new time-off requests.
- Do **not** modify any other leave request.
