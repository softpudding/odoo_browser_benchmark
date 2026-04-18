"""Oracle for appointment.public_booking_reschedule_cancel_portal.

BLOCKED TASK — the Odoo `appointment` addon is uninstallable in this
Community Edition checkout. The oracle exits with a clear error so the
harness records the blocker instead of producing spurious results.

To flesh out once appointment is installable:
  1. Navigate to /odoo/appointments → open 'Bench Intro Call' → verify
     30-min slot + 1 user resource.
  2. Go to /appointment/<slug>, pick a slot next week, submit
     (Bench Visitor / visitor@bench.test).
  3. Open the confirmation URL returned, click Reschedule to a slot in
     next-week+1, then click Cancel.
"""

from benchmark.oracle_helpers import run_oracle


def oracle(page):
    raise RuntimeError(
        "BLOCKED: appointment module is uninstallable in Odoo Community. "
        "Oracle body intentionally short-circuits. See STATUS.md row 350."
    )


run_oracle(oracle)
