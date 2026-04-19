"""Postcondition checks for im_livechat.configure_channel_then_handle_widget_chat."""


def check(env):
    failures = []

    channels = env["im_livechat.channel"].search([("name", "=", "Bench Support")])
    if len(channels) != 1:
        return [
            f"Expected exactly 1 channel named 'Bench Support', found {len(channels)}"
        ]

    channel = channels[0]

    if channel.default_message != "How can we help?":
        failures.append(
            f"Channel welcome message is '{channel.default_message}', "
            f"expected 'How can we help?'"
        )

    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        failures.append("Administrator user (base.user_admin) is missing")
    else:
        if admin not in channel.user_ids:
            failures.append(
                "Administrator is not listed as an operator on the 'Bench Support' channel"
            )
        if len(channel.user_ids) != 1:
            failures.append(
                f"Channel 'Bench Support' has {len(channel.user_ids)} operators, expected exactly 1"
            )

    responses = env["mail.canned.response"].search([("source", "=", ":hi")])
    if len(responses) < 1:
        failures.append(
            f"Expected at least 1 canned response with shortcut ':hi', found {len(responses)}"
        )
    else:
        matching = responses.filtered(
            lambda r: r.substitution == "Hi! How can I help you today?"
        )
        if not matching:
            failures.append(
                "No canned response with shortcut ':hi' has the expected "
                "substitution 'Hi! How can I help you today?'"
            )

    return failures
