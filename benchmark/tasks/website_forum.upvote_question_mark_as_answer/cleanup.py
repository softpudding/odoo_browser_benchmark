"""Cleanup for website_forum.upvote_question_mark_as_answer."""


FORUM_NAME = "Bench Forum"
QUESTION_TITLE = "How do I install?"


def cleanup(env):
    # Defensive: website_forum may not be installed if the base snapshot
    # was rebuilt without it; models won't exist in that case.
    if "forum.forum" not in env:
        return

    ForumForum = env["forum.forum"].with_context(active_test=False)
    ForumPost = env["forum.post"].with_context(active_test=False)
    ForumPostVote = env["forum.post.vote"].with_context(active_test=False)

    forums = ForumForum.search([("name", "=", FORUM_NAME)])
    if forums:
        posts = ForumPost.search([("forum_id", "in", forums.ids)])
        if posts:
            stale_votes = ForumPostVote.search(
                [("post_id", "in", posts.ids)],
            )
            if stale_votes:
                stale_votes.unlink()
            posts.unlink()
        forums.unlink()

    # Catch stragglers (e.g. a question re-created by a failed seed rerun
    # that did not cascade).
    stragglers = ForumPost.search([
        "|", ("name", "=", QUESTION_TITLE),
             ("parent_id.name", "=", QUESTION_TITLE),
    ])
    if stragglers:
        straggler_votes = ForumPostVote.search(
            [("post_id", "in", stragglers.ids)],
        )
        if straggler_votes:
            straggler_votes.unlink()
        stragglers.unlink()

    # Leave benchbot user around — cheaper to keep idempotent than to
    # unlink a user that may own attachments/messages.
