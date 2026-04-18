"""Cleanup for website_slides.add_quiz_lesson_to_existing_course."""


def cleanup(env):
    Slide = env["slide.slide"].with_context(active_test=False)
    Channel = env["slide.channel"].with_context(active_test=False)

    Slide.search([
        ("name", "in", ["Welcome Video", "Chapter 1 Quiz"]),
    ]).unlink()
    Channel.search([
        ("name", "=", "Bench Onboarding Course"),
    ]).unlink()
