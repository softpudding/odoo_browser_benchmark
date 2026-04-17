"""Postcondition checks for im_livechat.create_channel_add_canned_response."""


def check(env):
    failures = []

    channels = env["im_livechat.channel"].search([("name", "=", "Checkout Support")])
    if len(channels) != 1:
        return [f"Expected exactly 1 channel named 'Checkout Support', found {len(channels)}"]

    channel = channels[0]
    if channel.button_text != "Need help with your order?":
        failures.append(
            f"Channel notification text is '{channel.button_text}', expected 'Need help with your order?'"
        )

    responses = env["mail.canned.response"].search([("source", "=", "checkout_help")])
    if len(responses) != 1:
        failures.append(
            f"Expected exactly 1 canned response with shortcut 'checkout_help', found {len(responses)}"
        )
    else:
        if responses[0].substitution != "Hello, thanks for contacting checkout support.":
            failures.append("Canned response content does not match the expected text")

    return failures
