"""Seed CRM leads for the convert-lead-qualify task.

Category 2 (MEDIUM): the agent must open the CRM Leads view, find the correct
lead among a near-duplicate, complete the default conversion wizard, and move
the result to the Qualified stage.
"""

LEAD_NAME = "Silver Maple Network Refresh"
LEAD_EMAIL = "ops+netops@silvermaple.example.com"
DISTRACTOR_NAME = "Silver Maple Network Review"
DISTRACTOR_EMAIL = "ops+review@silvermaple.example.com"


def _cleanup_leads(env, names):
    leads = env["crm.lead"].search([("name", "in", names)])
    for lead in leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        lead.unlink()


def _ensure_stage(env, name, sequence):
    stage = env["crm.stage"].search([("name", "=", name)], limit=1)
    if not stage:
        stage = env["crm.stage"].create({
            "name": name,
            "sequence": sequence,
        })
    return stage


def setup(env):
    _cleanup_leads(env, [LEAD_NAME, DISTRACTOR_NAME])

    _ensure_stage(env, "New", 1)
    _ensure_stage(env, "Qualified", 20)
    _ensure_stage(env, "Proposition", 30)

    env["crm.lead"].create({
        "name": LEAD_NAME,
        "type": "lead",
        "contact_name": "Morgan Rivera",
        "email_from": LEAD_EMAIL,
        "phone": "+1 206 555 0108",
        "expected_revenue": 9000.0,
        "description": "Refresh aging access-layer switches before summer rollout.",
    })

    env["crm.lead"].create({
        "name": DISTRACTOR_NAME,
        "type": "lead",
        "contact_name": "Morgan Rivers",
        "email_from": DISTRACTOR_EMAIL,
        "phone": "+1 206 555 0199",
        "expected_revenue": 9000.0,
        "description": "Review the current switching layout for next quarter.",
    })
