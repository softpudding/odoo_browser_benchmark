# Submit, approve, and post an expense to accounting

You are in the Odoo 19 **Expenses** app logged in as **Administrator**
(you have both expense-approver and accounting rights).

Employee **Bob Benchmark** has a draft expense that needs to go all the
way through the pipeline — from draft to journal entry.

## What to do

Complete all three stages in order:

1. **Submit** the draft expense:
   - Find the expense **TRV-2026-04 — April client visit** in the
     **My Expenses** view.
   - Open it (it is in **Draft** state) and click **Submit**.
   - The expense moves to the **Submitted** state.

2. **Approve** the submitted expense:
   - Switch to the approver / manager view.
   - Open the same expense and click **Approve**.
   - The expense moves to the **Approved** state.

3. **Post** the approved expense to accounting:
   - The expense is now in **Approved** state.
   - Click **Post Journal Entries** (or equivalent — the action that
     creates the accounting move).
   - The expense should move to the **Posted** state, and a journal
     entry (account.move) should be created and linked.

## Rules

- You must go through **all three** transitions in order: draft → submit
  → approve → post.
- Do **not** skip any step.
- Do **not** refuse the expense.
- Do **not** create or modify any other expenses.
- The final expense must have a linked **journal entry** (account.move).
