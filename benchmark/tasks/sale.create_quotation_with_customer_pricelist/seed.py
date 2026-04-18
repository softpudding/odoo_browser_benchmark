"""Seed for sale.create_quotation_with_customer_pricelist.

Category: deep_ui_interaction (MEDIUM).

Sets up:
- Enables the `product.group_product_pricelist` group on the admin user so the
  Pricelist field is visible on the sale.order form.
- Creates a `VIP 20% Off` pricelist with a single rule: 20% off sales price
  on all products.
- Creates customer `Bench Premium Co` with that pricelist assigned
  (property_product_pricelist) so a new SO auto-applies it.
- Creates a distractor customer `Bench Regular Co` with no pricelist.
- Creates product `Bench Standard Widget` with list_price=100, no taxes
  (clean 20% discount math: 80.00 unit price).
"""


def setup(env):
    # --- Enable the pricelist feature/group ---
    # `product.pricelist._get_partner_pricelist_multi` short-circuits to an
    # empty result if `product.group_product_pricelist` is not enabled on
    # SUPERUSER (see `_is_feature_enabled`). Grant the group to both the
    # admin user AND user_root so the partner→pricelist computation works
    # at seed-time AND the Pricelist field is visible on the SO form.
    admin = env.ref("base.user_admin")
    root = env.ref("base.user_root")
    pricelist_group = env.ref("product.group_product_pricelist")
    to_add = [(4, admin.id), (4, root.id)]
    pricelist_group.sudo().write({"user_ids": to_add})

    # --- Cleanup prior runs: child-first order ---
    for customer_name in ("Bench Premium Co", "Bench Regular Co"):
        partner = env["res.partner"].with_context(active_test=False).search(
            [("name", "=", customer_name)], limit=1
        )
        if partner:
            old_orders = env["sale.order"].with_context(active_test=False).search([
                ("partner_id", "=", partner.id),
            ])
            for order in old_orders:
                if order.state == "sale":
                    order.action_cancel()
                order.sudo().unlink()

    # Cleanup old pricelist (detach from any partners first)
    old_pricelist = env["product.pricelist"].with_context(active_test=False).search(
        [("name", "=", "VIP 20% Off")]
    )
    if old_pricelist:
        # Clear partner property references
        partners_with = env["res.partner"].with_context(active_test=False).search([
            ("specific_property_product_pricelist", "in", old_pricelist.ids),
        ])
        for p in partners_with:
            p.sudo().write({"specific_property_product_pricelist": False})
        old_pricelist.sudo().unlink()

    # Cleanup old product
    old_product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", "Bench Standard Widget")]
    )
    if old_product:
        old_product.mapped("product_tmpl_id").sudo().unlink()

    # --- Create pricelist with 20%-off rule ---
    pricelist = env["product.pricelist"].create({
        "name": "VIP 20% Off",
        "active": True,
        "item_ids": [(0, 0, {
            "applied_on": "3_global",  # all products
            "compute_price": "percentage",
            "percent_price": 20.0,
            "base": "list_price",
        })],
    })

    # --- Create product ---
    tmpl = env["product.template"].create({
        "name": "Bench Standard Widget",
        "type": "consu",
        "list_price": 100.0,
        "taxes_id": [(5, 0, 0)],  # no customer taxes → clean math
    })
    product = tmpl.product_variant_id
    # Also clear any supplier taxes
    product.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]

    # --- Create customers ---
    premium = env["res.partner"].create({
        "name": "Bench Premium Co",
        "email": "premium@bench.example.com",
    })
    # `specific_property_product_pricelist` is the actual storage field
    # (company-dependent) used by `_get_partner_pricelist_multi` to compute
    # `property_product_pricelist`. Setting the non-stored field directly
    # is unreliable at create-time, so write the storage field explicitly.
    premium.with_company(env.company).write({
        "specific_property_product_pricelist": pricelist.id,
    })
    # Sanity-check: the compute should now resolve to our pricelist.
    assert premium.property_product_pricelist.id == pricelist.id, (
        f"Seed: Bench Premium Co did not inherit the VIP pricelist "
        f"(got {premium.property_product_pricelist})"
    )

    env["res.partner"].create({
        "name": "Bench Regular Co",
        "email": "regular@bench.example.com",
    })
