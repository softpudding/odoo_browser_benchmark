# Split a submitted expense batch — refuse the Gadget line, approve the rest

You are in the Odoo 19 **Expenses** app logged in as **Administrator**, acting
as the expense **manager / approver** for employee **Lee Bench**.

Lee just submitted three expenses tagged with the trip reference
**R-BENCH-SPLIT-001** (all currently in the **Submitted** state):

| Expense description | Category | Total |
|---|---|---|
| `R-BENCH-SPLIT-001 Meal` | Meals | `40.00` |
| `R-BENCH-SPLIT-001 Gadget` | Office Supplies | `500.00` |
| `R-BENCH-SPLIT-001 Taxi` | Travel | `25.00` |

The **Gadget** line is non-compliant (company policy caps non-IT gadgets at
$100). The Meal and Taxi lines are fine.

## What to do

You must effectively **split the submitted batch in two**:

1. Navigate into the manager's approver view of submitted expenses. A handy
   shortcut is **Expenses → Expense Reports → To Approve** (or the list
   that shows Submitted expenses across employees).
2. Open the expense **R-BENCH-SPLIT-001 Gadget** (the `$500.00` line).
3. Click **Refuse** in the form statusbar. A dialog appears asking for a
   refusal reason.
4. Enter the reason exactly: `Not compliant`
5. Confirm the dialog (click **Refuse Expense** / the primary confirm button).
   The Gadget expense should move to the **Refused** state.
6. Go back to the Submitted list. Open **R-BENCH-SPLIT-001 Meal** and click
   **Approve** in the statusbar so the line moves to **Approved**.
7. Go back to the Submitted list. Open **R-BENCH-SPLIT-001 Taxi** and click
   **Approve** so that line moves to **Approved** as well.

After you finish, the batch is effectively split: Meal + Taxi are **approved**
and ready to be posted, and the Gadget line is **refused** with the reason
recorded in its chatter.

## Rules

- The refusal reason **must** be exactly `Not compliant` (no extra
  punctuation, no trailing period, case-sensitive).
- Only the **Gadget** line may be refused. The Meal and Taxi lines must
  end up **Approved**, not refused and not still Submitted.
- Do **not** post, pay, or reset any of the three expenses.
- Do **not** delete any expense — the Gadget record must remain, just in
  the Refused state.
- Do **not** touch any unrelated expenses for other employees.
