"""Postcondition checks for mass_mailing.build_campaign_send_test_schedule."""

from datetime import datetime


def check(env):
    failures = []

    mailing = env["mailing.mailing"].search([("subject", "=", "Dockside April Bulletin")], limit=1)
    if not mailing:
        return ["Mailing 'Dockside April Bulletin' not found"]

    if mailing.preview != "Late berth changes and crane window updates":
        failures.append("Mailing preview text does not match the expected value")
    if mailing.schedule_type != "scheduled":
        failures.append(f"Schedule type is '{mailing.schedule_type}', expected 'scheduled'")
    if mailing.state != "in_queue":
        failures.append(f"Mailing state is '{mailing.state}', expected 'in_queue'")

    expected_dt = datetime(2026, 4, 30, 9, 0)
    if not mailing.schedule_date:
        failures.append("Mailing has no scheduled send date")
    else:
        actual = mailing.schedule_date.replace(tzinfo=None)
        if actual != expected_dt:
            failures.append(f"Schedule date is '{actual}', expected '{expected_dt}'")

    if mailing.contact_list_ids.mapped("name") != ["Dockside Subscribers"]:
        failures.append("Mailing is not linked only to the 'Dockside Subscribers' list")

    if not mailing.message_ids:
        failures.append("No chatter message was logged on the mailing after the test send")

    return failures
