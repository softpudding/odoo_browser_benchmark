"""Seed for website_slides.add_quiz_lesson_to_existing_course.

Category: deep UI interaction (nested model editing).
Creates a published course "Bench Onboarding Course" with a single existing
"Welcome Video" video lesson. The agent must add a NEW quiz lesson with three
questions and three answer options each, marking the correct answer per
question, and publish the new quiz lesson.
"""


def setup(env):
    Channel = env["slide.channel"].with_context(active_test=False)
    Slide = env["slide.slide"].with_context(active_test=False)

    # Cleanup any leftovers from prior runs (slides cascade-delete via channel,
    # but be defensive in case of orphaned records).
    Slide.search([
        ("name", "in", ["Welcome Video", "Chapter 1 Quiz"]),
    ]).unlink()
    Channel.search([
        ("name", "=", "Bench Onboarding Course"),
    ]).unlink()

    channel = env["slide.channel"].create({
        "name": "Bench Onboarding Course",
        "description_short": "<p>Standard onboarding for new Bench engineers.</p>",
        "channel_type": "training",
        "visibility": "public",
        "is_published": True,
    })

    env["slide.slide"].create({
        "name": "Welcome Video",
        "channel_id": channel.id,
        "slide_category": "video",
        "video_source_type": "youtube",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "is_published": True,
        "completion_time": 0.05,  # ~3 minutes
    })
