"""Seed five CRM leads for a bulk-enrich Actions-menu task.

Category: Deep UI interaction (HARD).

Design: All five leads use `@gmail.com` email addresses. `gmail.com` is
in `iap_tools._MAIL_PROVIDERS`, so `iap_enrich()` short-circuits before
hitting the external IAP endpoint — flipping `iap_enrich_done=True` and
posting a `mail_message_lead_enrich_notfound` chatter note ("No company
data found based on the email address or email address is one of an
email provider. No credit was consumed.") on each lead. This avoids any
dependency on live IAP credits or outbound network.

Three leads (BENCH-ENRICH-001/002/003) start with
`iap_enrich_done=False` and must be the ONLY leads selected for the
bulk action.

Two distractors are set up so that wrong selections fail the check:
- BENCH-ENRICH-DONE: already enriched (`iap_enrich_done=True`). Even if
  re-selected, `iap_enrich()` will skip it early and NOT re-post the
  notfound chatter message — so including it in selection WILL cause a
  check failure (we assert no new notfound message on the distractor
  during this run).
- BENCH-ENRICH-SKIP: also already enriched — marked as "do-not-enrich"
  per the prompt.

Pre-seed cleanup: remove any stale leads from prior runs (and their
messages/activities). The `crm_iap_enrich` module must be installed
(not in base snapshot); seed installs on demand.
"""

NAMES_TARGET = [
    "Bench Enrich Target Alpha",
    "Bench Enrich Target Bravo",
    "Bench Enrich Target Charlie",
]
NAMES_DISTRACT = [
    "Bench Enrich Already Delta",
    "Bench Enrich Manual Echo",
]
ALL_NAMES = NAMES_TARGET + NAMES_DISTRACT


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if not mod:
        raise RuntimeError(
            f"Module '{name}' not present in addons — cannot seed task"
        )
    if mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # Install crm_iap_enrich on demand (base snapshot has crm but not the
    # iap enrich bridge).
    _ensure_module(env, "crm_iap_enrich")

    # Enable the Leads feature so the "Leads" top menu is visible.
    group_lead = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if group_lead:
        admin = env.ref("base.user_admin")
        if group_lead not in admin.group_ids:
            admin.write({"group_ids": [(4, group_lead.id)]})

    # Auto-enrichment cron is scheduled after every crm.lead.create if the
    # setting is 'auto'. Turn it off during the seed so our leads stay in
    # the exact enrich-done state we specify.
    env["ir.config_parameter"].sudo().set_param(
        "crm.iap.lead.enrich.setting", "manual"
    )

    # --- Cleanup prior runs (messages + activities + leads, by unique name) ---
    Lead = env["crm.lead"].with_context(active_test=False)
    stale = Lead.search([("name", "in", ALL_NAMES)])
    for lead in stale:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
    stale.unlink()

    # --- Seed target leads (must be enriched by the agent) ---
    Lead.create({
        "name": "Bench Enrich Target Alpha",
        "type": "lead",
        "contact_name": "Alpha Contact",
        "email_from": "alpha.bench@gmail.com",
        "iap_enrich_done": False,
    })
    Lead.create({
        "name": "Bench Enrich Target Bravo",
        "type": "lead",
        "contact_name": "Bravo Contact",
        "email_from": "bravo.bench@gmail.com",
        "iap_enrich_done": False,
    })
    Lead.create({
        "name": "Bench Enrich Target Charlie",
        "type": "lead",
        "contact_name": "Charlie Contact",
        "email_from": "charlie.bench@gmail.com",
        "iap_enrich_done": False,
    })

    # --- Distractor 1: already enriched ---
    Lead.create({
        "name": "Bench Enrich Already Delta",
        "type": "lead",
        "contact_name": "Delta Contact",
        "email_from": "delta.bench@gmail.com",
        "iap_enrich_done": True,
    })

    # --- Distractor 2: also already enriched (marked do-not-enrich in prompt) ---
    Lead.create({
        "name": "Bench Enrich Manual Echo",
        "type": "lead",
        "contact_name": "Echo Contact",
        "email_from": "echo.bench@gmail.com",
        "iap_enrich_done": True,
    })
