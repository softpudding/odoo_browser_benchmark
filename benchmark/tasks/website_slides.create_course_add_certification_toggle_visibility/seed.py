"""Seed for website_slides.create_course_add_certification_toggle_visibility."""

def setup(env):
    env["slide.slide"].with_context(active_test=False).search([("name", "=", "Badge Criteria")]).unlink()
    env["slide.channel"].with_context(active_test=False).search([("name", "=", "Compliance Badge Basics")]).unlink()
