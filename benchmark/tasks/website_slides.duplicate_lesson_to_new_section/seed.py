"""Seed for website_slides.duplicate_lesson_to_new_section.

Creates a published course "Bench Onboarding Course" with a single section
"Intro" containing one published video lesson "Welcome Video". The agent
must add a new "Advanced" section, duplicate the video lesson via the
Actions / cog menu, move the duplicate into the "Advanced" section, and
rename it to "Advanced Welcome".
"""


def setup(env):
    Channel = env["slide.channel"].with_context(active_test=False)
    Slide = env["slide.slide"].with_context(active_test=False)

    # Cleanup any leftovers from prior runs.
    Slide.search([
        ("name", "in", ["Welcome Video", "Advanced Welcome", "Intro", "Advanced"]),
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

    # Section: Intro (sequence 10)
    env["slide.slide"].create({
        "name": "Intro",
        "channel_id": channel.id,
        "is_category": True,
        "sequence": 10,
    })

    # Lesson: Welcome Video (sequence 20, falls under "Intro")
    env["slide.slide"].create({
        "name": "Welcome Video",
        "channel_id": channel.id,
        "slide_category": "video",
        "video_source_type": "youtube",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "is_published": True,
        "completion_time": 0.05,  # ~3 minutes
        "sequence": 20,
    })
