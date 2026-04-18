"""Cleanup artifacts from prior runs."""

TARGET_NAME = "Bench Hot Lead"
TARGET_NUMBER = "+16175551234"


def cleanup(env):
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ])
    for lead in leads:
        msgs = env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ])
        if "sms.sms" in env.registry:
            env["sms.sms"].sudo().search([
                ("mail_message_id", "in", msgs.ids),
            ]).unlink()
        msgs.sudo().unlink()
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        lead.unlink()

    if "sms.sms" in env.registry:
        env["sms.sms"].sudo().search([("number", "=", TARGET_NUMBER)]).unlink()
