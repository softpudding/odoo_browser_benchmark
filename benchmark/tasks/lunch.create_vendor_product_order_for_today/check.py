"""Postcondition checks for lunch.create_vendor_product_order_for_today.

Validates:
1. Vendor 'Bench Cafe' exists with delivery='delivery' and Mon-Fri on.
2. Product 'Veggie Wrap' exists, price 8.00, linked to 'Bench Cafe',
   category Sandwich.
3. A lunch.order for admin today exists with product=Veggie Wrap,
   quantity=1, note='no onions', state in {'ordered','sent','confirmed'}
   (i.e. NOT 'new' and NOT 'cancelled').
"""

from odoo import fields

VENDOR_NAME = "Bench Cafe"
PRODUCT_NAME = "Veggie Wrap"


def check(env):
    failures = []
    admin = env.ref("base.user_admin")

    # ---- Vendor ----
    vendor = env["lunch.supplier"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        return [f"lunch.supplier '{VENDOR_NAME}' not found"]
    if not vendor.active:
        failures.append(f"Vendor '{VENDOR_NAME}' was archived")
    if vendor.delivery != "delivery":
        failures.append(
            f"Vendor '{VENDOR_NAME}' delivery is '{vendor.delivery}', "
            "expected 'delivery'"
        )
    for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
        if not vendor[day]:
            failures.append(
                f"Vendor '{VENDOR_NAME}' weekday '{day}' is False; "
                "expected Mon-Sun all True"
            )

    # ---- Product ----
    product = env["lunch.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return failures + [f"lunch.product '{PRODUCT_NAME}' not found"]
    if not product.active:
        failures.append(f"Product '{PRODUCT_NAME}' was archived")
    if product.supplier_id != vendor:
        failures.append(
            f"Product '{PRODUCT_NAME}' supplier is "
            f"'{product.supplier_id.name}', expected '{VENDOR_NAME}'"
        )
    if abs(product.price - 8.0) > 0.005:
        failures.append(
            f"Product '{PRODUCT_NAME}' price is {product.price}, "
            "expected 8.0"
        )
    if not product.category_id or product.category_id.name != "Sandwich":
        failures.append(
            f"Product '{PRODUCT_NAME}' category is "
            f"'{product.category_id.name if product.category_id else None}', "
            "expected 'Sandwich'"
        )

    # ---- Order ----
    # Tolerate +/- 1 day slippage between the admin's context_today
    # (tz-aware) and the backend's UTC date, which can cross midnight
    # mid-run.
    from datetime import timedelta
    today = fields.Date.context_today(admin)
    date_candidates = [today, today - timedelta(days=1), today + timedelta(days=1)]
    order = env["lunch.order"].with_context(active_test=False).search(
        [
            ("user_id", "=", admin.id),
            ("product_id", "=", product.id),
            ("date", "in", date_candidates),
            ("active", "=", True),
        ],
        limit=1,
        order="id desc",
    )
    if not order:
        failures.append(
            f"lunch.order for admin with product '{PRODUCT_NAME}' "
            f"around {today} not found"
        )
        return failures

    if abs(order.quantity - 1.0) > 0.005:
        failures.append(
            f"Order quantity is {order.quantity}, expected 1"
        )
    if (order.note or "").strip() != "no onions":
        failures.append(
            f"Order note is '{order.note}', expected 'no onions'"
        )
    if order.state == "new":
        failures.append(
            "Order is still in state 'new' -- expected to have clicked "
            "'Order Now' to move state to 'ordered' or later"
        )
    if order.state == "cancelled":
        failures.append("Order was cancelled")
    if order.state not in ("ordered", "sent", "confirmed"):
        failures.append(
            f"Order state is '{order.state}', expected one of "
            "('ordered', 'sent', 'confirmed')"
        )

    return failures
