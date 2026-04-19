"""Postcondition checks for website_slides.duplicate_course_edit_add_slide."""


def check(env):
    failures = []

    original = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Bench Course Original"),
    ])
    spring = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Bench Course Spring"),
    ])

    if len(original) != 1:
        failures.append(
            f"Expected exactly 1 course named 'Bench Course Original', "
            f"found {len(original)}"
        )
    if len(spring) != 1:
        failures.append(
            f"Expected exactly 1 course named 'Bench Course Spring', "
            f"found {len(spring)}"
        )

    # Exactly TWO Bench Course channels (original + spring). Catch agents that
    # leave a stray `Bench Course Original (copy)` alongside the renamed one.
    bench_channels = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=ilike", "Bench Course%"),
    ])
    channel_names = sorted(bench_channels.mapped("name"))
    if channel_names != ["Bench Course Original", "Bench Course Spring"]:
        failures.append(
            "Expected exactly two 'Bench Course*' channels "
            "['Bench Course Original', 'Bench Course Spring'], "
            f"got {channel_names}"
        )

    if original:
        # Original course must still have its seeded slide, unchanged.
        original_slides = env["slide.slide"].with_context(active_test=False).search([
            ("channel_id", "=", original.id),
            ("is_category", "=", False),
        ])
        orig_names = sorted(original_slides.mapped("name"))
        if orig_names != ["Bench Intro Video"]:
            failures.append(
                f"Original course 'Bench Course Original' slides must be "
                f"exactly ['Bench Intro Video'], got {orig_names}"
            )

    if spring:
        # Spring copy must have EXACTLY one slide with name 'Welcome slide'.
        spring_slides = env["slide.slide"].with_context(active_test=False).search([
            ("channel_id", "=", spring.id),
            ("is_category", "=", False),
        ])
        spring_names = [s.name for s in spring_slides]
        if spring_names != ["Welcome slide"]:
            failures.append(
                f"Course 'Bench Course Spring' must have exactly one slide "
                f"named 'Welcome slide', got {spring_names}"
            )
        else:
            new_slide = spring_slides[0]
            if new_slide.slide_category not in ("article", "document"):
                failures.append(
                    f"New slide 'Welcome slide' on 'Bench Course Spring' must "
                    f"have slide_category in ('article', 'document'), got "
                    f"{new_slide.slide_category!r}"
                )

    return failures
