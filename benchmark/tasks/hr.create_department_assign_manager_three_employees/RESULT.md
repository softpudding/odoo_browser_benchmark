ROW: 321
TASK_ID: hr.create_department_assign_manager_three_employees
DIFFICULTY: medium
SUMMARY: Create Bench Engineering dept w/ manager Mike Manager, then bulk-reassign 3 engineers' department_id.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## hr.create_department_assign_manager_three_employees

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | HR |
| **Workflow** | Create a new `hr.department` named `Bench Engineering` via the Departments view, set its `manager_id` to Mike Manager, then loop through three seeded employees (Eng One/Two/Three) and reassign each one's `department_id` to the new department. |
| **Capability tested** | Bulk reassignment across multiple records combined with a related-record creation step. |
| **Notes** | BU completed dept creation and assigned Eng One + Eng Two correctly but cleared Eng Three's department to null (4/5 atomic edits matched, 1 missing, 1 extra). Predicted "may forget one" calibration trap fires cleanly. Department form lives at `/odoo/departments`; `manager_id` uses `many2one_avatar_employee` widget but standard `set_many2one` still works. |
