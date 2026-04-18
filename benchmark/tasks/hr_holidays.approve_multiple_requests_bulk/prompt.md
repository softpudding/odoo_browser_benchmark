# Bulk-approve three pending time-off requests

You are logged in to Odoo 19 as **Administrator** in the **Time Off** app.

Four employees on the bench team have recently logged time-off requests:

- **Bench Alice** — *Paid Time Off* — 2 days — **To Approve** (pending)
- **Bench Bob** — *Paid Time Off* — 3 days — **To Approve** (pending)
- **Bench Carol** — *Paid Time Off* — 1 day — **To Approve** (pending)
- **Bench Diana** — *Paid Time Off* — 1 day — **Refused** (already refused
  — this request was rejected earlier and must remain refused)

Your job is to approve the **three pending (To Approve)** requests in a
single bulk action from the list view. **Diana's Refused request must
NOT be re-approved** — it was already refused and its state must stay
`Refused`.

## What to do

1. Open **Time Off → Approvals** (the manager dashboard at URL
   `/odoo/time-off-approval`).
2. Switch to **list view** (the three-horizontal-lines icon in the
   top-right view switcher).
3. The list is filtered by default (e.g. *Waiting For Me*, *This Year*).
   **Clear those search facets** by clicking the small **×** on each
   facet in the search bar so that Alice's, Bob's, and Carol's pending
   requests and Diana's refused request are all visible.
4. Tick the **checkboxes** on **exactly these three rows**:
   - Bench Alice's 2-day *Paid Time Off* request (**To Approve**)
   - Bench Bob's 3-day *Paid Time Off* request (**To Approve**)
   - Bench Carol's 1-day *Paid Time Off* request (**To Approve**)

   Do **not** tick any other row. In particular, do **not** tick
   Diana's row (her request is **Refused**, not **To Approve**).
5. With exactly those three rows selected, click the bulk **Approve**
   button that appears at the top of the list (it is shown in the
   selection-actions bar — alongside the cog "Actions" menu — once you
   have ticked rows). This is a genuine bulk action that approves all
   selected leaves in one call.
6. Each of Alice's, Bob's, and Carol's requests must transition from
   **To Approve** (`confirm`) to **Approved** (`validate`).
7. Diana's request must still be in **Refused** (`refuse`).

## Rules

- Approve **exactly** the three pending requests from Alice, Bob, and
  Carol. Diana's Refused request must remain refused.
- You must use a **bulk list-view approval**: checkbox-select the three
  pending rows and click the **Approve** bulk-action button.
  Do **not** open each leave form individually and click Approve.
- Do **not** refuse, cancel, delete, duplicate, or edit any leave.
- Do **not** create new time-off requests.
- Do **not** re-approve, reset, or otherwise modify Diana's Refused
  request.
