"""Cleanup for mail.create_alias_route_to_record."""


TEAM_NAME = "Bench Alias Team"
TARGET_ALIAS_NAME = "benchalias"


def cleanup(env):
    # Remove any crm.lead produced by earlier inbound-route simulations
    # (emails addressed to benchalias@...).
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        ("email_from", "ilike", f"{TARGET_ALIAS_NAME}@"),
    ])
    if old_leads:
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        old_leads.unlink()

    # Release and unlink every mail.alias with our target alias_name.
    aliases = env["mail.alias"].with_context(active_test=False).search([
        ("alias_name", "=", TARGET_ALIAS_NAME),
    ])
    if aliases:
        aliases.sudo().write({"alias_name": False})
        aliases.sudo().unlink()
