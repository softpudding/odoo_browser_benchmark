"""Oracle for stock_barcode.receive_via_barcode_scan_validate.

BLOCKED TASK — the Barcode tablet UI at `/odoo/barcode` is shipped by the
Enterprise-only `stock_barcode` addon, which is NOT vendored in this
Odoo 19 Community checkout. The oracle exits with a clear error so the
harness records the blocker instead of producing spurious results.

To flesh out once the enterprise stock_barcode addon is vendored:
  1. Navigate to /odoo/barcode. Land on the main menu with the tiles
     Operations / Inventory Adjustments / Batch Transfers.
  2. Click Operations → Receipts.
  3. Open R-BENCH-BC-001.
  4. For Bench Barcode A: type 'BENCH-A-001' into the hidden scan
     input (or click the `+` button three times). Confirm the move
     line's reserved qty is 3.0.
  5. For Bench Barcode B: same, with 'BENCH-B-002'.
  6. Click Validate. Assert the toast 'The transfer has been validated'
     appears and the header reads 'Done'.

The enterprise Barcode app historically uses a `<input>` element with
class `o_barcode_input` (or similar) behind a pointer-events:none
barrier; programmatic input via `page.keyboard.type('BENCH-A-001')` +
`page.keyboard.press('Enter')` drives the same code path as a physical
scanner. The `+ 1` tile is typically `button.o_add_reserved` or
`button.o_barcode_line_btn_add_quantity` — selector names have shifted
between Odoo versions, confirm against the Enterprise source before
writing selectors.
"""

from benchmark.oracle_helpers import run_oracle


def oracle(page):
    raise RuntimeError(
        "BLOCKED: /odoo/barcode (stock_barcode client action) is not "
        "available in this Odoo 19 Community checkout (Enterprise-only). "
        "Oracle body intentionally short-circuits. See STATUS.md row 401."
    )


run_oracle(oracle)
