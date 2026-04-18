"""Postcondition checks for website_sale.apply_product_filter_clear_facets.

Pass criteria:
  * There exists a draft website sale.order (cart) that contains exactly
    one line for 'Bench Widget Tiny', quantity 1.
  * That cart has NO lines for any of the other seeded products.
  * The cart remains in state 'draft' (not confirmed).
  * All five seeded products still exist (not accidentally deleted /
    archived / unpublished).
  * Both seeded categories still exist.

Note: /shop does not require login, so the cart partner may be the
public user or the admin depending on whether the agent logged in.
We therefore match the cart by its Bench Widget Tiny line rather than
by the partner.
"""

TARGET_NAME = "Bench Widget Tiny"
OTHER_NAMES = [
    "Bench Gadget Mini",
    "Bench Gadget Plus",
    "Bench Gadget Pro",
    "Bench Widget Max",
]
CATEGORY_NAMES = ["Gadgets", "Widgets"]


def check(env):
    failures = []

    # All seeded products still exist and are published/active
    for name in [TARGET_NAME, *OTHER_NAMES]:
        tmpl = env["product.template"].with_context(active_test=False).search(
            [("name", "=", name)], limit=1,
        )
        if not tmpl:
            failures.append(f"Product {name!r} is missing")
            continue
        if not tmpl.active:
            failures.append(f"Product {name!r} was archived")
        if not tmpl.is_published:
            failures.append(f"Product {name!r} was unpublished")

    for cname in CATEGORY_NAMES:
        cat = env["product.public.category"].search([("name", "=", cname)], limit=1)
        if not cat:
            failures.append(f"Category {cname!r} is missing")

    target_tmpl = env["product.template"].search([("name", "=", TARGET_NAME)], limit=1)
    if not target_tmpl:
        return failures

    # Find any website cart whose lines reference Bench Widget Tiny.
    carts = env["sale.order"].search([
        ("website_id", "!=", False),
        ("order_line.product_template_id", "=", target_tmpl.id),
    ])
    if not carts:
        failures.append(
            f"No website cart contains a {TARGET_NAME!r} line"
        )
        return failures

    cart = carts.sorted("write_date", reverse=True)[0]

    line_names = cart.order_line.mapped("product_template_id.name")

    forbidden = [n for n in line_names if n in OTHER_NAMES]
    if forbidden:
        failures.append(
            f"Cart contains forbidden product lines: {sorted(set(forbidden))}"
        )

    extra = [n for n in line_names if n not in {TARGET_NAME, *OTHER_NAMES}]
    if extra:
        failures.append(f"Cart contains unexpected extra lines: {sorted(set(extra))}")

    target_lines = cart.order_line.filtered(
        lambda l: l.product_template_id.name == TARGET_NAME
    )
    if len(target_lines) != 1:
        failures.append(
            f"Expected exactly 1 {TARGET_NAME!r} line, got {len(target_lines)}"
        )
    elif abs(target_lines.product_uom_qty - 1.0) > 0.001:
        failures.append(
            f"{TARGET_NAME!r} qty is {target_lines.product_uom_qty}, expected 1"
        )

    if cart.state != "draft":
        failures.append(f"Cart state is {cart.state!r}, expected 'draft'")

    return failures
