"""Seed for website_forum.upvote_question_mark_as_answer.

Category: deep_ui_interaction (MEDIUM).

Creates:
  * A public forum 'Bench Forum' (mode='questions' since we only need one
    answer on the seeded question).
  * A non-admin contributor user 'benchbot' with karma well above every
    forum threshold, so benchbot can authored the question + answer.
  * A seeded question 'How do I install?' (parent_id=False,
    state='active') authored by benchbot, starting with zero votes.
  * One seeded answer authored by benchbot, is_correct=False.

Agent (admin) must:
  * Click the question's upvote caret (button.vote_up) → posts JSON-RPC to
    `/forum/<forum>/post/<question>/upvote`, which calls `forum.post.vote`
    and creates a `forum.post.vote` row with vote='1' and user_id=admin.id.
  * Click the benchbot answer's Accept checkmark
    (.o_wforum_validate_toggler) → posts to
    `/forum/<forum>/post/<answer>/toggle_correct` which flips
    `is_correct=True`.

The frontend upvote controller blocks a user from upvoting their own
post (`if request.env.uid == post.create_uid.id: return {'error':
'own_post'}`). Similarly, toggle_correct blocks own-post accept. So the
question + answer both MUST be authored by benchbot, not admin.

Admin is `is_admin()` True in forum karma compute, bypassing all
karma thresholds (karma_upvote, karma_answer_accept_all, etc.). The
seed still grants benchbot 5000 karma so benchbot can be the author
of any moderate-state post.

website_forum is NOT in base_modules.txt, so we button_immediate_install
it on demand.
"""


FORUM_NAME = "Bench Forum"
QUESTION_TITLE = "How do I install?"
QUESTION_CONTENT = (
    "<p>I have Odoo running locally but I cannot find a reliable way to "
    "install a custom module from the shell. What is the canonical install "
    "path that works without touching the Apps UI?</p>"
)
SEEDED_ANSWER_CONTENT = (
    "<p>Run the install pipeline via <code>button_immediate_install</code> "
    "on <code>ir.module.module</code>. That refreshes the registry and "
    "loads data files in one shot.</p>"
)
BENCHBOT_LOGIN = "benchbot"
BENCHBOT_NAME = "Bench Bot"
BENCHBOT_EMAIL = "benchbot@example.com"


def _ensure_module(env, module_name):
    mod = env["ir.module.module"].search(
        [("name", "=", module_name)], limit=1,
    )
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # --- Ensure website_forum is installed ---
    _ensure_module(env, "website_forum")

    if "forum.forum" not in env:
        raise RuntimeError(
            "forum.forum model missing even after website_forum install",
        )

    ForumForum = env["forum.forum"].with_context(active_test=False)
    ForumPost = env["forum.post"].with_context(active_test=False)
    ForumPostVote = env["forum.post.vote"].with_context(active_test=False)
    Users = env["res.users"].with_context(active_test=False)

    # --- Cleanup prior runs ---
    # Unlink any votes first (cascade would also cover this, but be explicit).
    prior_posts = ForumPost.search([
        "|", ("name", "=", QUESTION_TITLE),
             ("parent_id.name", "=", QUESTION_TITLE),
    ])
    if prior_posts:
        prior_votes = ForumPostVote.search(
            [("post_id", "in", prior_posts.ids)],
        )
        if prior_votes:
            prior_votes.unlink()
        prior_posts.unlink()

    prior_forum = ForumForum.search([("name", "=", FORUM_NAME)])
    if prior_forum:
        more_posts = ForumPost.search(
            [("forum_id", "in", prior_forum.ids)],
        )
        if more_posts:
            more_votes = ForumPostVote.search(
                [("post_id", "in", more_posts.ids)],
            )
            if more_votes:
                more_votes.unlink()
            more_posts.unlink()
        prior_forum.unlink()

    # --- Benchbot user (forum contributor) ---
    benchbot = Users.search([("login", "=", BENCHBOT_LOGIN)], limit=1)
    if not benchbot:
        benchbot = Users.create({
            "name": BENCHBOT_NAME,
            "login": BENCHBOT_LOGIN,
            "email": BENCHBOT_EMAIL,
            "password": "benchbot",
            "group_ids": [(4, env.ref("base.group_portal").id)],
        })
    benchbot.karma = 5000

    # --- Forum (public, question-mode so the seeded answer is the only one) ---
    forum = ForumForum.create({
        "name": FORUM_NAME,
        "mode": "questions",
        "privacy": "public",
        "active": True,
        "description": "Benchmark forum for install-related Q&A.",
    })

    # --- Seed question by benchbot ---
    question = ForumPost.with_user(benchbot).create({
        "name": QUESTION_TITLE,
        "content": QUESTION_CONTENT,
        "forum_id": forum.id,
        "parent_id": False,
    })

    # --- One seeded answer by benchbot, is_correct=False ---
    # Give the answer a distinct backend `name` so the state-diff match_key
    # (name, parent_id, create_uid) is unambiguous even though there is only
    # one answer — keeps the pattern robust against future changes.
    ForumPost.with_user(benchbot).create({
        "name": "Bench Bot install answer",
        "content": SEEDED_ANSWER_CONTENT,
        "forum_id": forum.id,
        "parent_id": question.id,
        "is_correct": False,
    })

    # Force vote_ids to be empty from the start (benchbot is not auto-upvoting
    # own post in the default create path, but belt-and-braces).
    stale_votes = ForumPostVote.search([("post_id", "=", question.id)])
    if stale_votes:
        stale_votes.unlink()
