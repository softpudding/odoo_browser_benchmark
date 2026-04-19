"""Seed for purchase.set_vendor_product_code_on_po_line (MEDIUM).

Category: deep_ui_interaction.

Seeds:
- Vendor 'Bench Code Supplier' (supplier_rank=1).
- One consu product 'Bench Widget' with taxes cleared for clean diffs.
- A draft purchase.order with name='BENCH-VCODE' and
  partner_ref='BENCH-VCODE' for Bench Code Supplier, with exactly one
  order line: product=Bench Widget, product_qty=5, taxes cleared. The
  line's Description (`name`) defaults to the product display name
  'Bench Widget' via `_compute_price_unit_and_date_planned_and_name`.

Capability tested: the agent must click into the editable Description
(Text) cell on a purchase.order line and overwrite the auto-filled
product name with `BENCH-WDG-A1 / Bench Widget`. The `name` field is a
COMPUTED Text field with `store=True, readonly=False` — it is writable
but the compute pre-populated it from the product.

Trap: the agent may (a) edit the Product many2one cell instead of the
Description cell, (b) append to (or prepend) the existing description
rather than overwriting it, or (c) confirm the PO after editing, all of
which fail the check.
"""

VENDOR_NAME = "Bench Code Supplier"
PO_NAME = "BENCH-VCODE"
PRODUCT_NAME = "Bench Widget"
PRODUCT_PRICE = 30.0
PRODUCT_QTY = 5


def _cleanup(env):
    # Cleanup vendor bills and POs from prior runs.
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

    # Drop product so re-seeding starts clean.
    prod = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if prod:
        try:
            env["product.supplierinfo"].search([
                ("product_tmpl_id", "=", prod.product_tmpl_id.id),
            ]).unlink()
        except Exception:
            pass
        try:
            prod.mapped("product_tmpl_id").sudo().unlink()
        except Exception:
            pass

    # Drop vendor (last so PO cleanup above still finds it).
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
            "email": "orders@benchcodesupplier.example.com",
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})
    return vendor


def _ensure_product(env):
    prod = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if prod:
        prod.product_tmpl_id.write({
            "list_price": PRODUCT_PRICE,
            "standard_price": PRODUCT_PRICE,
            "purchase_ok": True,
        })
        return prod
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "list_price": PRODUCT_PRICE,
        "standard_price": PRODUCT_PRICE,
        "purchase_ok": True,
        "sale_ok": False,
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    })
    return tmpl.product_variant_id


def setup(env):
    _cleanup(env)

    vendor = _ensure_vendor(env)
    prod = _ensure_product(env)

    po = env["purchase.order"].create({
        "name": PO_NAME,
        "partner_id": vendor.id,
        "partner_ref": PO_NAME,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": prod.id,
        "product_qty": PRODUCT_QTY,
        "price_unit": PRODUCT_PRICE,
        # Let the compute set `name` to the product display name.
        # (Writing it here would mask the "auto-filled" starting state.)
        "tax_ids": [(5, 0, 0)],
    })

    # Sanity: draft, one line, line.name starts as the product name.
    assert po.state == "draft", f"Seed PO in state {po.state}"
    assert len(po.order_line) == 1, (
        f"Seed expected 1 line, got {len(po.order_line)}"
    )
    line = po.order_line
    # `name` is computed from product_id; for a bare product with no
    # translation / no variant description, it should be the product
    # display name (possibly "[code] Name" if a default_code is set —
    # we didn't set one, so it's just "Bench Widget").
    assert PRODUCT_NAME in (line.name or ""), (
        f"Seed expected line.name to contain {PRODUCT_NAME!r}; got {line.name!r}"
    )
    # It must NOT already be the target string (otherwise the task is a
    # no-op and the diff is empty).
    assert "BENCH-WDG-A1" not in (line.name or ""), (
        f"Seed: line.name already contains target code: {line.name!r}"
    )
    assert po.name == PO_NAME, (
        f"Seed PO name is {po.name!r}, expected {PO_NAME!r}"
    )
    env.cr.commit()
