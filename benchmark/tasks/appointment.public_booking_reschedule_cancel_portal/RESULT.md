# appointment.public_booking_reschedule_cancel_portal — RESULT

## Verdict: REMOVED (module unavailable)

This task is blocked because the Odoo `appointment` addon is not
available in the Community Edition checkout used for this benchmark.

## Evidence

```
psql -d benchmark_* -c "SELECT name, state FROM ir_module_module WHERE name = 'appointment';"
 name        | state
-------------+---------------
 appointment | uninstallable
```

`state='uninstallable'` means Odoo has registered the module name (via
dependency references) but cannot find a manifest (`__manifest__.py`)
or source code under any configured `addons_path`. Calling
`button_immediate_install()` on an uninstallable record raises
`UserError`.

## Precedent

An earlier sibling task (`appointment.portal_reschedule_and_cancel_booking`)
was also removed for the same reason. See STATUS.md detail section.

## Lifecycle status

- Oracle: did NOT run (short-circuits with RuntimeError).
- BU: did NOT run.
- F1: N/A.
- Calibration: N/A.

## Re-enabling

To re-enable, vendor the enterprise `appointment`, `website_appointment`,
and `appointment_account_payment` addons into `addons/` (or add an
`addons_path` entry), then:

1. Flesh out `seed.py` to create `appointment.type` 'Bench Intro Call'
   with a 30-minute slot + one `appointment.resource` user.
2. Flesh out `oracle.py` with the three-phase UI flow.
3. Flesh out `check.py` to assert `calendar.event.state=='cancelled'`
   for the Bench Visitor booking and chatter contains Reschedule and
   Cancel mail.message entries.
4. Flip STATUS row 350 from Removed → WIP and re-run the normal
   lifecycle.
