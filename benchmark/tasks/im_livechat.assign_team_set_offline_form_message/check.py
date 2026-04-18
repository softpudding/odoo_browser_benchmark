"""Postcondition checks for im_livechat.assign_team_set_offline_form_message."""

EXPECTED_BUTTON_TEXT = "Leave us a message and we will follow up by Monday."
EXPECTED_DEFAULT_MESSAGE = (
    "Hello \u2014 we are offline. "
    "Email support@bench.test and we will reply by Monday."
)


def check(env):
    failures = []

    channels = env["im_livechat.channel"].search([("name", "=", "Website Support")])
    if len(channels) != 1:
        return [
            f"Expected exactly 1 channel named 'Website Support', found {len(channels)}"
        ]

    channel = channels[0]

    if channel.button_text != EXPECTED_BUTTON_TEXT:
        failures.append(
            f"Channel button_text is {channel.button_text!r}, "
            f"expected {EXPECTED_BUTTON_TEXT!r}"
        )

    if channel.default_message != EXPECTED_DEFAULT_MESSAGE:
        failures.append(
            f"Channel default_message is {channel.default_message!r}, "
            f"expected {EXPECTED_DEFAULT_MESSAGE!r}"
        )

    # Sanity: do not have created/destroyed rules.
    rule_count = env["im_livechat.channel.rule"].search_count(
        [("channel_id", "=", channel.id)]
    )
    if rule_count != 0:
        failures.append(
            f"Expected 0 rules on 'Website Support', found {rule_count}"
        )

    return failures
