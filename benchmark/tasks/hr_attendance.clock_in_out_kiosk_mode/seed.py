"""Seed for hr_attendance.clock_in_out_kiosk_mode.

Category 5 (MEDIUM): deep UI interaction with a public kiosk tablet UI
(employee grid -> PIN numpad -> greetings auto-return) executed twice
(check in then check out).

Creates employee 'Bench Worker' with PIN '1234' and barcode 'ATT-001',
and configures the company to use manual kiosk selection with PIN
identification. `attendance_from_systray` is disabled so the agent cannot
clock in from the backend navbar widget.
"""

EMPLOYEE_NAME = "Bench Worker"
EMPLOYEE_PIN = "1234"
EMPLOYEE_BARCODE = "ATT001"


def _ensure_hr_attendance_installed(env):
    mod = env["ir.module.module"].search([("name", "=", "hr_attendance")], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup(env):
    env["hr.attendance"].sudo().search(
        [("employee_id.name", "=", EMPLOYEE_NAME)]
    ).unlink()
    employees = env["hr.employee"].with_context(active_test=False).search(
        [("name", "=", EMPLOYEE_NAME)]
    )
    for emp in employees:
        emp.sudo().unlink()


def setup(env):
    _ensure_hr_attendance_installed(env)
    _cleanup(env)

    company = env.company
    # attendance_kiosk_mode in Odoo 19 is one of: 'barcode', 'barcode_manual', 'manual'.
    # 'manual' corresponds to the "Manual Selection" label in the Settings UI.
    company.sudo().write({
        "attendance_kiosk_mode": "manual",
        "attendance_kiosk_use_pin": True,
        "attendance_from_systray": False,
    })

    env["hr.employee"].sudo().create({
        "name": EMPLOYEE_NAME,
        "company_id": company.id,
        "pin": EMPLOYEE_PIN,
        "barcode": EMPLOYEE_BARCODE,
    })
