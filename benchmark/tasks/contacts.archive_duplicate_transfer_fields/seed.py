"""Seed for contacts.archive_duplicate_transfer_fields.

Category: recovery_rollback (HARD).
Seeds two same-named company partners distinguished by their 'ref'
field. The agent must transfer the phone + email from the duplicate
to the primary, then archive the duplicate (active=False) via the
Actions menu — without deleting it.
"""

NAME = "Ridgeway Global Services"
PRIMARY_REF = "RGS-PRIMARY"
DUPLICATE_REF = "RGS-DUPLICATE"
PHONE = "+1 415 555 0188"
EMAIL = "contact@ridgeway-global.example"


def setup(env):
    Partner = env["res.partner"].with_context(active_test=False)

    # Remove all prior runs of either record (hard-delete; archived or
    # not).
    stale = Partner.search([
        ("ref", "in", [PRIMARY_REF, DUPLICATE_REF]),
    ])
    for p in stale:
        p.active = True
    stale.unlink()

    Partner.create({
        "name": NAME,
        "ref": PRIMARY_REF,
        "is_company": True,
        "street": "45 Market Street",
        "city": "San Francisco",
        "zip": "94103",
        "country_id": env.ref("base.us").id,
    })
    Partner.create({
        "name": NAME,
        "ref": DUPLICATE_REF,
        "is_company": True,
        "phone": PHONE,
        "email": EMAIL,
    })
