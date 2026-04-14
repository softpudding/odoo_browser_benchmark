"""Postcondition checks for account.complete_customer_tax_id_then_post."""


def check(env):
    failures = []

    east = env["res.partner"].search([("name", "=", "Northwind Studio East")], limit=1)
    west = env["res.partner"].search([("name", "=", "Northwind Studio West")], limit=1)
    move = env["account.move"].search([("invoice_origin", "=", "VAT-302")], limit=1)

    if not east or not west or not move:
        return ["Missing seeded partner or invoice records for VAT-302 task"]

    if east.vat != "EU3029981":
        failures.append(f"East customer VAT is {east.vat!r}, expected 'EU3029981'")
    if west.vat:
        failures.append(f"West customer VAT is {west.vat!r}, expected to stay empty")
    if move.state != "posted":
        failures.append(f"Invoice state is {move.state!r}, expected 'posted'")
    if move.ref != "VAT-302-CLEAR":
        failures.append(f"Customer Reference is {move.ref!r}, expected 'VAT-302-CLEAR'")

    return failures

