ROW: 368
TASK_ID: hr_expense.split_submitted_report_resubmit
DIFFICULTY: hard
SUMMARY: As expense approver, refuse the suspicious Gadget line (reason 'Not compliant') in a 3-expense submitted batch tagged R-BENCH-SPLIT-001 and approve the remaining two lines (Meal + Taxi). Replaces the old hr.expense.sheet split/resubmit flow since the sheet model is removed in Odoo 19.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier-than-expected (BU solved it single-shot in 143.4s / F1=1.0)

DETAIL_SECTION:
## hr_expense.split_submitted_report_resubmit

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 44.0s) |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 143.4s single-shot) |
| **F1** | 1.0 |
| **Odoo modules** | Expenses |
| **Workflow** | Seed 3 submitted `hr.expense` records for employee `Lee Bench` sharing the trip identifier R-BENCH-SPLIT-001: Meal (40, Bench Meals), Gadget (500, Bench Office Supplies, non-compliant), Taxi (25, Bench Travel). Admin is granted the three expense-approver groups (team_approver + manager + user) so the approve/refuse buttons are visible on the form statusbar. Agent opens the approver list (`/odoo/action-hr_expense.hr_expense_actions_my_all` or the standard Expenses app), clicks into the Gadget expense, hits **Refuse** in the statusbar, fills the wizard reason `Not compliant`, confirms. Goes back, opens Meal, clicks **Approve**. Opens Taxi, clicks **Approve**. End state: Meal + Taxi in `approved`, Gadget in `refused`, `Not compliant` snippet recorded in Gadget chatter. |
| **Capability tested** | Per-line triage of a multi-expense submitted batch — agent must refuse one specific line (with a filled wizard reason) AND approve the other two, NOT blanket-approve or blanket-refuse. Tests ability to loop over a batch, pick the right line by description, handle the refuse-reason modal, and re-open siblings for separate approval. |
| **Notes** | Original spec (from STATUS row 368) assumed the legacy `hr.expense.sheet` model with per-line refuse + automatic split of refused lines into a new sheet. That model is **removed in Odoo 19** (see ODOO19_PATTERNS.md) — the approval workflow now lives directly on `hr.expense` with `approval_state in {submitted, approved, refused}`. Pivoted the task to "per-expense triage of 3 submitted records tagged with a shared trip id". BU calibration **FAILED**: browser-use solved the task single-shot in 143.4s with F1=1.0 and zero postcondition failures — the multi-step loop (refuse + 2 approves) plus the refuse-reason modal did not trip it. Kept at hard tier anyway since the "refuse-one-approve-two" loop remains a multi-record triage pattern that can fail other runs. New cookbook entries: (1) `hr.expense` per-line refuse statusbar button opens `hr.expense.refuse.wizard` modal with a required `reason` Char; confirm button calls `action_refuse` which posts the mail template `hr_expense.hr_expense_template_refuse_reason` to the chatter. (2) The admin needs BOTH `group_hr_expense_team_approver` AND `group_hr_expense_manager` + `group_hr_expense_user` to see approve/refuse on expenses belonging to another employee. (3) The "Submitted / To Approve" manager list is reachable via action xmlid `hr_expense.hr_expense_actions_my_all`, reliable for oracle navigation. |
