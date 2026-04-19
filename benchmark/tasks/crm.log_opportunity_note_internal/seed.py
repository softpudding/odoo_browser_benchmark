"""Seed an opportunity for crm.log_opportunity_note_internal.

EASY (deep_ui_interaction): a fresh crm.lead of type='opportunity' named
'Bench Note Opp' is created for customer 'Bench Note Co'. The agent must
post exactly one internal Log note ('Customer asked for demo') on the
opportunity's chatter.

The hard pattern being exercised is the chatter Log-note vs Send-message
distinction. Even though the chatter opens on Log note by default, some
agents flip to Send message and fail the subtype check.

Distinct from:
  - row 408 mail.send_email_with_attachment_log_as_note (uses Send message
    subtype=mail.mt_comment and requires a paperclip attachment).
  - project.complete_task_log_note (combines stage-change + log note).
  - sale.add_note_to_quotation (log note on a sale.order).
"""

PARTNER_NAME = "Bench Note Co"
PARTNER_EMAIL = "contact@benchnote.test"
OPP_NAME = "Bench Note Opp"


def setup(env):
    # --- Cleanup prior runs --------------------------------------------------
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if leads:
        # Drop activities and chatter messages first.
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        leads.unlink()

    # --- Ensure partner exists -----------------------------------------------
    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": PARTNER_EMAIL,
            "is_company": True,
            "company_type": "company",
        })

    # --- Ensure the 'New' stage exists so the opp has a consistent stage ----
    stage = env["crm.stage"].search(
        [("name", "=", "New")], limit=1
    )
    if not stage:
        stage = env["crm.stage"].search([], order="sequence", limit=1)

    # --- Create the opportunity ---------------------------------------------
    sales_team = env["crm.team"].search([], limit=1)
    admin = env.ref("base.user_admin")

    env["crm.lead"].create({
        "name": OPP_NAME,
        "partner_id": partner.id,
        "partner_name": PARTNER_NAME,
        "email_from": PARTNER_EMAIL,
        "type": "opportunity",
        "stage_id": stage.id if stage else False,
        "expected_revenue": 12000.0,
        "probability": 25.0,
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id,
        "description": "Prospect reached out via trade show booth.",
    })
