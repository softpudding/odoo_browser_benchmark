"""Seed contacts for a recurring calendar scheduling task."""


TITLE = "Northwind Steering Sync"


def _ensure_partner(env, name, email):
    partner = env["res.partner"].search([("email", "=", email)], limit=1)
    if partner:
        partner.write({"name": name})
        return partner
    return env["res.partner"].create({
        "name": name,
        "email": email,
    })


def setup(env):
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if admin:
        admin.write({"tz": "UTC"})

    env["calendar.event"].search([("name", "=", TITLE)]).unlink()

    _ensure_partner(env, "Avery Stone", "avery.stone@northwind.example.com")
    _ensure_partner(env, "Morgan Tate", "morgan.tate@northwind.example.com")
