"""Postconditions for stock_sms.enable_delivery_sms_notification_validate.

Validates:
1. `res.company.stock_text_confirmation` is now True on the admin user's company
   (the agent toggled the feature on via Inventory settings).
2. The S-BENCH-SMS-001 delivery picking exists and reached state=done.
3. Exactly one sms.sms record exists with the customer's phone (+16175551234)
   and body referencing the picking (i.e., containing 'S-BENCH-SMS-001').
4. That sms.sms is linked via mail.message to the picking record (model=
   stock.picking, res_id=picking.id, message_type='sms').

Notes on the `sms.sms.state` field:
  IAP SMS delivery fails on a machine without IAP credits and flips state
  from 'outgoing' to 'error'. check.py ignores state; the persistence of
  the record + body + number + linkage is what proves the validate path ran
  with SMS on.
"""

SO_NAME = "S-BENCH-SMS-001"
TARGET_PHONE = "+16175551234"


def check(env):
    failures = []

    # 1. Company flag
    company = env.company
    if not company.stock_text_confirmation:
        failures.append(
            "res.company.stock_text_confirmation is still False — "
            "the Text Confirmation setting was not enabled."
        )
    if company.stock_confirmation_type != "sms":
        failures.append(
            f"res.company.stock_confirmation_type is "
            f"{company.stock_confirmation_type!r}, expected 'sms'."
        )

    # 2. Picking
    picking = env["stock.picking"].search([
        ("origin", "=", SO_NAME),
        ("picking_type_code", "=", "outgoing"),
    ], limit=1)
    if not picking:
        return failures + [
            f"Outgoing picking with origin {SO_NAME!r} not found."
        ]
    if picking.state != "done":
        failures.append(
            f"Picking {SO_NAME} state={picking.state!r}, expected 'done' "
            "(agent must click Validate)."
        )

    # 3. sms.sms record with customer phone
    if "sms.sms" not in env.registry:
        return failures + ["sms.sms model not registered — sms module missing."]

    sms_recs = env["sms.sms"].sudo().search([
        ("number", "=", TARGET_PHONE),
    ])
    if not sms_recs:
        return failures + [
            f"No sms.sms record found with number {TARGET_PHONE} — "
            "validating the picking did not trigger the SMS side effect."
        ]

    # Body must mention the picking origin to confirm it came from the
    # stock_sms delivery template (which includes `object.origin`).
    matching = sms_recs.filtered(
        lambda s: SO_NAME in (s.body or "")
    )
    if not matching:
        bodies = [f"id={s.id}: body={s.body!r}" for s in sms_recs]
        return failures + [
            f"No sms.sms record with body referencing {SO_NAME}. "
            "Existing: " + "; ".join(bodies)
        ]

    if len(matching) > 1:
        failures.append(
            f"Expected exactly 1 sms.sms for {SO_NAME}, "
            f"found {len(matching)} (agent may have validated twice)."
        )

    sms = matching[0]

    # 4. mail.message linkage
    if not sms.mail_message_id:
        failures.append(
            "sms.sms has no mail_message_id — SMS was not posted on the picking."
        )
    else:
        msg = sms.mail_message_id
        if msg.model != "stock.picking":
            failures.append(
                f"mail.message.model is {msg.model!r}, expected 'stock.picking'."
            )
        if msg.res_id != picking.id:
            failures.append(
                f"mail.message.res_id is {msg.res_id}, expected {picking.id} "
                f"(picking {SO_NAME})."
            )
        if msg.message_type != "sms":
            failures.append(
                f"mail.message.message_type is {msg.message_type!r}, "
                "expected 'sms'."
            )

    return failures
