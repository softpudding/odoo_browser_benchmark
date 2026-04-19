"""Cleanup for crm.bulk_archive_lost_leads."""


NAMES = ["Bench Lost 1", "Bench Lost 2", "Bench Lost 3", "Bench Keep 4"]
LOST_REASON_NAME = "Deferred to next fiscal year"


def cleanup(env):
    Lead = env["crm.lead"].with_context(active_test=False)
    stale = Lead.search([("name", "in", NAMES)])
    for lead in stale:
        env["mail.activity"].search(
            [("res_model", "=", "crm.lead"), ("res_id", "=", lead.id)]
        ).unlink()
        env["mail.message"].search(
            [("model", "=", "crm.lead"), ("res_id", "=", lead.id)]
        ).unlink()
    if stale:
        stale.with_context(active_test=False).write({"active": True})
        stale.unlink()

    LostReason = env["crm.lost.reason"]
    reasons = LostReason.search([("name", "=", LOST_REASON_NAME)])
    if reasons:
        try:
            reasons.unlink()
        except Exception:
            reasons.write({"active": False})
