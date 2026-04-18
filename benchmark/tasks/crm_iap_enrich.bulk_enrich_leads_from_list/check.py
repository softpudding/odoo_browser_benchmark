"""Postcondition checks for crm_iap_enrich.bulk_enrich_leads_from_list."""

import re

NAMES_TARGET = [
    "Bench Enrich Target Alpha",
    "Bench Enrich Target Bravo",
    "Bench Enrich Target Charlie",
]
NAME_DISTRACT_DONE = "Bench Enrich Already Delta"
NAME_DISTRACT_SKIP = "Bench Enrich Manual Echo"
# Substring from crm_iap_enrich.mail_message_lead_enrich_notfound template
# body: "No company data found based on the email address or email address
# is one of an email provider. No credit was consumed."
NOTFOUND_SUBSTRING = "No company data found"


def _strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html or "")
    text = (
        text.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&#39;", "'")
        .replace("&quot;", '"')
    )
    return " ".join(text.split()).strip()


def _has_notfound_msg(env, lead):
    """Return True if the lead has at least one mail.message whose plain-text
    body contains the enrichment no-match/no-credit marker."""
    msgs = env["mail.message"].search([
        ("model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
    ])
    for m in msgs:
        body_text = _strip_html(m.body or "")
        if NOTFOUND_SUBSTRING in body_text:
            return True
    return False


def check(env):
    failures = []
    Lead = env["crm.lead"].with_context(active_test=False)

    # --- Target leads: iap_enrich_done must be True AND a 'No company data
    #     found' chatter message must be present.
    for name in NAMES_TARGET:
        lead = Lead.search([("name", "=", name)], limit=1)
        if not lead:
            failures.append(f"Target lead '{name}' is missing")
            continue
        if not lead.active:
            failures.append(f"Target lead '{name}' was archived")
        if not lead.iap_enrich_done:
            failures.append(
                f"Target lead '{name}' has iap_enrich_done=False; the Enrich "
                f"action must have run on it"
            )
        if not _has_notfound_msg(env, lead):
            failures.append(
                f"Target lead '{name}' has no chatter message matching "
                f"'{NOTFOUND_SUBSTRING}' — the Enrich Action menu entry did "
                f"not post the expected no-match template on this lead"
            )
        if lead.type == "opportunity":
            failures.append(
                f"Target lead '{name}' was converted to an opportunity; only "
                f"the Enrich action should have run"
            )

    # --- Distractors must not have received a NEW notfound message during
    #     the run.  Both distractors start as iap_enrich_done=True, so even
    #     if selected the bulk action skips them — meaning their
    #     notfound-message count should stay 0.
    for name in (NAME_DISTRACT_DONE, NAME_DISTRACT_SKIP):
        lead = Lead.search([("name", "=", name)], limit=1)
        if not lead:
            failures.append(f"Distractor lead '{name}' is missing")
            continue
        if not lead.active:
            failures.append(f"Distractor lead '{name}' was archived")
        if not lead.iap_enrich_done:
            failures.append(
                f"Distractor lead '{name}' had iap_enrich_done reset to False "
                f"— it must remain True"
            )
        if _has_notfound_msg(env, lead):
            failures.append(
                f"Distractor lead '{name}' has an 'No company data found' "
                f"chatter message; it was not expected to receive one "
                f"during this run (it was already marked iap_enrich_done=True "
                f"at seed time)"
            )

    # --- Record-count guard: no new or deleted leads with the BENCH-ENRICH
    #     name prefix.
    all_names = NAMES_TARGET + [NAME_DISTRACT_DONE, NAME_DISTRACT_SKIP]
    seeded = Lead.search([("name", "in", all_names)])
    if len(seeded) != 5:
        failures.append(
            f"Expected 5 seeded Bench Enrich leads; found {len(seeded)}"
        )

    return failures
