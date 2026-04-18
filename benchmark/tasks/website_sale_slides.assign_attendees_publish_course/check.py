"""Postcondition checks for website_sale_slides.assign_attendees_publish_course."""


def check(env):
    failures = []

    course = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Bench Onboarding"),
    ], limit=1)
    if not course:
        return ["Course 'Bench Onboarding' not found"]

    prereq = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Bench 101"),
    ], limit=1)
    if not prereq:
        failures.append("Prerequisite course 'Bench 101' is missing (must not be deleted)")

    # Target course must be published.
    if not course.is_published:
        failures.append(
            f"Course 'Bench Onboarding' must be published (is_published=True); "
            f"got is_published={course.is_published}"
        )
    if not course.website_published:
        failures.append(
            "Course 'Bench Onboarding' website_published is False — publication "
            "toggle was not applied"
        )

    # Visibility must be 'members' (Course Attendees).
    if course.visibility != "members":
        failures.append(
            f"Course 'Bench Onboarding' visibility must be 'members', "
            f"got {course.visibility!r}"
        )

    # Enroll must be 'invite' (auto-coerced by _compute_enroll when
    # visibility == 'members').
    if course.enroll != "invite":
        failures.append(
            f"Course 'Bench Onboarding' enroll must be 'invite', got "
            f"{course.enroll!r}"
        )

    # Prerequisite must contain exactly Bench 101.
    prereq_names = sorted(course.prerequisite_channel_ids.mapped("name"))
    if prereq_names != ["Bench 101"]:
        failures.append(
            f"Course 'Bench Onboarding' prerequisite_channel_ids must be exactly "
            f"['Bench 101'], got {prereq_names}"
        )

    # Exactly two attendees: Alice Attendee + Bob Attendee, both 'joined'.
    attendees = env["slide.channel.partner"].with_context(active_test=False).search([
        ("channel_id", "=", course.id),
    ])
    attendee_names = sorted(attendees.mapped("partner_id.name"))
    if attendee_names != ["Alice Attendee", "Bob Attendee"]:
        failures.append(
            f"Course 'Bench Onboarding' attendees must be exactly "
            f"['Alice Attendee', 'Bob Attendee'], got {attendee_names}"
        )
    else:
        for ap in attendees:
            if ap.member_status != "joined":
                failures.append(
                    f"Attendee {ap.partner_id.name!r} must have member_status "
                    f"'joined' (enrolled), got {ap.member_status!r}"
                )

    # Bench 101 must be unchanged: published + members + invite.
    if prereq:
        if not prereq.is_published:
            failures.append("Prerequisite 'Bench 101' must remain published (is_published=True)")
        if prereq.visibility != "members":
            failures.append(
                f"Prerequisite 'Bench 101' visibility must remain 'members', "
                f"got {prereq.visibility!r}"
            )
        # Bench 101 must not have acquired Bench Onboarding as a prerequisite
        # (no cyclic linking from the agent).
        bench101_prereq_names = sorted(prereq.prerequisite_channel_ids.mapped("name"))
        if bench101_prereq_names:
            failures.append(
                f"Prerequisite 'Bench 101' must have NO prerequisites of its own, "
                f"got {bench101_prereq_names}"
            )
        # Bench 101 must not have accidentally gained enrolled attendees during
        # this task.
        b101_attendees = env["slide.channel.partner"].with_context(active_test=False).search([
            ("channel_id", "=", prereq.id),
        ])
        b101_attendee_names = sorted(b101_attendees.mapped("partner_id.name"))
        if b101_attendee_names:
            failures.append(
                f"Prerequisite 'Bench 101' should have no attendees, got "
                f"{b101_attendee_names}"
            )

    # No extra courses must have been created.
    all_bench_channels = env["slide.channel"].with_context(active_test=False).search([
        ("name", "like", "Bench"),
    ])
    extra = [c.name for c in all_bench_channels if c.name not in ("Bench Onboarding", "Bench 101")]
    if extra:
        failures.append(f"Unexpected extra courses created: {extra}")

    return failures
