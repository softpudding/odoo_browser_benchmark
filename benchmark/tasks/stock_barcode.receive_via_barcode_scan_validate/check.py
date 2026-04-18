"""Postcondition checks for stock_barcode.receive_via_barcode_scan_validate.

BLOCKED TASK — `stock_barcode` addon is not vendored in this Odoo 19
Community checkout, so the task cannot run end-to-end. The check below
returns a clear failure string so the eval pipeline flags it rather
than appearing as a spurious PASS.
"""


def check(env):
    module = env["ir.module.module"].search(
        [("name", "=", "stock_barcode")], limit=1
    )
    if not module or module.state != "installed":
        return [
            "BLOCKED: `stock_barcode` addon is not available in this Odoo "
            "Community checkout (Enterprise-only). Task cannot be validated "
            "end-to-end. See STATUS.md row 401 for re-enabling notes."
        ]

    # Concrete validation to add once the addon is vendored:
    #   - exactly one `stock.picking` with name='R-BENCH-BC-001' and
    #     state == 'done'.
    #   - picking has exactly 2 stock.move rows, one per product.
    #   - stock.move for Bench Barcode A has quantity == 3.0.
    #   - stock.move for Bench Barcode B has quantity == 3.0.
    #   - no backorder: picking.backorder_ids is empty.
    return [
        "BLOCKED: stock_barcode addon became available but check body not "
        "yet implemented. See STATUS.md row 401 for context."
    ]
