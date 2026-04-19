"""Seed for purchase.add_product_to_rfq_with_taxes (MEDIUM).

Category: deep_ui_interaction.

Seeds:
- Vendor 'Bench Tax Vendor' (supplier_rank=1).
- Product 'Bench Other Item' (the pre-existing line's product; no
  taxes, qty=2 on the seeded line).
- Product 'Bench Taxable Item' (the product the agent adds; list_price
  50.0, taxes cleared on the template so default tax doesn't
  auto-apply — the agent must set it explicitly via the Taxes column).
- Purchase tax 'Bench Tax 5%' with type_tax_use='purchase',
  amount_type='percent', amount=5 (company-default).
- Draft purchase.order name='BENCH-ADD-TAX', partner_ref='BENCH-ADD-TAX'
  for Bench Tax Vendor, with exactly one pre-existing line
  (Bench Other Item, product_qty=2, tax_ids cleared).

Capability tested: agent must click 'Add a product' on the Products
tab (inline o2m Add), pick Bench Taxable Item in the new row, set qty
to 3, and then set the Taxes column to the 'Bench Tax 5%' tag via the
many2many_tax_tags widget (autocomplete pill). Saving persists the new
line with tax_ids containing Bench Tax 5% and the existing line
untouched.

Trap: the agent may edit the EXISTING line's Taxes column instead of
adding a new line (row 450 pattern), or may add the line without
setting the tax, or may confirm the PO after saving. All three fail
the check.
"""

VENDOR_NAME = "Bench Tax Vendor"
PO_NAME = "BENCH-ADD-TAX"
PRODUCT_EXISTING = "Bench Other Item"
PRODUCT_NEW = "Bench Taxable Item"
PRODUCT_NEW_PRICE = 50.0
PRODUCT_EXISTING_QTY = 2
TAX_NAME = "Bench Tax 5%"


def _cleanup(env):
    """Scrub any lingering records from prior runs."""
    pos = env["purchase.order"].with_context(active_test=False).search([
        "|",
        ("name", "=", PO_NAME),
        ("partner_ref", "=", PO_NAME),
    ])
    for po in pos:
        for bill in po.invoice_ids:
            try:
                if bill.state == "posted":
                    bill.button_draft()
                bill.button_cancel()
                bill.unlink()
            except Exception:
                pass
        for p in po.picking_ids:
            if p.state not in ("done", "cancel"):
                try:
                    p.action_cancel()
                except Exception:
                    pass
            try:
                p.move_ids.write({"state": "cancel"})
                p.write({"state": "cancel"})
                p.unlink()
            except Exception:
                pass
        try:
            if po.state in ("purchase", "done"):
                po.button_cancel()
            po.unlink()
        except Exception:
            pass

    # Sweep any PO whose partner is our vendor (defensive).
    vendor = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if vendor:
        extra = env["purchase.order"].with_context(active_test=False).search([
            ("partner_id", "=", vendor.id),
        ])
        for po in extra:
            try:
                if po.state in ("purchase", "done"):
                    po.button_cancel()
                po.unlink()
            except Exception:
                pass

    # Drop products so re-seeding starts clean.
    prods = env["product.product"].with_context(active_test=False).search(
        [("name", "in", [PRODUCT_EXISTING, PRODUCT_NEW])]
    )
    if prods:
        try:
            env["product.supplierinfo"].search([
                ("product_tmpl_id", "in", prods.mapped("product_tmpl_id").ids),
            ]).unlink()
        except Exception:
            pass
        try:
            prods.mapped("product_tmpl_id").sudo().unlink()
        except Exception:
            pass

    # Drop the tax so we get a clean re-seed (and avoid name collisions).
    tax = env["account.tax"].with_context(active_test=False).search([
        ("name", "=", TAX_NAME),
    ])
    for t in tax:
        try:
            t.sudo().unlink()
        except Exception:
            pass

    # Drop vendor last.
    if vendor:
        try:
            vendor.sudo().unlink()
        except Exception:
            pass


def _ensure_vendor(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "orders@benchtaxvendor.example.com",
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})
    return vendor


def _ensure_product(env, name, price):
    prod = env["product.product"].search([("name", "=", name)], limit=1)
    if prod:
        prod.product_tmpl_id.write({
            "list_price": price,
            "standard_price": price,
            "purchase_ok": True,
            "taxes_id": [(5, 0, 0)],
            "supplier_taxes_id": [(5, 0, 0)],
        })
        return prod
    tmpl = env["product.template"].create({
        "name": name,
        "type": "consu",
        "list_price": price,
        "standard_price": price,
        "purchase_ok": True,
        "sale_ok": False,
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    })
    return tmpl.product_variant_id


def _ensure_tax(env):
    """Create a company-scoped purchase tax 'Bench Tax 5%' (percent, 5%)."""
    company = env.company
    tax = env["account.tax"].with_context(active_test=False).search([
        ("name", "=", TAX_NAME),
        ("company_id", "=", company.id),
        ("type_tax_use", "=", "purchase"),
    ], limit=1)
    if tax:
        tax.write({
            "amount_type": "percent",
            "amount": 5.0,
            "active": True,
        })
        return tax
    return env["account.tax"].create({
        "name": TAX_NAME,
        "type_tax_use": "purchase",
        "amount_type": "percent",
        "amount": 5.0,
        "company_id": company.id,
    })


def setup(env):
    _cleanup(env)

    vendor = _ensure_vendor(env)
    prod_existing = _ensure_product(env, PRODUCT_EXISTING, 10.0)
    _ensure_product(env, PRODUCT_NEW, PRODUCT_NEW_PRICE)
    tax = _ensure_tax(env)

    po = env["purchase.order"].create({
        "name": PO_NAME,
        "partner_id": vendor.id,
        "partner_ref": PO_NAME,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": prod_existing.id,
        "product_qty": PRODUCT_EXISTING_QTY,
        "price_unit": 10.0,
        "name": PRODUCT_EXISTING,
        "tax_ids": [(5, 0, 0)],  # no taxes on the pre-existing line
    })

    # Sanity
    assert po.state == "draft", f"Seed PO in state {po.state}"
    assert len(po.order_line) == 1, (
        f"Seed expected 1 line, got {len(po.order_line)}"
    )
    assert po.order_line.product_id.id == prod_existing.id
    assert po.order_line.product_qty == PRODUCT_EXISTING_QTY
    assert not po.order_line.tax_ids, (
        f"Seed expected no taxes on pre-existing line, got {po.order_line.tax_ids}"
    )
    assert tax.type_tax_use == "purchase"
    assert tax.amount == 5.0
    assert tax.amount_type == "percent"
    env.cr.commit()
