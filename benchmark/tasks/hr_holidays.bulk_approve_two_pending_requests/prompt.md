# Bulk-approve two pending time-off requests

You are logged in to Odoo 19 as **Administrator** in the **Time Off** app.

Three employees have pending time-off requests **To Approve**, plus a few
already-processed requests as background. You must approve **exactly two**
of the pending requests **at the same time** using the list-view bulk
**Approve** action — **not** by opening each record individually.

## What to do

1. Open **Time Off → Management** (URL `/odoo/time-off-approval`). This is
   the manager approval dashboard.
2. Switch to **list view** (the three-horizontal-lines icon in the top-right
   view switcher). Make sure all three pending requests are visible — if a
   default filter is hiding any of them, clear the search facets.
3. You should see at least these three pending (**To Approve**) requests:
   - **Eve Pending** — *Paid Time Off* — description
     `"Family vacation"` — May 4 to May 6, 2026
   - **Frank Pending** — *Paid Time Off* — description
     `"Wedding attendance"` — May 11 to May 13, 2026
   - **Alice Pending** — *Paid Time Off* — description
     `"Personal errands"` — May 18 to May 20, 2026 (**do NOT approve this one**)
4. Tick the **checkboxes** on **Eve Pending's** row and on
   **Frank Pending's** row — and only those two. Do **not** tick
   Alice's row, and do **not** tick any already-approved/refused row.
5. With exactly those two rows selected, click the bulk **Approve**
   action at the top of the list (the selection-actions bar shows an
   **Approve** / thumbs-up button that becomes visible once rows are
   selected — it is part of the list header actions, available alongside
   the cog "Actions" menu).
6. Both selected leaves must move from **To Approve** (`confirm`) to
   **Approved** (`validate`).

After the action, the list should show Eve's and Frank's requests as
**Approved**, while Alice's request stays **To Approve**.

## Rules

- Approve **exactly** Eve Pending and Frank Pending.
- Do **not** approve or modify **Alice Pending** — her request must remain
  in the **To Approve** state.
- You must perform the approval as a **bulk** action from the list view
  (checkbox select + bulk Approve button). Do **not** open each leave
  individually and click Approve on the form view — that workflow is
  forbidden for this task.
- Do **not** refuse, delete, cancel, duplicate, or edit any record.
- Do **not** create any new time-off requests.
- Do **not** touch the already-approved or refused distractor leaves.
