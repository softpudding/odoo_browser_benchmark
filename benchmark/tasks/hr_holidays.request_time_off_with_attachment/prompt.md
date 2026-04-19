# Request a Paid Leave and attach a justification PDF through the chatter

You are logged in to Odoo 19 as **Administrator** in the **Time Off** app
(start URL `/odoo/time-off`).

You need to submit a 2-day time-off request of type **Paid Leave** for
yourself (the admin's own employee record) AND attach the pre-seeded
**BENCH-JUST.pdf** justification file to the saved request through the
**chatter paperclip**.

## What to do

1. In **Time Off** (`/odoo/time-off`), click the green **New Request**
   button (or **New**) to open the new time-off form / dialog.
2. Fill in the request:
   - **Time Off Type**: `Paid Leave`
   - **Dates**: from **July 1, 2026** (Wednesday) to **July 2, 2026**
     (Thursday) — 2 working days.
   - **Description / Reason** (if the field is visible): `Medical appointment`
3. **Save** the request. It must land in the **To Approve** (`confirm`)
   state — do **not** approve / validate it yourself.
4. On the saved `hr.leave` form, scroll to / open the **chatter** panel.
   Click the **paperclip** icon (aria-label "Attach files") in the chatter
   and upload the pre-seeded PDF located at:

   ```
   benchmark/tasks/hr_holidays.request_time_off_with_attachment/seed_artifacts/BENCH-JUST.pdf
   ```

   Wait for the attachment chip showing `BENCH-JUST.pdf` to appear in the
   chatter attachments area. The attachment must be linked to **this**
   `hr.leave` record (res_model=`hr.leave`, res_id=the saved leave id).

## Expected end state

Exactly **one** `hr.leave` record exists with:

- **Time Off Type** = `Paid Leave`
- **Employee** = admin's own employee
- **Start** = `2026-07-01`
- **End** = `2026-07-02`
- **Duration** = 2 working days (`number_of_days = 2.0`)
- **State** = `To Approve` (`confirm`) — NOT `validate`
- At least one **ir.attachment** with `res_model='hr.leave'`,
  `res_id=<this leave id>`, `name='BENCH-JUST.pdf'`, and non-empty bytes.

## Rules

- Use **Paid Leave** exactly — not `Sick Leave`, `Annual Leave`, or any
  other pre-existing type. The seed creates the `Paid Leave` type fresh
  with `requires_allocation=False`, so you do NOT need to allocate first.
- The dates **2026-07-01 → 2026-07-02** are the exact dates the checker
  validates. Change the start and end dates from their defaults using the
  date widget — do NOT leave the defaults.
- Do **NOT** approve or validate the request yourself — it must stay in
  `To Approve` (`confirm`).
- Upload the PDF **through the chatter paperclip** — do NOT paste the
  file contents into the description, and do NOT upload a different
  filename. The attachment's `name` must be exactly `BENCH-JUST.pdf`.
- The attachment must be linked to the new `hr.leave` record
  (`res_model='hr.leave'`), not to the partner, user, or an unrelated
  record.
- Do **NOT** create additional leaves, allocations, or employee records.
- Do **NOT** delete, refuse, or cancel the request.
