"""Seed four CRM leads for a bulk-archive Actions-menu task.

Category: Deep UI interaction (MEDIUM).

Three leads (`Bench Lost 1/2/3`) start with `active=True`, `probability=0`,
and a "Deferred" lost reason assigned — they represent leads that were
marked lost but never archived. One distractor (`Bench Keep 4`) is a
normal active lead with probability > 0 and no lost reason.

The agent must open CRM -> Leads list, filter/search for the three
Bench Lost leads, multi-select them via row checkboxes, and use the
list-view cog Actions -> Archive bulk action to flip `active=False`
on exactly those three leads while leaving `Bench Keep 4` active.

Notes on won_status: the stock Odoo "Lost" filter requires
`(won_status == 'lost' AND active == False)`, i.e. only shows archived
lost leads. Since our targets are still active, the agent cannot rely on
that filter — they should search by name / lost_reason or just type
"Bench Lost" into the search box.
"""


TARGET_NAMES = ["Bench Lost 1", "Bench Lost 2", "Bench Lost 3"]
DISTRACTOR_NAME = "Bench Keep 4"
ALL_NAMES = TARGET_NAMES + [DISTRACTOR_NAME]
LOST_REASON_NAME = "Deferred to next fiscal year"


def _cleanup_prior(env):
    Lead = env["crm.lead"].with_context(active_test=False)
    stale = Lead.search([("name", "in", ALL_NAMES)])
    for lead in stale:
        env["mail.activity"].search(
            [("res_model", "=", "crm.lead"), ("res_id", "=", lead.id)]
        ).unlink()
        env["mail.message"].search(
            [("model", "=", "crm.lead"), ("res_id", "=", lead.id)]
        ).unlink()
    if stale:
        # Reactivate any archived stale leads so unlink cascades cleanly.
        stale.with_context(active_test=False).write({"active": True})
        stale.unlink()


def setup(env):
    # Enable the Leads feature so the "Leads" top menu is visible.
    group_lead = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if group_lead:
        admin = env.ref("base.user_admin")
        if group_lead not in admin.group_ids:
            admin.write({"group_ids": [(4, group_lead.id)]})

    _cleanup_prior(env)

    # Lost reason used on the three targets to make it clear they are
    # "lost but still active".
    LostReason = env["crm.lost.reason"]
    reason = LostReason.search([("name", "=", LOST_REASON_NAME)], limit=1)
    if not reason:
        reason = LostReason.create({"name": LOST_REASON_NAME})
    elif not reason.active:
        reason.active = True

    Lead = env["crm.lead"]

    target_specs = [
        ("Bench Lost 1", "Alice Lost", "alice.bench@example.com"),
        ("Bench Lost 2", "Bob Lost", "bob.bench@example.com"),
        ("Bench Lost 3", "Carol Lost", "carol.bench@example.com"),
    ]
    for name, contact, email in target_specs:
        Lead.create(
            {
                "name": name,
                "type": "lead",
                "contact_name": contact,
                "email_from": email,
                "probability": 0.0,
                "automated_probability": 0.0,
                "lost_reason_id": reason.id,
                "active": True,
            }
        )

    # Distractor: a normal active lead, untouched by the task.
    Lead.create(
        {
            "name": DISTRACTOR_NAME,
            "type": "lead",
            "contact_name": "Dan Keep",
            "email_from": "dan.bench@example.com",
            "probability": 30.0,
            "active": True,
        }
    )

    # Force flush
    env.cr.execute("SELECT 1")
