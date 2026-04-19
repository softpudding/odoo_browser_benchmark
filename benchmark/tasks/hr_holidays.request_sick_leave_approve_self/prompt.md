# Request a sick leave, then approve it as manager

You are logged in to Odoo 19 as **Administrator** in the **Time Off** app.

**Bench Sick Employee** is a direct report whose time off you manage. You must
perform both sides of the workflow: first create a sick-leave request as the
administrator for Bench Sick Employee, then switch to the manager approval
dashboard and approve that request so it moves all the way to the **Approved**
state.

## What to do

### Part 1 — Submit the sick leave request

1. From **Time Off** (URL `/odoo/time-off`), click the green **New Request**
   button (or **New**) to open the new time-off dialog/form.
2. Fill in the request:
   - **Time Off Type**: `Sick Leave`
   - **Employee**: `Bench Sick Employee`
   - **Dates**: start **May 11, 2026** (Monday), end **May 12, 2026**
     (Tuesday) — a two-day sick leave. Use the start/end date fields — this
     is a day-based request, so entering the calendar dates is enough.
   - **Description / Reason** (if shown): `Sick leave benchmark`
3. **Save / Confirm / Submit** the request. It must move into the
   **To Approve** (`confirm`) state — do **not** leave it in `draft`.

### Part 2 — Approve as manager

1. Navigate to **Time Off → Management** (URL
   `/odoo/time-off-approval`) — the manager approval dashboard.
2. Locate the pending request for **Bench Sick Employee** — *Sick Leave* —
   May 11 to May 12, 2026. If default filters hide it, clear the search
   facets until the request is visible.
3. Open the request and click **Approve** (or Validate), or use the bulk
   Approve from the list view with only that row selected.
4. The request must reach **Approved** state (`validate`). Verify by
   re-reading the record — its state should no longer be **To Approve**.

After you are done, there should be **exactly one** `hr.leave` record with:

- type = **Sick Leave**
- employee = **Bench Sick Employee**
- start = **2026-05-11**
- end = **2026-05-12**
- state = **Approved** (`validate`)

## Rules

- You must both **submit** and **approve** the request in this task. The
  request does not pre-exist.
- Use the dates **May 11, 2026** (start) and **May 12, 2026** (end) — these
  are the exact dates the checker validates.
- Use **Sick Leave** (the pre-existing Sick Leave leave type) and
  **Bench Sick Employee** (the pre-existing employee).
- Do **not** refuse, delete, cancel, or duplicate the request.
- Do **not** create any additional leave, allocation, or employee records.
- Do **not** modify any other employee, leave type, or unrelated record.
