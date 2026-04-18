"""Cleanup for appointment.public_booking_reschedule_cancel_portal.

BLOCKED TASK — appointment module is not available in this checkout.
Cleanup is a no-op to avoid NameError on missing models.
"""


def cleanup(env):
    mod = env["ir.module.module"].search([("name", "=", "appointment")], limit=1)
    if not mod or mod.state != "installed":
        return
    # Once the module is installed, append cleanup for appointment.type
    # 'Bench Intro Call' and any calendar.event bookings for Bench Visitor.
