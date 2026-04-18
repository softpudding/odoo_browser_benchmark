"""Seed for stock_sms.enable_delivery_sms_notification_validate.

Category (MEDIUM): side_effect_trap — settings toggle with downstream SMS emission
on validate.

Creates:
  * Partner 'Bench SMS Customer' with country_id=base.us, phone='+16175551234'
    (valid US E.164 so `_phone_format` sanitizes to itself).
  * Storable product 'Bench SMS Item' with on-hand stock of 10.
  * A confirmed outgoing stock.picking linked to sale.order 'S-BENCH-SMS-001'
    (so the picking's `origin` shows the S-BENCH-SMS-001 reference the prompt
    references). The picking has move quantities already pushed to reserved
    so that button_validate doesn't open a nothing-to-transfer / backorder
    wizard — only the stock_sms confirmation wizard can appear.

Module install:
  * `sms` and `stock_sms` are NOT in base; seed installs `sms` which
    auto-installs `stock_sms` (stock_sms has auto_install=True with depends
    on stock + sms).

Settings reset:
  * `stock_sms.__init__._assign_default_sms_template_picking_id` post_init
    hook flips `res.company.stock_text_confirmation=True` on install if the
    template exists. We explicitly reset it to False AFTER install so the
    agent has to toggle it on through the UI.
  * `has_received_warning_stock_sms` is reset to False so the first validate
    triggers the SMS warning wizard (the expected UX path).
"""

TARGET_PARTNER = "Bench SMS Customer"
TARGET_PHONE = "+16175551234"
TARGET_EMAIL = "sms-customer@benchstock.example"
SO_NAME = "S-BENCH-SMS-001"
PRODUCT_NAME = "Bench SMS Item"


def _ensure_modules(env):
    """Install `sms` if not installed. `stock_sms` auto-installs when both
    `stock` (base) and `sms` are installed."""
    for mod_name in ("sms", "stock_sms"):
        mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
        if mod and mod.state != "installed":
            mod.button_immediate_install()


def _cleanup(env):
    # Pickings sourced from the target SO name (origin)
    for picking in env["stock.picking"].with_context(active_test=False).search([
        ("origin", "=", SO_NAME),
    ]):
        # Unlink any sms.sms linked through the picking's messages
        if "sms.sms" in env.registry:
            msgs = env["mail.message"].search([
                ("model", "=", "stock.picking"),
                ("res_id", "=", picking.id),
            ])
            env["sms.sms"].sudo().search([
                ("mail_message_id", "in", msgs.ids),
            ]).unlink()
            msgs.sudo().unlink()
        if picking.state not in ("done", "cancel"):
            picking.action_cancel()
        picking.unlink()

    # SO
    for so in env["sale.order"].with_context(active_test=False).search([
        ("name", "=", SO_NAME),
    ]):
        for picking in so.picking_ids:
            if picking.state not in ("done", "cancel"):
                picking.action_cancel()
            picking.unlink()
        if so.state in ("sale", "done"):
            so._action_cancel()
        so.unlink()

    # Stray sms.sms from prior runs
    if "sms.sms" in env.registry:
        env["sms.sms"].sudo().search([
            ("number", "=", TARGET_PHONE),
        ]).unlink()

    # Product + partner are reused across runs — don't delete.


def setup(env):
    _ensure_modules(env)
    _cleanup(env)

    # --- Reset the company's stock SMS settings so the agent must toggle ---
    company = env.company
    company.sudo().write({
        "stock_text_confirmation": False,
        "stock_confirmation_type": "sms",
        "has_received_warning_stock_sms": False,
    })

    # --- Partner (US E.164 for clean phone sanitization) ---
    us_country = env.ref("base.us", raise_if_not_found=False)
    partner = env["res.partner"].search(
        [("name", "=", TARGET_PARTNER)], limit=1
    )
    vals = {
        "name": TARGET_PARTNER,
        "email": TARGET_EMAIL,
        "phone": TARGET_PHONE,
    }
    if us_country:
        vals["country_id"] = us_country.id
    if not partner:
        partner = env["res.partner"].create(vals)
    else:
        partner.write(vals)

    # --- Product with on-hand stock ---
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1,
    )
    if not product:
        product_tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "is_storable": True,
            "list_price": 20.0,
            "standard_price": 10.0,
        })
        product_tmpl.write({"taxes_id": [(5, 0, 0)]})
        product = product_tmpl.product_variant_id

    # Seed on-hand stock (idempotent: delta to target 10 units at WH/Stock)
    current_qty = env["stock.quant"]._get_available_quantity(product, stock_loc)
    needed = 10.0 - current_qty
    if needed > 0.01:
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": product.id,
            "location_id": stock_loc.id,
            "inventory_quantity": 10.0,
        }).action_apply_inventory()

    # --- Sale order → confirmed → picking ---
    so = env["sale.order"].create({
        "name": SO_NAME,
        "partner_id": partner.id,
        "order_line": [(0, 0, {
            "product_id": product.id,
            "name": PRODUCT_NAME,
            "product_uom_qty": 2,
            "price_unit": 20.0,
            "tax_ids": [(5, 0, 0)],
        })],
    })
    so.action_confirm()

    # Reserve + push qty_done so Validate doesn't open transfer wizard
    for picking in so.picking_ids:
        picking.action_assign()
        for move in picking.move_ids:
            if move.state in ("confirmed", "partially_available", "assigned"):
                move.write({
                    "quantity": move.product_uom_qty,
                    "picked": True,
                })
