"""Check im_livechat.configure_channel_hours_operator_rules."""

def check(env):
    failures = []
    channel = env["im_livechat.channel"].search([("name", "=", "Support Routing")], limit=1)
    if not channel:
        return ["Channel not found"]
    if channel.button_text != "Talk to support now":
        failures.append(f"button_text is {channel.button_text!r}")
    if channel.max_sessions_mode != "limited":
        failures.append(f"max_sessions_mode is {channel.max_sessions_mode!r}")
    if channel.max_sessions != 1:
        failures.append(f"max_sessions is {channel.max_sessions}, expected 1")
    names = set(channel.user_ids.mapped("name"))
    if names != {"Administrator", "Demo User"}:
        failures.append(f"Agents are {sorted(names)!r}, expected Administrator and Demo User")
    if len(channel.rule_ids) != 1:
        failures.append(f"Expected 1 rule, found {len(channel.rule_ids)}")
    else:
        rule = channel.rule_ids[0]
        if rule.regex_url != "/support":
            failures.append(f"regex_url is {rule.regex_url!r}")
        if rule.action != "display_button":
            failures.append(f"action is {rule.action!r}, expected 'display_button'")
    return failures
