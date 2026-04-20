"""Check website_slides.create_course_add_certification_toggle_visibility."""

def check(env):
    failures = []
    course = env["slide.channel"].with_context(active_test=False).search([("name", "=", "Compliance Badge Basics")], limit=1)
    if not course:
        return ["Course not found"]
    if not course.website_published:
        failures.append("Course is not published")
    if course.visibility != "members":
        failures.append(f"visibility is {course.visibility!r}, expected 'members'")
    if course.enroll != "invite":
        failures.append(f"enroll is {course.enroll!r}, expected 'invite'")
    lesson = env["slide.slide"].with_context(active_test=False).search([("name", "=", "Badge Criteria"), ("channel_id", "=", course.id)], limit=1)
    if not lesson:
        failures.append("Lesson not found")
    else:
        if lesson.slide_category != "article":
            failures.append(f"slide_category is {lesson.slide_category!r}")
        if not lesson.website_published:
            failures.append("Lesson is not published")
        if "safety checklist" not in (lesson.html_content or ""):
            failures.append("Lesson body missing expected phrase")
    return failures
