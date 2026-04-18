"""Postcondition checks for website_slides.duplicate_lesson_to_new_section."""


def check(env):
    failures = []

    course = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Bench Onboarding Course"),
    ], limit=1)
    if not course:
        return ["Course 'Bench Onboarding Course' not found"]

    # Sections (slide.slide with is_category=True) on this course.
    sections = env["slide.slide"].with_context(active_test=False).search([
        ("channel_id", "=", course.id),
        ("is_category", "=", True),
    ])
    section_names = sections.mapped("name")
    if sorted(section_names) != ["Advanced", "Intro"]:
        failures.append(
            f"Expected exactly two sections ['Advanced', 'Intro'] on course, "
            f"got {sorted(section_names)}"
        )

    intro = sections.filtered(lambda s: s.name == "Intro")
    advanced = sections.filtered(lambda s: s.name == "Advanced")
    if not intro:
        failures.append("Section 'Intro' is missing")
    if not advanced:
        failures.append("Section 'Advanced' is missing")

    # Original Welcome Video must still be in Intro and unchanged.
    welcome = env["slide.slide"].with_context(active_test=False).search([
        ("name", "=", "Welcome Video"),
        ("channel_id", "=", course.id),
        ("is_category", "=", False),
    ])
    if len(welcome) != 1:
        failures.append(
            f"Expected exactly 1 'Welcome Video' lesson on course, found {len(welcome)}"
        )
    else:
        if welcome.slide_category != "video":
            failures.append(
                f"Welcome Video slide_category is {welcome.slide_category!r}, expected 'video'"
            )
        if not welcome.website_published:
            failures.append("Welcome Video lesson is no longer published")
        if intro and welcome.category_id != intro:
            failures.append(
                f"Welcome Video should still be in 'Intro' section, "
                f"but its section is {welcome.category_id.name!r}"
            )

    # New Advanced Welcome lesson must be in Advanced section, video category.
    adv_welcome = env["slide.slide"].with_context(active_test=False).search([
        ("name", "=", "Advanced Welcome"),
        ("channel_id", "=", course.id),
        ("is_category", "=", False),
    ])
    if len(adv_welcome) != 1:
        failures.append(
            f"Expected exactly 1 'Advanced Welcome' lesson on course, "
            f"found {len(adv_welcome)}"
        )
    else:
        if adv_welcome.slide_category != "video":
            failures.append(
                f"Advanced Welcome slide_category is {adv_welcome.slide_category!r}, "
                f"expected 'video' (since it must be a duplicate of Welcome Video)"
            )
        if advanced and adv_welcome.category_id != advanced:
            actual = adv_welcome.category_id.name if adv_welcome.category_id else None
            failures.append(
                f"Advanced Welcome should be in 'Advanced' section, "
                f"but its section is {actual!r}"
            )

    # Make sure no extra non-category slides exist on the course.
    all_lessons = env["slide.slide"].with_context(active_test=False).search([
        ("channel_id", "=", course.id),
        ("is_category", "=", False),
    ])
    lesson_names = sorted(all_lessons.mapped("name"))
    if lesson_names != ["Advanced Welcome", "Welcome Video"]:
        failures.append(
            f"Expected exactly two lessons ['Advanced Welcome', 'Welcome Video'] "
            f"on course, got {lesson_names}"
        )

    return failures
