"""Postcondition checks for hr_recruitment.skill_filter_then_send_offer.

Validates:
1. Alice Senior has a mail.message with subject 'Job Offer - QA Lead'
   AND body containing '2026-06-01'.
2. Bob Junior, Dana Pirate, Eve Contractor, Charlie Jones have NO
   message with that offer subject.
3. Alice's stage/job/email/skill/tag unchanged.
4. All distractors still active and not refused.
"""

JOB_QA_LEAD = "QA Lead"
ALICE = "Alice Senior"
BOB = "Bob Junior"
DANA = "Dana Pirate"
EVE = "Eve Contractor"
CHARLIE = "Charlie Jones"

OFFER_SUBJECT = "Job Offer - QA Lead"
BODY_REQUIRED = "2026-06-01"


def _plain_text(html):
    import re
    if not html:
        return ""
    return re.sub(r"<[^>]+>", " ", html)


def check(env):
    failures = []
    Applicant = env["hr.applicant"].with_context(active_test=False)
    Msg = env["mail.message"].sudo()

    alice = Applicant.search([("partner_name", "=", ALICE)], limit=1)
    bob = Applicant.search([("partner_name", "=", BOB)], limit=1)
    dana = Applicant.search([("partner_name", "=", DANA)], limit=1)
    eve = Applicant.search([("partner_name", "=", EVE)], limit=1)
    charlie = Applicant.search([("partner_name", "=", CHARLIE)], limit=1)

    if not alice:
        return [f"Applicant '{ALICE}' not found"]

    # --- Alice: offer email must exist, with correct subject + body ---
    alice_msgs = Msg.search([
        ("model", "=", "hr.applicant"),
        ("res_id", "=", alice.id),
        ("subject", "=", OFFER_SUBJECT),
    ])
    if not alice_msgs:
        failures.append(
            f"No mail.message on '{ALICE}' with subject '{OFFER_SUBJECT}'"
        )
    else:
        has_date = any(
            BODY_REQUIRED in _plain_text(m.body or "") for m in alice_msgs
        )
        if not has_date:
            failures.append(
                f"Offer email body on '{ALICE}' does not contain the "
                f"required date '{BODY_REQUIRED}'"
            )

    # --- Alice fields unchanged ---
    if alice.job_id.name != JOB_QA_LEAD:
        failures.append(
            f"Alice's job is '{alice.job_id.name}', expected '{JOB_QA_LEAD}'"
        )
    if alice.email_from != "alice.senior@example.com":
        failures.append(f"Alice's email changed to '{alice.email_from}'")
    if "Senior" not in alice.categ_ids.mapped("name"):
        failures.append(
            f"Alice's Senior tag missing; tags: {alice.categ_ids.mapped('name')}"
        )
    if "Python" not in alice.applicant_skill_ids.mapped("skill_id.name"):
        failures.append(
            f"Alice's Python skill missing; skills: "
            f"{alice.applicant_skill_ids.mapped('skill_id.name')}"
        )
    if not alice.active or alice.refuse_reason_id:
        failures.append("Alice should not be refused/archived")

    # --- Other applicants: no offer email + untouched ---
    for other in (bob, dana, eve, charlie):
        if not other:
            failures.append("A seeded distractor applicant is missing")
            continue
        wrong_msgs = Msg.search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", other.id),
            ("subject", "=", OFFER_SUBJECT),
        ])
        if wrong_msgs:
            failures.append(
                f"Distractor '{other.partner_name}' should not have "
                f"the offer email; found {len(wrong_msgs)}"
            )
        if not other.active or other.refuse_reason_id:
            failures.append(
                f"Distractor '{other.partner_name}' should stay active/unreversed"
            )

    return failures
