"""Seed for hr.generate_employee_card_set_badge_id.

Category 5 (MEDIUM): deep UI interaction.

The agent must open employee 'Bench Worker Badge', switch to the HR 'Settings'
notebook tab, and fill the Badge ID (`hr.employee.barcode`) field with an exact
value `EMPBENCH001`. The Odoo 19 employee form renames this field label to
"Badge ID" but the underlying technical field is `barcode` (there is no
`badge_id` field on `hr.employee` in Odoo 19 — see ODOO19_PATTERNS.md).

Odoo 19 quirk (pre-flight finding): `hr.employee._verify_barcode` rejects any
character outside `[A-Za-z0-9]` and anything longer than 18 chars. We use
`EMPBENCH001` (11 chars, all alphanumeric) so the constraint accepts the value.

We seed the employee with `barcode=False` so the diff engine sees a clean
False -> 'EMPBENCH001' transition, and so the form's "Print Badge" button
(which is `invisible="not barcode"`) is hidden until the agent fills the field.
"""

EMPLOYEE_NAME = "Bench Worker Badge"
EXPECTED_BADGE = "EMPBENCH001"


def _cleanup(env):
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()


def setup(env):
    _cleanup(env)

    job = env["hr.job"].search([("name", "ilike", "developer")], limit=1)
    env["hr.employee"].create({
        "name": EMPLOYEE_NAME,
        "job_id": job.id if job else False,
        "job_title": "Badge Test Worker",
        "barcode": False,
    })
