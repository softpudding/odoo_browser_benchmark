"""Clean up artifacts from previous runs for contacts.merge_three_duplicates_keep_email."""


REFS = ["BENCH-JD-01", "BENCH-JD-02", "BENCH-JD-03", "BENCH-JD-DECOY", "BENCH-JD-ACME"]


def cleanup(env):
    Partner = env["res.partner"].with_context(active_test=False)
    stale = Partner.search([("ref", "in", REFS)])
    for p in stale:
        p.active = True
    stale.unlink()
