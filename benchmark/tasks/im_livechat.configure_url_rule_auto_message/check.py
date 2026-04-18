"""Postcondition checks for im_livechat.configure_url_rule_auto_message."""


def check(env):
    failures = []

    channels = env["im_livechat.channel"].search([("name", "=", "Website Support")])
    if len(channels) != 1:
        return [
            f"Expected exactly 1 channel named 'Website Support', found {len(channels)}"
        ]

    channel = channels[0]

    rules = env["im_livechat.channel.rule"].search([("channel_id", "=", channel.id)])
    if len(rules) != 1:
        return [
            f"Expected exactly 1 rule on 'Website Support', found {len(rules)}"
        ]

    rule = rules[0]
    if rule.regex_url != "/contact":
        failures.append(
            f"Rule URL Regex is {rule.regex_url!r}, expected '/contact'"
        )
    if rule.action != "auto_popup":
        failures.append(
            f"Rule action is {rule.action!r}, expected 'auto_popup' (Open automatically)"
        )
    if rule.auto_popup_timer != 5:
        failures.append(
            f"Rule auto_popup_timer is {rule.auto_popup_timer}, expected 5"
        )
    if rule.chatbot_script_id:
        failures.append(
            f"Rule chatbot_script_id should be empty, got {rule.chatbot_script_id.display_name}"
        )
    if rule.country_ids:
        failures.append(
            f"Rule country_ids should be empty, got {rule.country_ids.mapped('name')}"
        )

    return failures
