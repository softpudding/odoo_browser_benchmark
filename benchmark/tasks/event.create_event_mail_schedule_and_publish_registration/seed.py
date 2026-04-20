"""Seed for event.create_event_mail_schedule_and_publish_registration."""

def setup(env):
    mod = env["ir.module.module"].search([("name", "=", "website_event")], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()
    env["event.event"].with_context(active_test=False).search([("name", "=", "Dock Systems Expo 2026")]).unlink()
    tmpl = env["mail.template"].search([("name", "=", "Bench Event Reminder"), ("model", "=", "event.registration")], limit=1)
    if not tmpl:
        model = env["ir.model"]._get("event.registration")
        env["mail.template"].create({
            "name": "Bench Event Reminder",
            "model_id": model.id,
            "subject": "Reminder for your event registration",
            "body_html": "<p>Reminder</p>",
            "email_from": env.user.email or "admin@example.com",
        })
