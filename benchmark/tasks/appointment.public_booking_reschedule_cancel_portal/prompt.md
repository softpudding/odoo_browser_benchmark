# Public appointment booking reschedule + cancel (BLOCKED)

> **Note**: This task is BLOCKED because the `appointment` Odoo addon is not
> present in the Odoo Community Edition checkout used for this benchmark.
> `ir.module.module` reports `state = 'uninstallable'` for `appointment`
> because no source code / manifest exists in `addons/`. The task cannot be
> executed end-to-end without pulling the enterprise-only `appointment`
> module into the codebase.
>
> The original task intent is preserved below for future re-scoping when
> enterprise addons become available.

You will complete a three-phase appointment workflow that round-trips
between the Odoo back-office and the public portal.

A seeded appointment type named `Bench Intro Call` already exists with a
30-minute slot and one user resource assigned.

## Phase 1 — Back-office: verify configuration

1. Open the **Appointments** app (`/odoo/appointments`).
2. Open the `Bench Intro Call` appointment type and verify:
   - Duration is 30 minutes.
   - At least one user resource is assigned.

## Phase 2 — Public portal: book the slot

3. Navigate to the public booking URL for the appointment type (e.g.
   `/appointment/<slug>`).
4. Pick any available slot in next week's calendar.
5. Submit the booking form with:
   - **Name**: `Bench Visitor`
   - **Email**: `visitor@bench.test`
6. Confirmation page appears with a unique booking URL.

## Phase 3 — Portal: reschedule and cancel

7. Open the confirmation URL returned by Phase 2.
8. Click **Reschedule** and pick a slot in the next-week+1 timeframe.
9. Click **Cancel** to cancel the rescheduled booking.

## Rules

- Exactly one booking for `Bench Visitor` must exist when done.
- Final state of that booking must be **cancelled**.
- Chatter on the booking must show Reschedule then Cancel events.
