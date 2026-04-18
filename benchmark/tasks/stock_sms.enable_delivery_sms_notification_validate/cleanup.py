"""Cleanup for stock_sms.enable_delivery_sms_notification_validate."""

SO_NAME = "S-BENCH-SMS-001"
TARGET_PHONE = "+16175551234"


def cleanup(env):
    for picking in env["stock.picking"].with_context(active_test=False).search([
        ("origin", "=", SO_NAME),
    ]):
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

    if "sms.sms" in env.registry:
        env["sms.sms"].sudo().search([
            ("number", "=", TARGET_PHONE),
        ]).unlink()

    # Reset company flags so the next run starts clean.
    company = env.company
    company.sudo().write({
        "stock_text_confirmation": False,
        "has_received_warning_stock_sms": False,
    })
