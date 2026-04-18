"""Seed for sale_purchase.update_pol_alternative_vendor_compare.

Category 2 (HARD, policy/wizard trap):
    - The agent must add TWO alternative RFQs to an existing draft RFQ via the
      "Create Alternative" wizard, override the unit price on each alternative,
      then open the bespoke "Compare Product Lines" view (custom js_class
      list view), use the per-row "Choose" bullseye action to clear competing
      quantities, and finally confirm the chosen RFQ via the
      "What about the alternative Requests for Quotations?" warning dialog
      using the non-default "Cancel Alternatives" branch.

This seed:
    1. Ensures the ``purchase_requisition`` module is installed (it is NOT in
       the base snapshot — it ships the alternative-RFQ feature + the
       Compare Product Lines list view).
    2. Grants the admin user the "Manage Purchase Alternatives" group so the
       Alternatives tab and Create Alternative button are visible on the PO
       form.
    3. Creates / refreshes three vendor partners (Atlas Industrial,
       Beacon Mechanical, Crestline Equipment).
    4. Creates a consu product "Industrial Compressor".
    5. Creates a draft RFQ R-BENCH-ALT-001 for Atlas Industrial with one
       line: 10 × Industrial Compressor @ 120.00 (taxes cleared).
"""


VENDOR_A = "Atlas Industrial"
VENDOR_B = "Beacon Mechanical"
VENDOR_C = "Crestline Equipment"
PRODUCT_NAME = "Industrial Compressor"
RFQ_REF = "R-BENCH-ALT-001"
QTY = 10
PRICE_A = 120.0


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _ensure_vendor(env, name, email):
    p = env["res.partner"].search([("name", "=", name)], limit=1)
    if not p:
        p = env["res.partner"].create({
            "name": name,
            "email": email,
            "supplier_rank": 1,
            "is_company": True,
        })
    else:
        p.write({"supplier_rank": max(p.supplier_rank, 1)})
    return p


def _cleanup(env, vendors):
    """Wipe POs from any prior run so the agent always starts clean."""
    # By origin
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("origin", "=", RFQ_REF),
    ])
    # Also any PO for our three vendors that might be linked via group
    for v in vendors:
        pos |= env["purchase.order"].with_context(active_test=False).search([
            ("partner_id", "=", v.id),
        ])

    # Cancel related pickings + draft state walk before unlink
    for po in pos:
        for picking in po.picking_ids:
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
                except Exception:
                    pass
        if po.state in ("purchase", "done"):
            try:
                po.button_cancel()
            except Exception:
                pass
        if po.state == "cancel":
            try:
                po.button_draft()
            except Exception:
                pass
        try:
            po.unlink()
        except Exception:
            # Last-ditch: detach from any group then delete
            try:
                po.purchase_group_id = False
                po.unlink()
            except Exception:
                pass

    # Stranded purchase.order.group records (POs deleted but group lingered)
    stale_groups = env["purchase.order.group"].search([])
    for g in stale_groups:
        if not g.order_ids:
            try:
                g.unlink()
            except Exception:
                pass


def setup(env):
    _ensure_module(env, "purchase_requisition")

    # The Alternatives tab is hidden behind this group.
    grp = env.ref(
        "purchase_requisition.group_purchase_alternatives", raise_if_not_found=False
    )
    if grp:
        admin = env.ref("base.user_admin")
        if admin not in grp.user_ids:
            grp.user_ids = [(4, admin.id)]

    vendor_a = _ensure_vendor(env, VENDOR_A, "sales@atlas.example.com")
    vendor_b = _ensure_vendor(env, VENDOR_B, "orders@beacon.example.com")
    vendor_c = _ensure_vendor(env, VENDOR_C, "rfq@crestline.example.com")

    # Product
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 200.0,
            "standard_price": PRICE_A,
            "purchase_method": "purchase",
        })
        product = tmpl.product_variant_id
    # Clear taxes so the totals match the prompt exactly.
    product.product_tmpl_id.write({
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    })

    _cleanup(env, vendor_a + vendor_b + vendor_c)

    po = env["purchase.order"].create({
        "partner_id": vendor_a.id,
        "origin": RFQ_REF,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": product.id,
        "product_qty": QTY,
        "price_unit": PRICE_A,
        "tax_ids": [(5, 0, 0)],
        "name": PRODUCT_NAME,
    })
