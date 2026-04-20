"""Seed for mass_mailing.create_sms_mailing_filter_schedule_send."""

SUBJECT = "Berlin Ops SMS"
PARTNERS = [
    {"name": "Berlin Ops One", "city": "Berlin", "phone": "+491700000001"},
    {"name": "Berlin Ops Two", "city": "Berlin", "phone": "+491700000002"},
    {"name": "Hamburg Ops", "city": "Hamburg", "phone": "+491700000003"},
]

def setup(env):
    mod = env["ir.module.module"].search([("name", "=", "mass_mailing_sms")], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()
    env["mailing.mailing"].search([("subject", "=", SUBJECT)]).unlink()
    for spec in PARTNERS:
        recs = env["res.partner"].search([("name", "=", spec["name"])])
        recs.unlink()
        env["res.partner"].create({
            "name": spec["name"],
            "city": spec["city"],
            "phone": spec["phone"],
            "is_company": True,
        })
