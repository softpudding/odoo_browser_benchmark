"""Postcondition checks for sale.add_section_note_line_to_quotation.

Validates:
1. Products `Bench Struct Item A` / `Bench Struct Item B` and partner
   `Bench Struct Co` still exist.
2. Quotation `SO-BENCH-STRUCT` still exists, state='draft', same customer.
3. Both seeded product lines are still present and unmodified:
    * Bench Struct Item A qty=1, display_type unset
    * Bench Struct Item B qty=2, display_type unset
4. A NEW section line exists on the SO:
    * display_type == 'line_section'
    * name == 'Phase 1'   (exact trim-compare)
    * product_id is unset
5. A NEW note line exists on the SO:
    * display_type == 'line_note'
    * name == 'Delivery by end of month' (exact trim-compare)
    * product_id is unset
6. The SO has exactly 4 order lines total (2 products + 1 section + 1 note).
7. Exactly 1 sale.order row for Bench Struct Co (no duplicates created).
"""

PARTNER_NAME = "Bench Struct Co"
SO_NAME = "SO-BENCH-STRUCT"
PRODUCT_A = "Bench Struct Item A"
PRODUCT_B = "Bench Struct Item B"
SECTION_TEXT = "Phase 1"
NOTE_TEXT = "Delivery by end of month"


def _norm(s):
    return (s or "").strip()


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    product_a = env["product.product"].search([("name", "=", PRODUCT_A)], limit=1)
    product_b = env["product.product"].search([("name", "=", PRODUCT_B)], limit=1)
    if not product_a:
        return [f"Product '{PRODUCT_A}' not found"]
    if not product_b:
        return [f"Product '{PRODUCT_B}' not found"]

    # Exactly one SO for this customer
    partner_orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", partner.id)]
    )
    if len(partner_orders) != 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_NAME}', "
            f"found {len(partner_orders)} (names: {partner_orders.mapped('name')})"
        )

    so = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)], limit=1
    )
    if not so:
        failures.append(f"Quotation '{SO_NAME}' not found")
        return failures

    if so.partner_id.id != partner.id:
        failures.append(
            f"SO customer is '{so.partner_id.display_name}', expected '{PARTNER_NAME}'"
        )
    if so.state != "draft":
        failures.append(f"SO state is '{so.state}', expected 'draft'")

    lines = so.order_line
    # Partition by display_type
    product_lines = lines.filtered(lambda l: not l.display_type)
    section_lines = lines.filtered(lambda l: l.display_type == "line_section")
    note_lines = lines.filtered(lambda l: l.display_type == "line_note")

    # --- Product lines (the 2 seeded ones) ---
    if len(product_lines) != 2:
        failures.append(
            f"Expected 2 product lines (display_type unset), found {len(product_lines)}"
        )
    by_product = {l.product_id.id: l for l in product_lines}
    if product_a.id not in by_product:
        failures.append(f"Missing seeded product line '{PRODUCT_A}'")
    elif abs(by_product[product_a.id].product_uom_qty - 1) > 0.001:
        failures.append(
            f"'{PRODUCT_A}' qty is {by_product[product_a.id].product_uom_qty}, expected 1"
        )
    if product_b.id not in by_product:
        failures.append(f"Missing seeded product line '{PRODUCT_B}'")
    elif abs(by_product[product_b.id].product_uom_qty - 2) > 0.001:
        failures.append(
            f"'{PRODUCT_B}' qty is {by_product[product_b.id].product_uom_qty}, expected 2"
        )

    # --- Section line ---
    if len(section_lines) == 0:
        failures.append(
            "No sale.order.line with display_type='line_section' found — "
            "the agent likely used 'Add a product' instead of 'Add a section'"
        )
    elif len(section_lines) > 1:
        failures.append(
            f"Expected exactly 1 line_section row, found {len(section_lines)} "
            f"(names: {section_lines.mapped('name')})"
        )
    else:
        sec = section_lines[0]
        if _norm(sec.name) != SECTION_TEXT:
            failures.append(
                f"Section line name is {sec.name!r}, expected {SECTION_TEXT!r}"
            )
        if sec.product_id:
            failures.append(
                f"Section line must have no product; got product_id="
                f"{sec.product_id.display_name!r}"
            )

    # --- Note line ---
    if len(note_lines) == 0:
        failures.append(
            "No sale.order.line with display_type='line_note' found — "
            "the agent likely used 'Add a product' / 'Add a section' instead of 'Add a note'"
        )
    elif len(note_lines) > 1:
        failures.append(
            f"Expected exactly 1 line_note row, found {len(note_lines)} "
            f"(names: {note_lines.mapped('name')})"
        )
    else:
        note = note_lines[0]
        if _norm(note.name) != NOTE_TEXT:
            failures.append(
                f"Note line name is {note.name!r}, expected {NOTE_TEXT!r}"
            )
        if note.product_id:
            failures.append(
                f"Note line must have no product; got product_id="
                f"{note.product_id.display_name!r}"
            )

    # --- Total line count: exactly 4 (no stray lines) ---
    if len(lines) != 4:
        failures.append(
            f"Expected exactly 4 order lines (2 products + 1 section + 1 note), "
            f"found {len(lines)} (display_types: {lines.mapped('display_type')})"
        )

    return failures
