"""Postcondition checks for im_livechat.add_canned_response_send_in_chat."""


def check(env):
    failures = []

    responses = env["mail.canned.response"].search([("source", "=", ":greet")])
    if len(responses) != 1:
        return [
            f"Expected exactly 1 canned response with source ':greet', found {len(responses)}"
        ]

    expected_substitution = "Hello! How can I help you today? \u2014 Bench Support"
    if responses[0].substitution != expected_substitution:
        failures.append(
            f"Canned response substitution is '{responses[0].substitution}', "
            f"expected '{expected_substitution}'"
        )

    return failures
