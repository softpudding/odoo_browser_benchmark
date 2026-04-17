# Submit, approve, and post an expense report to accounting

You are in the Odoo 19 **Expenses** app logged in as **Administrator**
(you have both expense-approver and accounting rights).

Employee **Bob Benchmark** has a draft expense report that needs to go
all the way through the pipeline — from draft to journal entry.

## What to do

Complete all three stages in order:

1. **Submit** the draft report:
   - Find the report **TRV-2026-04 – April client visit** in the
     **Drafts** / **My Expenses** view.
   - Open it (it is in **Draft** state) and click **Submit to Manager**.
   - The report moves to the **Submitted** state.

2. **Approve** the submitted report:
   - Switch to the approver view (**Expenses → Expense Reports → To
     Approve**).
   - Open the same report and click **Approve**.
   - The report moves to the **Approved** state.

3. **Post** the approved report to accounting:
   - The report is now in **Approved** state.
   - Click **Post Journal Entries** (or equivalent — the action that
     creates the accounting move).
   - The report should move to the **Done** / **Posted** state, and a
     journal entry should be created and linked to the report.

## Rules

- You must go through **all three** transitions in order: draft → submit
  → approve → post.
- Do **not** skip the submission step or the approval step.
- Do **not** refuse the report.
- Do **not** create or modify any other reports or expense lines.
- The final report must have a linked **journal entry** (account.move).
