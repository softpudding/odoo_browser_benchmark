"""Postcondition checks for event.publish_event_register_attendee."""


def check(env):
    failures = []
    event = env["event.event"].search([("name", "=", "Field Service Summit 2026")], limit=1)
    if not event:
        return ["Field Service Summit 2026 not found"]
    if "website_published" in event._fields and not event.website_published:
        failures.append("Event is not published")

    regs = env["event.registration"].search([
        ("event_id", "=", event.id),
        ("name", "=", "Jordan Rivera"),
        ("email", "=", "jordan.rivera@example.com"),
    ])
    if len(regs) != 1:
        failures.append(f"Expected exactly one matching registration, found {len(regs)}")
        return failures

    reg = regs[0]
    if reg.phone != "+1 555 0199":
        failures.append(f"Attendee phone is {reg.phone!r}")
    if reg.state not in {"open", "done"}:
        failures.append(f"Attendee state is {reg.state!r}")
    return failures
