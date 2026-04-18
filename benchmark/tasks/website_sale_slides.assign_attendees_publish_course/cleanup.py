"""Cleanup for website_sale_slides.assign_attendees_publish_course."""


def cleanup(env):
    Channel = env["slide.channel"].with_context(active_test=False)
    ChannelPartner = env["slide.channel.partner"].with_context(active_test=False)
    Partner = env["res.partner"].with_context(active_test=False)

    channels = Channel.search([
        ("name", "in", ["Bench Onboarding", "Bench 101"]),
    ])
    if channels:
        ChannelPartner.search([("channel_id", "in", channels.ids)]).unlink()
        channels.unlink()

    partners = Partner.search([
        ("name", "in", ["Alice Attendee", "Bob Attendee"]),
    ])
    if partners:
        env["mail.mail"].with_context(active_test=False).search([
            ("email_to", "in", [p.email for p in partners if p.email]),
        ]).unlink()
        partners.unlink()

    env["ir.mail_server"].with_context(active_test=False).search([
        ("name", "=", "benchmark_fake_smtp"),
    ]).unlink()
