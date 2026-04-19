"""Seed for crm.assign_lead_salesperson_change_stage_won.

Medium: one Many2one assignment (Salesperson) plus a stage change via the
form header status bar (Won button). The opportunity starts unassigned
(user_id=False) in the default first stage so the agent must pick Bench Rep
from autocomplete AND click the Won statusbar button — both actions required.
"""

OPP_NAME = "Bench Big Deal"
PARTNER_NAME = "Bench Buyer Co"
PARTNER_EMAIL = "buyer@benchbuyerco.example"
REP_LOGIN = "bench.rep"
REP_NAME = "Bench Rep"
EXPECTED_REVENUE = 50000.0


def setup(env):
    # --- Cleanup prior runs ---
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if old_leads:
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", old_leads.ids),
        ]).unlink()
        old_leads.unlink()

    # --- Ensure Bench Rep user exists (internal user + CRM user group) ---
    rep = env["res.users"].with_context(active_test=False).search([
        ("login", "=", REP_LOGIN),
    ], limit=1)
    group_ids = [
        (4, env.ref("base.group_user").id),
        (4, env.ref("sales_team.group_sale_salesman").id),
    ]
    if not rep:
        rep = env["res.users"].create({
            "name": REP_NAME,
            "login": REP_LOGIN,
            "password": REP_LOGIN,
            "group_ids": group_ids,
        })
    else:
        if rep.name != REP_NAME:
            rep.name = REP_NAME
        if not rep.active:
            rep.write({"active": True})
        # Re-apply groups defensively
        rep.write({"group_ids": group_ids})

    # --- Partner ---
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "email": PARTNER_EMAIL,
        })

    # --- Pick a sensible starting stage (default first, non-won) ---
    first_stage = env["crm.stage"].search(
        [("is_won", "=", False)], order="sequence asc, id asc", limit=1
    )
    if not first_stage:
        first_stage = env["crm.stage"].search([], order="sequence asc, id asc", limit=1)

    # --- Create unassigned opportunity ---
    env["crm.lead"].create({
        "name": OPP_NAME,
        "type": "opportunity",
        "partner_id": partner.id,
        "email_from": PARTNER_EMAIL,
        "user_id": False,
        "stage_id": first_stage.id if first_stage else False,
        "expected_revenue": EXPECTED_REVENUE,
        "probability": 10.0,
        "description": "Unassigned — claim and mark Won.",
    })
