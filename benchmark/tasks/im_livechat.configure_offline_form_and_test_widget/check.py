"""Postcondition checks for im_livechat.configure_offline_form_and_test_widget."""


CHANNEL_NAME = "After Hours Help"


def check(env):
    failures = []

    channel = env["im_livechat.channel"].search([("name", "=", CHANNEL_NAME)])
    if len(channel) != 1:
        return [f"Expected exactly 1 live chat channel named '{CHANNEL_NAME}', found {len(channel)}"]

    channel = channel[0]
    if channel.button_text != "Questions after hours?":
        failures.append(
            f"Notification text is '{channel.button_text}', expected 'Questions after hours?'"
        )
    if channel.default_message != "Leave your email and we will get back to you tomorrow morning.":
        failures.append("Default message does not match the expected offline copy")
    if channel.available_operator_ids:
        failures.append("Channel still has available operators, expected an offline channel")

    info = channel.sudo().get_livechat_info(username="Visitor")
    if info.get("available"):
        failures.append("Public live chat info reports the channel as available")
    if "can_load_livechat: false" not in (channel.script_external or "") and "loader" not in (channel.script_external or ""):
        failures.append("Channel does not expose the expected public loader script")

    return failures
