"""Seed for crm_sms.send_sms_to_opportunity.

Category (MEDIUM): side_effect_trap via cross-module cog Actions menu.

Creates a crm.lead opportunity 'Bench Hot Lead' with a partner having
phone '+16175551234'. Requires crm_sms + sms to be installed so that
the form's cog Actions menu exposes the 'Send SMS' wizard binding.

Calibration: SMS sending calls IAP which will fail (no credits) and
mark records as state='error', but the sms.sms record is still
persisted with body/number/mail_message_id. check.py validates the
persisted record, NOT the transport outcome, so no IAP stub is needed.
"""

TARGET_NAME = "Bench Hot Lead"
TARGET_PARTNER = "Bench Hot Prospect"
TARGET_EMAIL = "hotlead@benchprospect.example"
TARGET_PHONE = "+16175551234"  # valid US E.164; prompt uses "+1 617-555-1234"


def _ensure_modules(env):
    """Install sms and crm_sms if not installed (not in base snapshot)."""
    for mod_name in ("sms", "crm_sms"):
        mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
        if mod and mod.state != "installed":
            mod.button_immediate_install()


def setup(env):
    _ensure_modules(env)

    # --- Cleanup prior runs ---
    # Delete any prior sms.sms linked via mail.message to the target lead
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ])
    for lead in old_leads:
        msgs = env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ])
        # Delete linked sms.sms first
        env["sms.sms"].sudo().search([
            ("mail_message_id", "in", msgs.ids),
        ]).unlink()
        msgs.sudo().unlink()
        # Delete mail.activity if any
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        lead.unlink()

    # Clean any stray sms.sms with our target number from prior runs
    env["sms.sms"].sudo().search([("number", "=", TARGET_PHONE)]).unlink()

    # --- Ensure partner ---
    # Use US country so _phone_format produces the expected E.164 number
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

    # --- Ensure CRM stage ---
    stage = env["crm.stage"].search([("name", "=", "Qualified")], limit=1)
    if not stage:
        stage = env["crm.stage"].search([], order="sequence", limit=1)

    sales_team = env["crm.team"].search([], limit=1)
    admin = env.ref("base.user_admin")

    env["crm.lead"].create({
        "name": TARGET_NAME,
        "partner_id": partner.id,
        "partner_name": TARGET_PARTNER,
        "email_from": TARGET_EMAIL,
        "phone": TARGET_PHONE,
        "type": "opportunity",
        "stage_id": stage.id if stage else False,
        "expected_revenue": 12000.0,
        "probability": 40.0,
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id,
        "description": "Hot inbound inquiry — follow up ASAP.",
    })
