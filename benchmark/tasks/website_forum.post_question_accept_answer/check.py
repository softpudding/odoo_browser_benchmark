"""Postcondition checks for website_forum.post_question_accept_answer.

Validates:
1. Forum 'Bench Q&A' still exists and has the seeded question.
2. The seeded question 'How to configure Bench module?' is intact
   (unchanged name, state='active', parent_id is False).
3. The pre-seeded canonical benchbot answer (content mentions
   'button_immediate_install') has is_correct=True.
4. The pre-seeded decoy benchbot answer has is_correct=False.
5. Exactly ONE new answer exists on the question authored by admin;
   its content mentions 'button_immediate_install' and is_correct is
   False (admin cannot accept their own post; even if they somehow
   flipped it, this is still a violation of the rules).
6. Total answers on the question == 3.
"""


FORUM_NAME = "Bench Q&A"
QUESTION_TITLE = "How to configure Bench module?"
CANONICAL_ANSWER_MARKER = "button_immediate_install"


def check(env):
    failures = []

    forum = env["forum.forum"].with_context(active_test=False).search(
        [("name", "=", FORUM_NAME)], limit=1,
    )
    if not forum:
        return [f"Forum '{FORUM_NAME}' not found"]

    question = env["forum.post"].with_context(active_test=False).search([
        ("forum_id", "=", forum.id),
        ("name", "=", QUESTION_TITLE),
        ("parent_id", "=", False),
    ], limit=1)
    if not question:
        return [f"Seeded question '{QUESTION_TITLE}' not found"]

    if question.state != "active":
        failures.append(
            f"Question state is {question.state!r}, expected 'active'",
        )

    answers = env["forum.post"].with_context(active_test=False).search([
        ("parent_id", "=", question.id),
    ])

    if len(answers) != 3:
        failures.append(
            f"Expected 3 answers on the question, got {len(answers)}"
        )

    admin_login = "admin"
    admin_user = env["res.users"].search(
        [("login", "=", admin_login)], limit=1,
    )
    if not admin_user:
        return ["admin user not found"]

    admin_answers = answers.filtered(lambda a: a.create_uid == admin_user)
    if len(admin_answers) != 1:
        failures.append(
            "Expected exactly 1 admin-authored answer, got "
            f"{len(admin_answers)}"
        )
    else:
        admin_answer = admin_answers[0]
        content = (admin_answer.content or "").lower()
        if CANONICAL_ANSWER_MARKER.lower() not in content:
            failures.append(
                "Admin answer content does not contain "
                f"{CANONICAL_ANSWER_MARKER!r}: {admin_answer.content!r}"
            )
        if admin_answer.is_correct:
            failures.append(
                "Admin answer has is_correct=True; admin cannot accept "
                "their own post, and the task requires accepting Bench "
                "Bot's canonical answer instead."
            )

    benchbot = env["res.users"].search(
        [("login", "=", "benchbot")], limit=1,
    )
    if not benchbot:
        return ["benchbot user not found"]

    bot_answers = answers.filtered(lambda a: a.create_uid == benchbot)
    if len(bot_answers) != 2:
        failures.append(
            f"Expected 2 benchbot-authored answers, got {len(bot_answers)}"
        )

    canonical = bot_answers.filtered(
        lambda a: CANONICAL_ANSWER_MARKER in (a.content or "")
    )
    if len(canonical) != 1:
        failures.append(
            f"Canonical benchbot answer (marker {CANONICAL_ANSWER_MARKER!r}) "
            f"not uniquely found: got {len(canonical)}"
        )
    elif not canonical.is_correct:
        failures.append(
            "Canonical benchbot answer is NOT marked is_correct=True; "
            "the agent must click Accept on that answer."
        )

    decoy = bot_answers - canonical
    if decoy and any(d.is_correct for d in decoy):
        failures.append(
            "The decoy benchbot answer was marked is_correct=True; "
            "only the canonical benchbot answer should be accepted."
        )

    # Nobody should have deleted or renamed the original question.
    if question.name != QUESTION_TITLE:
        failures.append(
            f"Question name changed to {question.name!r}"
        )

    return failures
