"""Seed for product.configure_stock_route_for_product (medium).

Category 5: Deep UI interaction (notebook tab + m2m_checkboxes).

Seeds:
    * Activates the MTO route (``stock.route_warehouse0_mto``). It ships
      with ``active=False`` in a fresh DB — without this the route is
      not visible on the product form.
    * The MTO route's ``product_selectable`` default is True, so once it
      is active the ``has_available_route_ids`` compute flips to True
      and the Operations/Routes group renders on the Inventory tab.
    * Grants admin the ``stock.group_adv_location`` group (routes
      visibility) and ``stock.group_stock_multi_locations`` so the
      route-selection affordances are consistent across product views.
    * Creates a fresh storable product ``Bench MTO Item`` at on-hand=0
      with an EMPTY ``route_ids`` m2m (no routes selected).  The agent
      must switch to the Inventory tab on the product form and tick
      'Replenish on Order (MTO)' in the Routes many2many_checkboxes
      field, then save.

Task difficulty:
    * Tab navigation — Routes m2m_checkboxes is hidden behind the
      Inventory tab of the product form notebook.
    * Specific checkbox pick — among several visible route checkboxes
      (MTO, Buy, Manufacture, etc. depending on installed modules),
      the agent must tick exactly 'Replenish on Order (MTO)' and
      nothing else.
    * No wizard, no dialog — just the m2m_checkboxes widget and Save.
"""

PRODUCT_NAME = "Bench MTO Item"


def _cleanup(env):
    # Drop any lingering product from prior runs so the seed is deterministic.
    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if not products:
        # Also catch template-only leftovers.
        tmpls = env["product.template"].with_context(active_test=False).search(
            [("name", "=", PRODUCT_NAME)]
        )
        for t in tmpls:
            try:
                t.sudo().unlink()
            except Exception:
                try:
                    t.write({"active": False})
                except Exception:
                    pass
        return

    try:
        env["stock.warehouse.orderpoint"].with_context(
            active_test=False
        ).search([("product_id", "in", products.ids)]).unlink()
    except Exception:
        pass
    try:
        env["stock.move.line"].search(
            [("product_id", "in", products.ids)]
        ).sudo().unlink()
    except Exception:
        pass
    try:
        env["stock.move"].search(
            [("product_id", "in", products.ids)]
        ).sudo().unlink()
    except Exception:
        pass
    try:
        env["stock.quant"].with_context(inventory_mode=True).search(
            [("product_id", "in", products.ids)]
        ).sudo().unlink()
    except Exception:
        pass
    try:
        products.mapped("product_tmpl_id").sudo().unlink()
    except Exception:
        for tmpl in products.mapped("product_tmpl_id"):
            try:
                tmpl.write({"active": False})
            except Exception:
                pass


def setup(env):
    _cleanup(env)

    # --- 1. Activate MTO route. Ships with active=False in fresh DBs. ---
    mto_route = env.ref("stock.route_warehouse0_mto")
    if not mto_route.active:
        mto_route.active = True
    # product_selectable default is True, but be explicit in case a
    # prior migration/test clobbered it.
    if not mto_route.product_selectable:
        mto_route.product_selectable = True

    # --- 2. Admin visibility groups for route / multi-location UI. ---
    admin = env.ref("base.user_admin")
    grp_adv = env.ref("stock.group_adv_location", raise_if_not_found=False)
    if grp_adv and admin not in grp_adv.user_ids:
        grp_adv.user_ids = [(4, admin.id)]
    grp_multi = env.ref(
        "stock.group_stock_multi_locations", raise_if_not_found=False
    )
    if grp_multi and admin not in grp_multi.user_ids:
        grp_multi.user_ids = [(4, admin.id)]

    # --- 3. Storable product with NO routes selected. ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 49.0,
        "standard_price": 20.0,
        "sale_ok": True,
        "purchase_ok": True,
        "default_code": "BENCH-MTO-01",
        # Explicitly clear routes so the agent has to tick the MTO
        # checkbox themselves — even if benchmark_base snapshot has
        # altered default route behavior.
        "route_ids": [(5, 0, 0)],
    })

    # Sanity: product was created with an empty route_ids.
    if tmpl.route_ids:
        # Force-clear in case an onchange slipped a default route back in.
        tmpl.write({"route_ids": [(5, 0, 0)]})
    assert not tmpl.route_ids, (
        f"seed: {PRODUCT_NAME} still has routes {tmpl.route_ids.mapped('name')!r}"
    )

    # Sanity: the MTO route must be selectable on products so the
    # agent's checkbox appears.
    assert mto_route.active, "seed: MTO route did not activate"
    assert mto_route.product_selectable, (
        "seed: MTO route is not product_selectable — checkbox will not render"
    )

    env.cr.execute("SELECT 1")
