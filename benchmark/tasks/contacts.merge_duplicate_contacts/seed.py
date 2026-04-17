"""Seed four Globex-prefixed company contacts for the merge task.

Two identically-named 'Globex Corporation' records are true duplicates;
'Globex plc' and 'Globex Labs' are distractor companies. Unique internal
refs keep the state diff scoped to only these four partners.
"""


DUP_NAME = "Globex Corporation"
REFS = {
    "GLOBEX-OLD": {
        "name": DUP_NAME,
        "email": "contact@globex-old.com",
        "phone": "+1 415 555 0188",
    },
    "GLOBEX-NEW": {
        "name": DUP_NAME,
        "email": "billing@globex.io",
        "vat": "BE0477472701",
    },
    "GLOBEX-PLC": {
        "name": "Globex plc",
        "email": "info@globex-plc.co.uk",
        "vat": "GB123456789",
        "phone": "+44 20 7946 0958",
    },
    "GLOBEX-LABS": {
        "name": "Globex Labs",
        "email": "research@globex-labs.io",
        "phone": "+1 650 555 0147",
    },
}


def setup(env):
    Partner = env["res.partner"].with_context(active_test=False)

    stale = Partner.search([("ref", "in", list(REFS.keys()))])
    for p in stale:
        p.active = True
    stale.unlink()

    for ref, vals in REFS.items():
        Partner.create({
            "ref": ref,
            "is_company": True,
            **vals,
        })
