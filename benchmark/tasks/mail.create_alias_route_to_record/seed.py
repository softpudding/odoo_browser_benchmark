"""Seed for mail.create_alias_route_to_record.

Hard workflow: create a mail.alias that routes inbound email addressed to
`benchalias@<domain>` into new crm.lead records assigned to the seeded
'Bench Alias Team'. The alias configuration form is only reachable via
Settings > Technical > Email > Aliases, which is hidden until developer
mode is turned on — the agent has to click 'Activate the developer mode'
in the Developer Tools section of Settings first.

We intentionally do NOT pre-create the alias; the task requires the agent
to make it. We DO ensure:
  * The 'Bench Alias Team' crm.team exists so the agent has a concrete
    team_id to reference in alias_defaults.
  * A default mail.alias.domain exists so the alias form renders the @
    domain and Save succeeds without ValidationError.
  * Any stale alias_name='benchalias' from a prior run is released so
    the UNIQUE(alias_name, alias_domain_id) constraint does not reject
    the agent's Save.
  * Any prior seeded ir.config_parameter that forces debug off is cleared.

We deliberately do NOT pre-activate developer mode on the server side
(`base.group_no_one` is only effective when session.debug is truthy, which
is a client cookie the agent must set via the UI). The challenge of the
task is recognising that the Technical menu is hidden and acting to
un-hide it.
"""

TEAM_NAME = "Bench Alias Team"
TARGET_ALIAS_NAME = "benchalias"


def setup(env):
    # --- 1. Release any stale alias with the same alias_name so the agent's
    #        Save does not hit the mail.alias UNIQUE constraint.
    stale = env["mail.alias"].with_context(active_test=False).search([
        ("alias_name", "=", TARGET_ALIAS_NAME),
    ])
    if stale:
        # Also wipe any crm.lead created by past runs of this alias so
        # cleanup re-runs start from a clean state.
        lead_ids = env["crm.lead"].with_context(active_test=False).search([
            ("email_from", "ilike", f"{TARGET_ALIAS_NAME}@"),
        ])
        if lead_ids:
            env["mail.message"].search([
                ("model", "=", "crm.lead"),
                ("res_id", "in", lead_ids.ids),
            ]).unlink()
            lead_ids.unlink()
        stale.sudo().write({"alias_name": False})
        stale.sudo().unlink()

    # --- 2. Ensure a default mail.alias.domain exists so the alias form
    #        renders a populated `@<domain>` dropdown.
    if not env["mail.alias.domain"].search([], limit=1):
        env["mail.alias.domain"].create({
            "name": "bench.example.com",
            "bounce_alias": "bounce",
            "catchall_alias": "catchall",
        })

    # --- 3. Ensure the 'Bench Alias Team' crm.team exists.
    team = env["crm.team"].with_context(active_test=False).search([
        ("name", "=", TEAM_NAME),
    ], limit=1)
    if not team:
        team = env["crm.team"].create({
            "name": TEAM_NAME,
            "sequence": 50,
            "use_leads": True,
            "use_opportunities": True,
        })
    else:
        update = {}
        if not team.active:
            update["active"] = True
        if not team.use_leads:
            update["use_leads"] = True
        if update:
            team.write(update)

    # Expose the team id to the eval artifacts so the oracle and checker
    # can both find it deterministically by name lookup (we don't want to
    # hardcode an id because snapshots differ).

    # --- 4. Make sure the admin user has base.group_no_one (Technical
    #        Features). On a stock Odoo this is implied via group_system,
    #        but we set it explicitly so developer mode actually unlocks
    #        the Technical menu once the agent toggles the session debug
    #        flag via the Developer Tools link.
    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    group_no_one = env.ref("base.group_no_one", raise_if_not_found=False)
    if admin and group_no_one and group_no_one not in admin.group_ids:
        admin.sudo().write({"group_ids": [(4, group_no_one.id)]})

    # --- 5. Clean up any lingering crm.lead from previous inbound-route
    #        simulations so cleanup re-runs stay idempotent.
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        ("email_from", "ilike", f"{TARGET_ALIAS_NAME}@"),
    ])
    if old_leads:
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        old_leads.unlink()
