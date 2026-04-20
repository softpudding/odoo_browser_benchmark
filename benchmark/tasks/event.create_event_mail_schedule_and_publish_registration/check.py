"""Check event.create_event_mail_schedule_and_publish_registration."""

def check(env):
    failures = []
    event = env["event.event"].search([("name", "=", "Dock Systems Expo 2026")], limit=1)
    if not event:
        return ["Event not found"]
    if "website_published" in event._fields and not event.website_published:
        failures.append("Event is not published")
    sched = event.event_mail_ids
    if len(sched) != 1:
        failures.append(f"Expected 1 communication line, found {len(sched)}")
    else:
        s = sched[0]
        if s.interval_type != "before_event":
            failures.append(f"interval_type is {s.interval_type!r}, expected 'before_event'")
        if s.interval_unit != "days" or s.interval_nbr != 2:
            failures.append(f"interval is {s.interval_nbr} {s.interval_unit}, expected 2 days")
        if not s.template_ref or s.template_ref.name != "Bench Event Reminder":
            failures.append("Template is not Bench Event Reminder")
    regs = env["event.registration"].search([("event_id", "=", event.id)])
    if regs:
        failures.append("No registrations should be created")
    return failures
