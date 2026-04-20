"""Check mass_mailing.create_sms_mailing_filter_schedule_send."""
from ast import literal_eval


def check(env):
    failures = []
    mailing = env["mailing.mailing"].search([("subject", "=", "Berlin Ops SMS")], limit=1)
    if not mailing:
        return ["SMS mailing not found"]
    if mailing.mailing_type != "sms":
        failures.append(f"mailing_type is {mailing.mailing_type!r}, expected 'sms'")
    if "Berlin operations update" not in (mailing.body_plaintext or ""):
        failures.append("SMS body does not contain expected text")
    if mailing.state not in {"in_queue", "schedule", "scheduled", "draft"}:
        failures.append(f"Unexpected state {mailing.state!r}")
    if not mailing.schedule_date:
        failures.append("schedule_date is empty")
    dom = mailing.mailing_domain or ""
    if "Berlin" not in dom and "berlin" not in dom.lower():
        try:
            parsed = literal_eval(dom)
            count = env["res.partner"].search_count(parsed)
            if count != 2:
                failures.append(f"mailing_domain count is {count}, expected 2")
        except Exception:
            failures.append(f"mailing_domain is {dom!r}, expected Berlin filter")
    return failures
