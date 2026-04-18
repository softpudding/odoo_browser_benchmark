"""Seed for website_sale_wishlist.add_product_share_to_email.

Installs ``website_sale_wishlist`` (auto-installs with website_sale in most
base snapshots, but we ensure it's present) and creates a single published
product ``Bench Wishlist Item`` so the agent has something to heart-click
on ``/shop``.

DEVIATION NOTE
--------------
The original backlog description called for a "Share via email" dialog on
``/shop/wishlist``. ``website_sale_wishlist`` in Odoo 19 Community exposes
NO share feature (no share controller, no share template, no share JS).
The task is re-scoped to wishlist persistence: verify a ``product.wishlist``
row is created with ``partner_id = admin.partner_id`` referencing the
product on the active website.
"""


PRODUCT_NAME = "Bench Wishlist Item"
LIST_PRICE = 25.0


def _ensure_wishlist_module(env):
    mod = env["ir.module.module"].search(
        [("name", "=", "website_sale_wishlist")], limit=1
    )
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup(env):
    admin = env.ref("base.user_admin")
    # Drop any prior wishlist rows referencing our seeded product
    # (by product name) or owned by admin on any website.
    tmpl = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1,
    )
    if tmpl:
        variants = tmpl.product_variant_ids
        if variants:
            env["product.wishlist"].with_context(active_test=False).sudo().search(
                [("product_id", "in", variants.ids)]
            ).unlink()
        tmpl.sudo().unlink()

    # Also clear admin-owned wishlist rows from a prior run so counts are
    # deterministic (they should have been caught by the template unlink
    # above, but be defensive).
    env["product.wishlist"].with_context(active_test=False).sudo().search(
        [("partner_id", "=", admin.partner_id.id)]
    ).unlink()


def setup(env):
    _ensure_wishlist_module(env)
    _cleanup(env)

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": LIST_PRICE,
        "is_published": True,
        "website_published": True,
        "taxes_id": [(5, 0, 0)],
    })

    # Sanity: must have a website to render /shop.
    if not env["website"].search([], limit=1):
        raise RuntimeError("No website record present in DB; cannot run shop test")

    env.cr.execute("SELECT 1")  # flush
