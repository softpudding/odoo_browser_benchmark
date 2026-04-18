"""Seed for crm.create_lead_from_email_alias_log_message.

Hard workflow: configure an Email Alias on an existing CRM team, create a
lead with a specific email_from, then post a chatter message. The Email
Alias field is mid-form (next to the salesperson) under Team Details — the
agent must open the team form rather than a generic settings panel.

We pre-seed the 'Inbound' team *without* the target alias so the alias
write is a genuine state change. The team has use_leads enabled so the
alias controls are visible.
"""

TEAM_NAME = "Inbound"
TARGET_ALIAS = "leads-inbound"
LEAD_NAME = "Inbound Inquiry from Sample"
LEAD_EMAIL = "prospect@external.test"
CHATTER_MESSAGE = "Asked about Bench Pro pricing."
TAG_NAME = "Website"


def setup(env):
    # --- Cleanup prior runs (lead + activities/messages) ---
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", LEAD_NAME),
    ])
    for lead in old_leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
    old_leads.unlink()

    # --- Ensure the 'Inbound' team exists and has use_leads enabled ---
    # Also make sure the alias is NOT already set to the target value so the
    # task requires a real write.
    team = env["crm.team"].with_context(active_test=False).search([
        ("name", "=", TEAM_NAME),
    ], limit=1)
    if not team:
        team = env["crm.team"].create({
            "name": TEAM_NAME,
            "sequence": 10,
            "use_leads": True,
            "use_opportunities": True,
            "company_id": False,
        })
    else:
        update = {}
        if not team.active:
            update["active"] = True
        if not team.use_leads:
            update["use_leads"] = True
        if not team.use_opportunities:
            update["use_opportunities"] = True
        if update:
            team.write(update)

    # Reset the alias if it happens to match our target (clean slate for re-runs)
    if team.alias_name == TARGET_ALIAS:
        team.write({"alias_name": False})

    # Release any lingering alias that might collide with our target so the
    # agent can successfully set 'leads-inbound'. Alias names are unique
    # within a domain.
    other = env["mail.alias"].with_context(active_test=False).search([
        ("alias_name", "=", TARGET_ALIAS),
    ])
    for alias in other:
        if team.alias_id and alias.id == team.alias_id.id:
            continue
        alias.write({"alias_name": False})

    # Ensure a default alias domain is configured so the '@<domain>' shows
    # in the form (otherwise the inline domain field is blank and the agent
    # may get confused).
    if not env["mail.alias.domain"].search([], limit=1):
        env["mail.alias.domain"].create({
            "name": "example.com",
            "bounce_alias": "bounce",
            "catchall_alias": "catchall",
        })

    # Reset alias_contact to 'everyone' so the task's change to 'partners'
    # is a real state diff.
    if team.alias_id and team.alias_id.alias_contact != "everyone":
        team.alias_id.sudo().write({"alias_contact": "everyone"})

    # --- Ensure the 'Website' crm.tag exists (+ distractor tag) ---
    if not env["crm.tag"].search([("name", "=", TAG_NAME)], limit=1):
        env["crm.tag"].create({"name": TAG_NAME})
    # Distractor tag that shares a common prefix in autocomplete so agent
    # must read the exact tag label.
    if not env["crm.tag"].search([("name", "=", "Web-Inquiry")], limit=1):
        env["crm.tag"].create({"name": "Web-Inquiry"})
