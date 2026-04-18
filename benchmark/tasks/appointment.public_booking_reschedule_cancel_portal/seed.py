"""Seed for appointment.public_booking_reschedule_cancel_portal.

BLOCKED TASK — the Odoo `appointment` addon is not present in the
Community Edition checkout used for this benchmark. `ir.module.module`
reports `state='uninstallable'` because no source code / manifest is
found in the `addons/` path. `button_immediate_install()` on an
uninstallable record raises UserError, so we cannot silently skip.

To keep the benchmark pipeline stable, this seed raises a clear error
so the eval pipeline records the blocker instead of crashing during
browser interaction.
"""


def setup(env):
    mod = env["ir.module.module"].search([("name", "=", "appointment")], limit=1)
    if not mod or mod.state == "uninstallable":
        raise RuntimeError(
            "appointment module is uninstallable in this Odoo Community "
            "checkout. Task blocked until enterprise addons are available. "
            "See STATUS.md row 350 for details."
        )
    if mod.state != "installed":
        mod.button_immediate_install()
    # If the module ever becomes installable in the base snapshot,
    # add the concrete seed logic below (create appointment.type
    # 'Bench Intro Call', slots, resource assignment, etc.).
    raise NotImplementedError(
        "Seed body intentionally left empty — flesh out when "
        "appointment addon is available."
    )
