"""Cleanup for website_slides.duplicate_course_edit_add_slide."""


def cleanup(env):
    Channel = env["slide.channel"].with_context(active_test=False)
    Slide = env["slide.slide"].with_context(active_test=False)
    ChannelPartner = env["slide.channel.partner"].with_context(active_test=False)

    channels = Channel.search([
        "|",
        ("name", "in", ["Bench Course Original", "Bench Course Spring"]),
        ("name", "=like", "Bench Course Original%"),
    ])
    if channels:
        ChannelPartner.search([("channel_id", "in", channels.ids)]).unlink()
        Slide.search([("channel_id", "in", channels.ids)]).unlink()
        channels.unlink()

    Slide.search([
        ("name", "in", ["Bench Intro Video", "Welcome slide"]),
    ]).unlink()
