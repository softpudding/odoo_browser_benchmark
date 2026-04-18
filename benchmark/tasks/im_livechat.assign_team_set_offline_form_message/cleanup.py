"""Cleanup for im_livechat.assign_team_set_offline_form_message."""


def cleanup(env):
    env["im_livechat.channel"].search([("name", "=", "Website Support")]).unlink()
