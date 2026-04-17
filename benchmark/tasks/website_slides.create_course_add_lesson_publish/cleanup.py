"""Cleanup for website_slides.create_course_add_lesson_publish."""


def cleanup(env):
    env["slide.slide"].with_context(active_test=False).search([
        ("name", "=", "Emergency Exit Drill"),
    ]).unlink()
    env["slide.channel"].with_context(active_test=False).search([
        ("name", "=", "Dock Safety Express"),
    ]).unlink()
