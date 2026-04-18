"""Postcondition checks for sale_management.create_quotation_template_apply_to_new_so.

Validates:
1. The quotation template 'Bench Starter Pack' exists with exactly two lines:
   (Bench Widget, qty=5) and (Bench Gadget, qty=2).
2. A draft sale.order for 'Bench Test Co' exists with
   sale_order_template_id pointing to that template.
3. That SO has exactly two order lines matching the template (Widget qty=5,
   Gadget qty=2), state='draft'.
"""

TEMPLATE_NAME = "Bench Starter Pack"
PARTNER_NAME = "Bench Test Co"
PRODUCT_WIDGET = "Bench Widget"
PRODUCT_GADGET = "Bench Gadget"


def check(env):
    failures = []

    # ---- Products ----
    widget = env["product.product"].search([("name", "=", PRODUCT_WIDGET)], limit=1)
    gadget = env["product.product"].search([("name", "=", PRODUCT_GADGET)], limit=1)
    if not widget:
        return [f"Product '{PRODUCT_WIDGET}' not found"]
    if not gadget:
        return [f"Product '{PRODUCT_GADGET}' not found"]

    # ---- Partner ----
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    # ---- Template ----
    templates = env["sale.order.template"].with_context(active_test=False).search(
        [("name", "=", TEMPLATE_NAME)]
    )
    if not templates:
        failures.append(f"Quotation template '{TEMPLATE_NAME}' not found")
        return failures
    if len(templates) > 1:
        failures.append(
            f"Expected exactly 1 quotation template named '{TEMPLATE_NAME}', found {len(templates)}"
        )

    template = templates[0]

    # Template lines — must be exactly two product lines (no sections / notes)
    tlines = template.sale_order_template_line_ids.sorted("sequence")
    product_tlines = tlines.filtered(lambda l: not l.display_type)
    if len(product_tlines) != 2:
        failures.append(
            f"Template '{TEMPLATE_NAME}' expected 2 product lines, found "
            f"{len(product_tlines)} (total lines including sections/notes: {len(tlines)})"
        )
    else:
        # Check each product/qty pair exists
        by_product = {l.product_id.id: l for l in product_tlines}
        if widget.id not in by_product:
            failures.append(f"Template missing '{PRODUCT_WIDGET}' line")
        elif abs(by_product[widget.id].product_uom_qty - 5) > 0.001:
            failures.append(
                f"Template '{PRODUCT_WIDGET}' qty is {by_product[widget.id].product_uom_qty}, expected 5"
            )
        if gadget.id not in by_product:
            failures.append(f"Template missing '{PRODUCT_GADGET}' line")
        elif abs(by_product[gadget.id].product_uom_qty - 2) > 0.001:
            failures.append(
                f"Template '{PRODUCT_GADGET}' qty is {by_product[gadget.id].product_uom_qty}, expected 2"
            )

    # Reject extra sections / notes
    extra = tlines - product_tlines
    if extra:
        types = sorted(set(extra.mapped("display_type")))
        failures.append(
            f"Template has unexpected non-product lines ({types}); expected only 2 plain product lines"
        )

    # ---- Sale Order ----
    orders = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", partner.id),
        ("sale_order_template_id", "=", template.id),
    ])
    if not orders:
        failures.append(
            f"No sale.order found for '{PARTNER_NAME}' with template '{TEMPLATE_NAME}'"
        )
        return failures

    drafts = orders.filtered(lambda o: o.state == "draft")
    if not drafts:
        failures.append(
            f"No draft quotation for '{PARTNER_NAME}'; order states found: "
            f"{sorted(set(orders.mapped('state')))}"
        )
        return failures
    if len(drafts) > 1:
        failures.append(
            f"Expected exactly 1 draft quotation for '{PARTNER_NAME}', found {len(drafts)}"
        )

    so = drafts[0]

    # SO lines — must be exactly two product lines matching the template.
    lines = so.order_line.sorted("sequence")
    product_lines = lines.filtered(lambda l: not l.display_type)

    if len(product_lines) != 2:
        failures.append(
            f"SO expected 2 product order_line rows, found {len(product_lines)} "
            f"(total lines including sections/notes: {len(lines)})"
        )
    else:
        by_product = {l.product_id.id: l for l in product_lines}
        if widget.id not in by_product:
            failures.append(f"SO missing '{PRODUCT_WIDGET}' order line")
        elif abs(by_product[widget.id].product_uom_qty - 5) > 0.001:
            failures.append(
                f"SO '{PRODUCT_WIDGET}' qty is {by_product[widget.id].product_uom_qty}, expected 5"
            )
        if gadget.id not in by_product:
            failures.append(f"SO missing '{PRODUCT_GADGET}' order line")
        elif abs(by_product[gadget.id].product_uom_qty - 2) > 0.001:
            failures.append(
                f"SO '{PRODUCT_GADGET}' qty is {by_product[gadget.id].product_uom_qty}, expected 2"
            )

    # Reject extra sections / notes the agent may have introduced
    so_extra = lines - product_lines
    if so_extra:
        types = sorted(set(so_extra.mapped("display_type")))
        failures.append(
            f"SO has unexpected non-product lines ({types}); expected only 2 plain product lines"
        )

    return failures
