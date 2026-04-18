"""Seed an existing draft mailing for the duplicate-and-modify workflow.

Category 5 (MEDIUM): The agent must use the Action menu Duplicate on a
seeded draft mailing, then change the subject and switch the recipients
model to Contact with a Country=Germany domain filter on the COPY only.

Capability tested: Action menu Duplicate + multi-field edit on the copy
without touching the original. The original uses Mailing List recipients;
the copy must be retargeted to res.partner (Contact) with a country filter.
"""


SOURCE_SUBJECT = "Q1 Bulletin Template"
DUP_SUBJECT = "Q2 Bulletin Update"


def _ensure_mass_mailing_module(env):
    module = env["ir.module.module"].search([("name", "=", "mass_mailing")], limit=1)
    if module and module.state != "installed":
        module.button_immediate_install()


def setup(env):
    _ensure_mass_mailing_module(env)

    # --- Cleanup any prior mailing with either subject ---
    env["mailing.mailing"].search([
        ("subject", "in", [SOURCE_SUBJECT, DUP_SUBJECT]),
    ]).unlink()

    # --- Cleanup the seeded mailing list (only ours) ---
    env["mailing.list"].search([("name", "=", "Bench Q1 Subscribers")]).unlink()

    # --- Create a small mailing list for the source mailing ---
    mailing_list = env["mailing.list"].create({
        "name": "Bench Q1 Subscribers",
    })

    # --- Get model ids ---
    list_model = env["ir.model"].search([("model", "=", "mailing.list")], limit=1)
    if not list_model:
        raise RuntimeError("ir.model for mailing.list not found")

    # --- Get email_from for the source mailing ---
    admin = env.ref("base.user_admin")
    email_from = admin.email or admin.partner_id.email or "admin@example.com"

    # --- Create the source draft mailing (Mailing List recipients) ---
    env["mailing.mailing"].create({
        "subject": SOURCE_SUBJECT,
        "email_from": email_from,
        "mailing_model_id": list_model.id,
        "contact_list_ids": [(6, 0, [mailing_list.id])],
        "body_html": "<p>Q1 bulletin template body.</p>",
        "body_arch": "<p>Q1 bulletin template body.</p>",
    })
