"""Cleanup for website_forum.post_question_accept_answer."""


FORUM_NAME = "Bench Q&A"
QUESTION_TITLE = "How to configure Bench module?"
BENCHBOT_LOGIN = "benchbot"


def cleanup(env):
    # Defensive: website_forum may not be installed if the base snapshot
    # was rebuilt without it; models won't exist in that case.
    if "forum.forum" not in env:
        return

    ForumForum = env["forum.forum"].with_context(active_test=False)
    ForumPost = env["forum.post"].with_context(active_test=False)

    forums = ForumForum.search([("name", "=", FORUM_NAME)])
    if forums:
        (ForumPost.search([("forum_id", "in", forums.ids)])).unlink()
        forums.unlink()

    # Catch stragglers (e.g. a question re-created by a failed seed rerun
    # that did not cascade).
    stragglers = ForumPost.search([
        "|", ("name", "=", QUESTION_TITLE),
             ("parent_id.name", "=", QUESTION_TITLE),
    ])
    if stragglers:
        stragglers.unlink()

    # Leave benchbot user around — cheaper to keep idempotent than to
    # unlink a user that may own attachments/messages.
