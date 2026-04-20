"""Seed for im_livechat.configure_channel_hours_operator_rules."""

def setup(env):
    env["im_livechat.channel"].search([("name", "=", "Support Routing")]).unlink()
    demo = env.ref("base.user_demo", raise_if_not_found=False)
    livechat_group = env.ref("im_livechat.im_livechat_group_user")
    if not demo:
        demo = env["res.users"].create({
            "name": "Demo User",
            "login": "demo",
            "password": "demo",
            "group_ids": [
                (4, env.ref("base.group_user").id),
                (4, livechat_group.id),
            ],
        })
    elif livechat_group not in demo.groups_id:
        demo.groups_id = [(4, livechat_group.id)]
