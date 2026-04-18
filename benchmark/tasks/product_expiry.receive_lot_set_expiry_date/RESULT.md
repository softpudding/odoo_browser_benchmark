# product_expiry.receive_lot_set_expiry_date — run notes

## Oracle

- PASS on iteration 4 (F1=1.0, 37.3s headless).
- State diff: 3/3 expected edits matched (picking.state=done,
  stock.lot create: name=BP-LOT-001, product_id=Bench Perishable).
- 59 API calls; 25 writes, 34 reads. No forbidden ops. RequiredOp
  recall 1.0; HarmfulWriteRate 0.0.

### Oracle iterations

1. **FAIL** — `expiration_date` input not found inside the lot dialog.
   Root cause: Odoo 19 `DateTimeField` renders as `<button>` (not
   `<input>`) whenever `values[i] && picker.activeInput !== field`.
   Had to click the button first to swap it into an editable input.
2. **FAIL** — same widget issue; tightened the widget locator but still
   keyed off `input` only.
3. **FAIL** — diagnosed via full-page screenshot dump to
   `/tmp/lot_dialog_debug.png`; confirmed both `Expiration` and
   `Removal Date` were rendered as buttons.
4. **PASS** — rewritten `_set_datetime_in_dialog` clicks
   `button, input` first, waits for `input` to appear, then types
   `MM/DD/YYYY HH:MM:SS` with a 20ms per-char delay, presses Escape,
   and clicks the modal title to commit.

## Browser-Use (single-shot)

- **PASS** (F1=1.0, 181.3s headless, 0 postcondition failures).
  Calibration surprise — BU solved the multi-modal navigation
  (Details popup → lot m2o internal-link → stock.lot nested dialog →
  set datetime → save chain → Validate) single-shot. The task
  remains a legitimate medium — BU spent ~3x oracle's wall clock and
  the datetime-picker-after-button interaction is non-trivial — but
  it is NOT a reliable failure trap.

## Notes

- Seed installs `product_expiry` on demand (not in base snapshot)
  via `button_immediate_install`.
- Seed sets `use_create_lots=True` AND `use_existing_lots=True` on
  the Receipts picking type so the popup exposes the `lot_id` m2o
  widget (with Create autocomplete + internal-link button), not the
  text-only `lot_name`.
- Seed pre-fills `move_line.quantity = 10` so the agent's sole
  remaining work is the lot-creation + datetime-set + Validate.
- Expiration dates on stock.lot land via a compute chain: writing
  `expiration_date` also recomputes `use_date`, `removal_date`, and
  `alert_date` from the template's `use_time`/`removal_time`/
  `alert_time`. Writing `removal_date` explicitly after
  `expiration_date` overrides the compute.
