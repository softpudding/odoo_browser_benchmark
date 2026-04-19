"""Seed for mass_mailing.create_mailing_select_list_schedule_send.

Seeds:
- A mailing.list 'Bench Newsletter Subs' with 3 mailing.contact rows.
- Idempotently cleans up any prior 'Spring Promo' mailing from a previous run.

The agent must create a new mailing.mailing from scratch (subject,
body, mailing list), click Schedule, fill the datetime widget in the
schedule-date wizard, and confirm — no duplicate of any existing record.
"""

SUBJECT = "Spring Promo"
LIST_NAME = "Bench Newsletter Subs"

CONTACT_EMAILS = [
    ("Spring Subscriber One", "spring1@bench.test"),
    ("Spring Subscriber Two", "spring2@bench.test"),
    ("Spring Subscriber Three", "spring3@bench.test"),
]


def _ensure_mass_mailing_module(env):
    module = env["ir.module.module"].search([("name", "=", "mass_mailing")], limit=1)
    if module and module.state != "installed":
        module.button_immediate_install()


def setup(env):
    _ensure_mass_mailing_module(env)

    # --- Cleanup any prior run ---
    env["mailing.mailing"].search([("subject", "=", SUBJECT)]).unlink()
    env["mailing.contact"].search([
        ("email", "in", [e for _, e in CONTACT_EMAILS]),
    ]).unlink()
    env["mailing.list"].search([("name", "=", LIST_NAME)]).unlink()

    # --- Create mailing list + 3 contacts ---
    mailing_list = env["mailing.list"].create({"name": LIST_NAME})
    for name, email in CONTACT_EMAILS:
        env["mailing.contact"].create({
            "name": name,
            "email": email,
            "subscription_ids": [(0, 0, {
                "list_id": mailing_list.id,
                "opt_out": False,
            })],
        })
