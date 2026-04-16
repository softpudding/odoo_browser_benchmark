"""Postcondition checks for crm.batch_mark_lost_with_reason."""


TARGETS = {
    "Blue Canyon Power Renewal",
    "Blue Canyon Power Expansion",
}
DISTRACTOR = "Blue Canyon Logistics Renewal"
EXPECTED_REASON = "Price too high"
EXPECTED_NOTE = "Budget frozen until Q4 review."


def check(env):
    failures = []

    lead_env = env["crm.lead"].with_context(active_test=False)
    targets = lead_env.search([("name", "in", list(TARGETS))])
    distractor = lead_env.search([("name", "=", DISTRACTOR)], limit=1)

    if len(targets) != 2:
        return [f"Expected 2 target opportunities, found {len(targets)}"]
    if not distractor:
        return [f"Distractor opportunity {DISTRACTOR!r} not found"]

    for lead in targets:
        if lead.active:
            failures.append(f"{lead.name} is still active, expected archived/lost")
        if float(lead.probability or 0.0) != 0.0:
            failures.append(f"{lead.name} probability is {lead.probability}, expected 0")
        if lead.lost_reason_id.name != EXPECTED_REASON:
            failures.append(
                f"{lead.name} lost reason is {lead.lost_reason_id.name!r}, expected {EXPECTED_REASON!r}"
            )
        note_messages = env["mail.message"].search(
            [
                ("model", "=", "crm.lead"),
                ("res_id", "=", lead.id),
            ],
            order="id desc",
        )
        if not any(EXPECTED_NOTE.lower() in (msg.body or "").lower() for msg in note_messages):
            failures.append(f"{lead.name} is missing the expected closing note")

    if not distractor.active:
        failures.append("Distractor opportunity was archived")
    if distractor.lost_reason_id:
        failures.append("Distractor opportunity received a lost reason")

    return failures
