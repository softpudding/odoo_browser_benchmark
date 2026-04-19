"""Seed for account.post_customer_invoice_with_tax_groups (MEDIUM).

Category: deep_ui_interaction.

Seeds:
- Customer partner 'Bench Tax Cust' (customer_rank=1).
- Service product 'Bench Tax Service' (list_price=200.0,
  taxes_id/supplier_taxes_id cleared so no default tax auto-applies on
  the invoice line -- the agent must set the tax explicitly via the
  Taxes many2many_tax_tags cell).
- Two sale taxes (both type_tax_use='sale', amount_type='percent'):
  * 'Bench Sale Tax 10%' (amount=10) -- the distractor.
  * 'Bench Sale Tax 20%' (amount=20) -- the correct one the agent must pick.

The agent must create the invoice from scratch (no pre-existing draft
invoice exists), fill Customer + Invoice Date + one line with the 20%
tax pill (NOT the 10% one), and click Confirm to post.

Trap: the two similarly-named taxes both match 'Bench Sale Tax' as a
prefix in the autocomplete, so the agent must read the percentage
carefully and pick the 20% pill, not the 10% one. This is the
discrimination signal the task tests.
"""

CUSTOMER_NAME = "Bench Tax Cust"
PRODUCT_NAME = "Bench Tax Service"
TAX_10_NAME = "Bench Sale Tax 10%"
TAX_20_NAME = "Bench Sale Tax 20%"


def _cleanup(env):
    """Scrub any lingering records from prior runs."""
    # Drop any invoice for this customer (any state, any move_type out_*).
    customer = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if customer:
        moves = env["account.move"].with_context(active_test=False).search([
            ("partner_id", "=", customer.id),
            ("move_type", "in", ["out_invoice", "out_refund"]),
        ])
        for mv in moves:
            reversals = env["account.move"].search([
                ("reversed_entry_id", "=", mv.id),
            ])
            for rev in reversals:
                if rev.state == "posted":
                    try:
                        rev.button_draft()
                    except Exception:
                        pass
                try:
                    rev.button_cancel()
                except Exception:
                    pass
                try:
                    rev.unlink()
                except Exception:
                    pass
            for line in mv.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                try:
                    line.remove_move_reconcile()
                except Exception:
                    pass
            if mv.state == "posted":
                try:
                    mv.button_draft()
                except Exception:
                    pass
            try:
                mv.button_cancel()
            except Exception:
                pass
            try:
                mv.unlink()
            except Exception:
                pass

    # Drop the product (template) so we can re-seed cleanly with no taxes.
    prod = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if prod:
        try:
            tmpl = prod.product_tmpl_id
            prod.sudo().unlink()
            if tmpl and not tmpl.product_variant_ids:
                tmpl.sudo().unlink()
        except Exception:
            pass

    # Drop taxes.
    taxes = env["account.tax"].with_context(active_test=False).search([
        ("name", "in", [TAX_10_NAME, TAX_20_NAME]),
    ])
    for t in taxes:
        try:
            t.sudo().unlink()
        except Exception:
            pass

    # Drop the customer last.
    if customer:
        try:
            customer.sudo().unlink()
        except Exception:
            pass


def _ensure_customer(env):
    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if not customer:
        customer = env["res.partner"].create({
            "name": CUSTOMER_NAME,
            "is_company": True,
            "customer_rank": 1,
            "email": "ar@benchtaxcust.example.com",
        })
    else:
        customer.write({
            "is_company": True,
            "customer_rank": max(customer.customer_rank, 1),
            "email": "ar@benchtaxcust.example.com",
        })
    return customer


def _ensure_product(env):
    prod = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if prod:
        prod.product_tmpl_id.write({
            "type": "service",
            "list_price": 200.0,
            "standard_price": 200.0,
            "sale_ok": True,
            "purchase_ok": False,
            "invoice_policy": "order",
            "taxes_id": [(5, 0, 0)],
            "supplier_taxes_id": [(5, 0, 0)],
        })
        return prod
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "service",
        "list_price": 200.0,
        "standard_price": 200.0,
        "sale_ok": True,
        "purchase_ok": False,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    })
    return tmpl.product_variant_id


def _ensure_tax(env, name, amount):
    """Create a company-scoped sale tax (percent)."""
    company = env.company
    tax = env["account.tax"].with_context(active_test=False).search([
        ("name", "=", name),
        ("company_id", "=", company.id),
        ("type_tax_use", "=", "sale"),
    ], limit=1)
    if tax:
        tax.write({
            "amount_type": "percent",
            "amount": amount,
            "active": True,
        })
        return tax
    return env["account.tax"].create({
        "name": name,
        "type_tax_use": "sale",
        "amount_type": "percent",
        "amount": amount,
        "company_id": company.id,
    })


def setup(env):
    _cleanup(env)

    _ensure_customer(env)
    _ensure_product(env)
    tax_10 = _ensure_tax(env, TAX_10_NAME, 10.0)
    tax_20 = _ensure_tax(env, TAX_20_NAME, 20.0)

    # Sanity checks.
    assert tax_10.type_tax_use == "sale"
    assert tax_10.amount == 10.0
    assert tax_20.type_tax_use == "sale"
    assert tax_20.amount == 20.0

    env.cr.commit()
