"""Seed an existing employee for the activity scheduling task.

Category: deep_ui_interaction (EASY).
Starting state: Employee "Sofia Chen" exists with basic information.
The agent must schedule a Call activity via the chatter.
"""


def setup(env):
    # --- Cleanup prior runs ---
    employee = env["hr.employee"].search([("name", "=", "Sofia Chen")], limit=1)
    if employee:
        env["mail.activity"].search([
            ("res_model", "=", "hr.employee"),
            ("res_id", "=", employee.id),
        ]).unlink()

    # --- Ensure employee exists ---
    if not employee:
        env["hr.employee"].create({
            "name": "Sofia Chen",
            "work_email": "sofia.chen@example.com",
            "work_phone": "+1 555 0200",
        })