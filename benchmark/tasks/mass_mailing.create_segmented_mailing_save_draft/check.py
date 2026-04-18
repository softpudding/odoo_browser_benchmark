"""Postcondition checks for mass_mailing.create_segmented_mailing_save_draft."""

from ast import literal_eval


SUBJECT = "Berlin April Bulletin"


def check(env):
    failures = []
    mailings = env["mailing.mailing"].search([("subject", "=", SUBJECT)])
    if len(mailings) == 0:
        return [f"No mailing.mailing with subject {SUBJECT!r}"]
    if len(mailings) > 1:
        failures.append(f"Expected exactly one mailing with subject {SUBJECT!r}, found {len(mailings)}")
    mailing = mailings[0]

    if mailing.state != "draft":
        failures.append(f"mailing.state is {mailing.state!r}, expected 'draft'")

    if mailing.mailing_model_name != "res.partner":
        failures.append(
            f"mailing.mailing_model_name is {mailing.mailing_model_name!r}, expected 'res.partner'"
        )

    body = (mailing.body_html or "") + " " + (mailing.body_arch or "")
    if "Berlin team" not in body:
        failures.append("body does not contain 'Berlin team'")

    domain_str = mailing.mailing_domain or ""
    domain_ok = ("city" in domain_str.lower()) and ("berlin" in domain_str.lower())
    recipient_count = None
    if domain_str:
        try:
            domain = literal_eval(domain_str)
            recipient_count = env["res.partner"].search_count(domain)
        except Exception:
            recipient_count = None
    if not domain_ok and recipient_count != 2:
        failures.append(
            f"mailing_domain {domain_str!r} does not match Berlin (recipient_count={recipient_count})"
        )

    # Make sure the mailing has not been sent.
    if mailing.sent_date:
        failures.append(f"mailing was sent at {mailing.sent_date}")

    # The Berlin contacts must still exist (the agent should not have deleted them).
    for name in ("Berlin Alpha Co", "Berlin Beta Co", "Munich Gamma Co"):
        if not env["res.partner"].sudo().search_count([
            ("name", "=", name),
            ("is_company", "=", True),
        ]):
            failures.append(f"Seed contact {name!r} is missing")

    return failures
