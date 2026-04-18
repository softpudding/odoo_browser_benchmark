# Cookbook notes — hr_attendance.clock_in_out_kiosk_mode

## New / reinforced quirks

- `res.company.attendance_kiosk_mode` selection values in Odoo 19 are
  `barcode`, `barcode_manual`, `manual`. The "Manual Selection" label in
  Settings maps to the raw value `manual` (NOT `manual_selection`). Using
  `manual_selection` writes False and the kiosk controller silently falls
  back to barcode mode.
- Must set `attendance_kiosk_use_pin=True` on the company OR the PIN pad
  is skipped entirely — `manual_selection` controller short-circuits and
  checks the employee in on the first card click.
- `hr.employee._verify_barcode` rejects non-alphanumeric chars and strings
  >18 chars. `ATT-001` raises `ValidationError`; use `ATT001`.
- Backend **Attendances → Kiosk Mode** menu triggers a server action that
  logs the admin out (if a password is set) and 302-redirects to
  `/hr_attendance/<token>`. Any oracle/agent logic that tries to
  round-trip back to `/odoo/...` afterwards must re-login.
- DOM selectors that work in Odoo 19 kiosk:
  - Manual grid:   `.o_hr_kiosk_manual_selection`.
  - Employee card: `.o_hr_kiosk_manual_selection .card:has(h6:has-text('<name>'))`.
  - PIN pad:       `.o_hr_attendance_pin_pad`.
  - Pad button:    `.o_hr_attendance_PINbox_button:has-text('<digit|OK>')`.
  - Greeting card: `.o_hr_attendance_kiosk_card`.
  - Return button: `.o_hr_kiosk_mode_bottom button:has-text('OK')`.

## state_spec / expected_state design

- `hr.attendance.check_in` and `check_out` are dynamic UTC datetimes —
  excluding them from `state_spec.fields` keeps the observed diff clean
  (one `create` event on `employee_id` only). Validate the actual
  timestamps in `check.py` with a today ± 1 day window.

## Browser-use behavior

- BU completed the full 2-phase cycle (card → PIN → OK → greet → OK →
  card → PIN → OK) in 107s on a single shot. The visual distinctness of
  the kiosk UI (big avatar cards, large numpad buttons, On site/Absent
  badges) makes this a solid medium-tier task rather than hard.
