"""Seed for website_sale.add_product_to_cart_checkout_portal.

Seeds:
  * one published shop product 'Bench Portal Product' at 25.00
  * enables + publishes the offline 'Wire Transfer' payment.provider on the
    current website so the /shop/payment step actually renders it

Does NOT seed any sale.order — the agent (or oracle) must create the order
through the public checkout flow. Also cleans up any leftover
'Bench Portal Customer' partner + 'Bench Portal Product' template + related
sale.orders from prior runs.
"""


PRODUCT_NAME = "Bench Portal Product"
CUSTOMER_NAME = "Bench Portal Customer"


def _cleanup(env):
    # Orders first (references partner + product). Cancel non-cancel states
    # so unlink doesn't trip on posted/confirmed constraints.
    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", CUSTOMER_NAME),
    ])
    if partners:
        orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "in", partners.ids),
        ])
        if orders:
            live = orders.filtered(lambda o: o.state not in ("draft", "cancel"))
            if live:
                live.sudo().action_cancel()
            orders.sudo().unlink()
        # Detach any stale cart link before unlinking partners.
        partners.sudo().unlink()

    tmpls = env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ])
    if tmpls:
        # Kill any residual order lines referencing the product (safety net).
        variant_ids = tmpls.mapped("product_variant_ids").ids
        if variant_ids:
            leftover = env["sale.order"].with_context(active_test=False).search([
                ("order_line.product_id", "in", variant_ids),
            ])
            if leftover:
                live = leftover.filtered(lambda o: o.state not in ("draft", "cancel"))
                if live:
                    live.sudo().action_cancel()
                leftover.sudo().unlink()
        tmpls.sudo().unlink()


def setup(env):
    _cleanup(env)

    website = env["website"].search([], limit=1)
    if not website:
        raise RuntimeError("No website record present in DB")

    tmpl_vals = {
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 25.0,
        "is_published": True,
        "taxes_id": [(5, 0, 0)],
        "website_id": False,  # all websites
    }
    # website_published is the historical alias; safe to set both.
    if "website_published" in env["product.template"]._fields:
        tmpl_vals["website_published"] = True
    env["product.template"].create(tmpl_vals)

    # --- Payment provider: enable + publish offline Wire Transfer ---
    # The provider is shipped as XML record `payment.payment_provider_transfer`
    # (code='custom', custom_mode='wire_transfer'). By default it's disabled
    # and unpublished; flip it on for this website so /shop/payment shows it.
    provider = env.ref(
        "payment.payment_provider_transfer", raise_if_not_found=False
    )
    if not provider:
        provider = env["payment.provider"].search([
            ("code", "=", "custom"),
            ("custom_mode", "=", "wire_transfer"),
        ], limit=1)
    if not provider:
        raise RuntimeError(
            "Wire Transfer payment.provider (code='custom', "
            "custom_mode='wire_transfer') not found; ensure payment_custom "
            "module is installed in the benchmark base DB"
        )
    provider_vals = {
        "state": "enabled",
        "is_published": True,
        "company_id": website.company_id.id,
    }
    provider.sudo().write(provider_vals)

    # Make sure no residual cart survives for the admin user either — the
    # public oracle flow will create a brand-new one.
    admin = env.ref("base.user_admin")
    stale_carts = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("state", "=", "draft"),
        ("website_id", "!=", False),
    ])
    for cart in stale_carts:
        cart.sudo().unlink()

    # Sanity checks
    tmpl = env["product.template"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not tmpl:
        raise RuntimeError("Seed sanity failed: product not created")
    if not tmpl.is_published:
        raise RuntimeError("Seed sanity failed: product not published")
    if abs(tmpl.list_price - 25.0) > 0.01:
        raise RuntimeError(
            f"Seed sanity failed: product list_price {tmpl.list_price}, expected 25.0"
        )
    if provider.state != "enabled":
        raise RuntimeError(
            f"Seed sanity failed: wire transfer provider state is {provider.state}"
        )
