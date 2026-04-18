"""Cleanup for website_slides.duplicate_lesson_to_new_section."""


def cleanup(env):
    Slide = env["slide.slide"].with_context(active_test=False)
    Channel = env["slide.channel"].with_context(active_test=False)

    Slide.search([
        ("name", "in", ["Welcome Video", "Advanced Welcome", "Intro", "Advanced"]),
    ]).unlink()
    Channel.search([
        ("name", "=", "Bench Onboarding Course"),
    ]).unlink()
