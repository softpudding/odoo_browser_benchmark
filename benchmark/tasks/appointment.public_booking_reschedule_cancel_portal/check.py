"""Postcondition checks for appointment.public_booking_reschedule_cancel_portal.

BLOCKED TASK — appointment module is uninstallable in this checkout, so
the task cannot run end-to-end. The check below returns a clear failure
so the eval pipeline flags it rather than appearing as a spurious PASS.
"""


def check(env):
    mod = env["ir.module.module"].search([("name", "=", "appointment")], limit=1)
    if not mod or mod.state == "uninstallable":
        return [
            "BLOCKED: appointment module is uninstallable in this Odoo "
            "Community checkout — task cannot be validated end-to-end."
        ]
    if mod.state != "installed":
        return ["appointment module is not installed — seed failed"]

    # Concrete validation to add once the module is available:
    #  - exactly one calendar.event for Bench Visitor, state='cancelled'
    #  - chatter on that calendar.event logs Reschedule then Cancel events
    #  - no extra bookings, no deleted appointment.type
    return [
        "BLOCKED: appointment module was available but check body not "
        "yet implemented. See STATUS.md row 350 for context."
    ]
