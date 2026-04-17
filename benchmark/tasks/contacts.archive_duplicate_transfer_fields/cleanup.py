"""Clean up artifacts from previous runs of contacts.archive_duplicate_transfer_fields."""

PRIMARY_REF = "RGS-PRIMARY"
DUPLICATE_REF = "RGS-DUPLICATE"


def cleanup(env):
    Partner = env["res.partner"].with_context(active_test=False)
    stale = Partner.search([("ref", "in", [PRIMARY_REF, DUPLICATE_REF])])
    for p in stale:
        p.active = True
    stale.unlink()
