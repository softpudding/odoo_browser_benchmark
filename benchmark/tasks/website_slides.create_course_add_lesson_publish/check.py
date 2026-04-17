"""Postcondition checks for website_slides.create_course_add_lesson_publish."""


def check(env):
    failures = []

    course = env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Dock Safety Express"),
    ], limit=1)
    if not course:
        return ["Course 'Dock Safety Express' not found"]

    if not course.website_published:
        failures.append("Course is not published")
    if "A quick refresher for loading-bay launch crews." not in (course.description_short or ""):
        failures.append(f"Short description is {course.description_short!r}")

    lesson = env["slide.slide"].with_context(active_test=False).search([
        ("name", "=", "Emergency Exit Drill"),
        ("channel_id", "=", course.id),
    ], limit=1)
    if not lesson:
        failures.append("Lesson 'Emergency Exit Drill' not found on the target course")
    else:
        if lesson.slide_category != "article":
            failures.append(f"Lesson category is {lesson.slide_category!r}")
        if not lesson.website_published:
            failures.append("Lesson is not published")
        if "assembly point" not in (lesson.html_content or ""):
            failures.append("Lesson article content is missing the expected body text")

    return failures
