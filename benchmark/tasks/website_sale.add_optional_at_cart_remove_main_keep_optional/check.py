"""Postcondition checks for
website_sale.add_optional_at_cart_remove_main_keep_optional.

Pass criteria:
  * The 'Bench Tripod' product exists in some draft website sale.order
    associated with the admin user.
  * That cart has exactly ONE line, for Bench Tripod, qty 1.
  * That cart has NO line for Bench Camera.
  * The cart's state is 'draft'.
  * Both Bench Camera and Bench Tripod still exist as products (not
    accidentally archived/unlinked).
"""

MAIN_NAME = "Bench Camera"
OPTIONAL_NAME = "Bench Tripod"


def check(env):
    failures = []

    main_tmpl = env["product.template"].search([("name", "=", MAIN_NAME)], limit=1)
    optional_tmpl = env["product.template"].search([("name", "=", OPTIONAL_NAME)], limit=1)
    if not main_tmpl:
        failures.append(f"Product {MAIN_NAME!r} no longer exists")
    if not optional_tmpl:
        failures.append(f"Product {OPTIONAL_NAME!r} no longer exists")
    if not main_tmpl or not optional_tmpl:
        return failures

    admin = env.ref("base.user_admin")
    carts = env["sale.order"].search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
    ])

    # Find a cart that contains Bench Tripod
    tripod_carts = carts.filtered(
        lambda o: OPTIONAL_NAME in o.order_line.mapped("product_template_id.name")
    )
    if not tripod_carts:
        failures.append(
            f"No website cart for admin contains a {OPTIONAL_NAME!r} line"
        )
        return failures

    # Prefer the most recently written cart that has Tripod
    cart = tripod_carts.sorted("write_date", reverse=True)[0]

    line_names = cart.order_line.mapped("product_template_id.name")
    if MAIN_NAME in line_names:
        failures.append(
            f"Cart still contains a {MAIN_NAME!r} line "
            f"(lines: {line_names}); main product was not removed"
        )

    tripod_lines = cart.order_line.filtered(
        lambda l: l.product_template_id.name == OPTIONAL_NAME
    )
    if len(tripod_lines) != 1:
        failures.append(
            f"Expected exactly 1 {OPTIONAL_NAME!r} line, got {len(tripod_lines)}"
        )
    elif abs(tripod_lines.product_uom_qty - 1.0) > 0.001:
        failures.append(
            f"{OPTIONAL_NAME!r} qty is {tripod_lines.product_uom_qty}, expected 1"
        )

    # No phantom extra products
    extra = [n for n in line_names if n not in {MAIN_NAME, OPTIONAL_NAME}]
    if extra:
        failures.append(f"Cart has unexpected extra lines: {extra}")

    if cart.state != "draft":
        failures.append(f"Cart state is {cart.state!r}, expected 'draft'")

    return failures
