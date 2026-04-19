# Allocate a new leave type, approve, then book a day off against it

You are logged in to Odoo 19 as **Administrator** in the **Time Off** app.

**Bench Worker** is a direct report who needs a custom bonus-days allocation
and then a single-day leave request booked against it. The leave type
`Bench Bonus Days` requires an allocation before any request can be made, so
the order matters: you must approve the allocation first, otherwise the
leave request will not validate.

## What to do

### Part 1 — Allocate 5 days

1. Go to **Time Off → Management → Allocations**.
2. Click **New**.
3. Fill in:
   - **Description**: `Q2 bonus`
   - **Employee**: `Bench Worker`
   - **Time Off Type**: `Bench Bonus Days`
   - **Allocation**: `5 days`
4. **Save** the allocation (cloud icon or the breadcrumb save).
5. Click **Approve** on the saved allocation form. It must move from
   **To Confirm** to **Approved** (state `validate`).

### Part 2 — Book 1 day against the allocation

1. Go to **Time Off → Management → Time Off** (or the New Request
   shortcut from the Time Off app).
2. Click **New**.
3. Fill in:
   - **Description**: `Bench day off`
   - **Employee**: `Bench Worker`
   - **Time Off Type**: `Bench Bonus Days`
   - **Dates**: single day, **May 15, 2026** (start = end = 2026-05-15).
4. **Save** the request.
5. Click **Approve** on the saved form. It must move to **Approved**
   (state `validate`).

After completion there must be **exactly one** approved allocation and
**exactly one** approved leave for Bench Worker with the values above.

## Rules

- The allocation MUST be approved before the leave request is approved —
  otherwise the leave refuses to validate (no allocated balance).
- The allocation is exactly **5 days** for the **Bench Bonus Days** type.
- The leave request is exactly **1 day** on **2026-05-15** (start and end
  equal).
- Use **Bench Worker** for both records.
- Do not refuse, cancel, or delete any records.
- Do not create additional allocations or leave requests.
- Do not modify any other employee, leave type, or unrelated record.
