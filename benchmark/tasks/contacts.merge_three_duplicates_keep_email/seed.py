"""Seed four 'John Doe' contacts for a 3-way merge task.

Three are true duplicates (BENCH-JD-01, BENCH-JD-02, BENCH-JD-03) with
disjoint email/phone data; the fourth (BENCH-JD-DECOY) is a different
John Doe under Acme Corp and must NOT be merged.

Design:
- JD-01: no email, no phone (pure placeholder)
- JD-02: email=john@x.com, no phone
- JD-03: no email, phone=555-1234
- JD-DECOY: email=jdoe@acme.com, parent company Acme Corp

Because the base merge wizard's _update_values picks the last-truthy
value in iteration order (src_partners, then dst_partner), and the three
duplicates have disjoint email/phone, ANY of the three is an acceptable
master and the merge always produces email=john@x.com AND phone=555-1234
on the survivor — as long as the agent selects ONLY the three duplicates
(not the decoy) and uses Actions > Merge.
"""


DUP_NAME = "John Doe"
DECOY_REF = "BENCH-JD-DECOY"
ACME_REF = "BENCH-JD-ACME"
REFS = ["BENCH-JD-01", "BENCH-JD-02", "BENCH-JD-03", DECOY_REF, ACME_REF]


def setup(env):
    Partner = env["res.partner"].with_context(active_test=False)

    # Cleanup stale records from prior runs
    stale = Partner.search([("ref", "in", REFS)])
    for p in stale:
        p.active = True
    stale.unlink()

    # Create Acme Corp as parent company for the decoy
    acme = Partner.create({
        "ref": ACME_REF,
        "name": "Acme Corp",
        "is_company": True,
        "email": "info@acme.com",
    })

    # Three duplicate JD records with disjoint email/phone
    Partner.create({
        "ref": "BENCH-JD-01",
        "name": DUP_NAME,
        "is_company": False,
    })
    Partner.create({
        "ref": "BENCH-JD-02",
        "name": DUP_NAME,
        "is_company": False,
        "email": "john@x.com",
    })
    Partner.create({
        "ref": "BENCH-JD-03",
        "name": DUP_NAME,
        "is_company": False,
        "phone": "555-1234",
    })

    # Decoy: same name but different person under Acme Corp
    Partner.create({
        "ref": DECOY_REF,
        "name": DUP_NAME,
        "is_company": False,
        "email": "jdoe@acme.com",
        "parent_id": acme.id,
    })
