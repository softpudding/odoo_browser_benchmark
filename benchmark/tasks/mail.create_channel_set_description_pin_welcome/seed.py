"""Seed data for mail.create_channel_set_description_pin_welcome."""


CHANNEL_NAME = "Launch Bridge Red"


def setup(env):
    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    channels.unlink()

    user = env["res.users"].search([("name", "=", "Marc Demo")], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "email": "marc.demo@example.com",
            "group_ids": [(6, 0, [env.ref("base.group_user").id])],
        })
