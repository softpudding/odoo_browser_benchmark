"""Postcondition checks for website_forum.upvote_question_mark_as_answer.

Validates:
1. Forum 'Bench Forum' still exists and still has the seeded question.
2. The seeded question 'How do I install?' is intact (name, state='active',
   parent_id is False).
3. The question has gained exactly ONE new forum.post.vote row owned by
   admin, with vote='1' (the agent's upvote click).
4. The seeded benchbot answer has is_correct=True.
5. No new forum.post records were created (exactly 1 question + 1 answer,
   both authored by benchbot).
6. The answer itself has NOT been upvoted — the task only asks for
   upvoting the question.
"""


FORUM_NAME = "Bench Forum"
QUESTION_TITLE = "How do I install?"


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

    if question.name != QUESTION_TITLE:
        failures.append(
            f"Question name changed to {question.name!r}"
        )

    answers = env["forum.post"].with_context(active_test=False).search([
        ("parent_id", "=", question.id),
    ])

    if len(answers) != 1:
        failures.append(
            f"Expected exactly 1 answer on the question (the seeded one), "
            f"got {len(answers)}"
        )

    admin_user = env["res.users"].search(
        [("login", "=", "admin")], limit=1,
    )
    if not admin_user:
        return ["admin user not found"]

    benchbot = env["res.users"].search(
        [("login", "=", "benchbot")], limit=1,
    )
    if not benchbot:
        return ["benchbot user not found"]

    # The seeded answer must belong to benchbot and be marked correct.
    if answers:
        bot_answers = answers.filtered(lambda a: a.create_uid == benchbot)
        admin_answers = answers.filtered(lambda a: a.create_uid == admin_user)
        if len(bot_answers) != 1:
            failures.append(
                f"Expected exactly 1 benchbot-authored answer, got "
                f"{len(bot_answers)}"
            )
        if admin_answers:
            failures.append(
                f"An admin-authored answer was created; the task forbids "
                f"posting new answers (found {len(admin_answers)})."
            )
        if bot_answers and not bot_answers[0].is_correct:
            failures.append(
                "The seeded benchbot answer is NOT marked is_correct=True; "
                "the agent must click the Accept checkmark on it."
            )

    # Question must have exactly one upvote row from admin.
    Vote = env["forum.post.vote"].with_context(active_test=False)
    q_votes = Vote.search([("post_id", "=", question.id)])
    up_votes = q_votes.filtered(lambda v: v.vote == "1")
    if len(up_votes) != 1:
        failures.append(
            f"Expected exactly 1 upvote (vote='1') on the question, "
            f"got {len(up_votes)} (all vote rows: {len(q_votes)})"
        )
    elif up_votes.user_id != admin_user:
        failures.append(
            f"Upvote on question is not authored by admin; got user "
            f"{up_votes.user_id.login!r}"
        )

    # No downvotes on the question.
    down_votes = q_votes.filtered(lambda v: v.vote == "-1")
    if down_votes:
        failures.append(
            f"Question has {len(down_votes)} downvote(s); task forbids "
            f"downvoting."
        )

    # Answer must NOT have been voted on (task says only upvote the question).
    if answers:
        a_votes = Vote.search([("post_id", "in", answers.ids)])
        if a_votes:
            failures.append(
                f"Answer was voted on ({len(a_votes)} vote row(s)); task "
                f"only asks the agent to upvote the QUESTION."
            )

    return failures
