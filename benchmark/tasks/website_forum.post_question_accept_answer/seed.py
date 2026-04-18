"""Seed for website_forum.post_question_accept_answer.

Category: deep_ui_interaction (MEDIUM).

Creates:
  * A public forum 'Bench Q&A' (mode='discussions' so multiple answers are
    allowed — the agent posts one answer while the pre-seeded benchbot
    answer remains distinct).
  * A non-admin contributor user 'benchbot' with karma well above every
    forum threshold, so benchbot can have posted both the seeded question
    and the candidate answers.
  * A seeded question 'How to configure Bench module?' (parent_id=False,
    state='active') authored by benchbot.
  * Two candidate answers on that question, both authored by benchbot.
    Both start with is_correct=False. The agent's task is to accept the
    canonical one ('You can install it via button_immediate_install ...').

The frontend /forum/<forum>/post/<post>/toggle_correct controller blocks
the currently logged-in user from accepting their own answer
(`if request.env.uid == post.create_uid.id: return {'error': 'own_post'}`).
That is the only reason the question and candidate answers have to be
authored by benchbot, not admin — admin (the agent) cannot mark their
own post as correct, so the accepted answer must belong to a different
user. The agent still authors one brand-new answer as admin, which is
the artefact the state-diff / postcondition checks verify was created
during the run.

Admin is an internal user and already `is_admin()` in the forum karma
model, so no karma grant on admin is needed; the own-post block is a
separate guard that karma does not override.

If website_forum is not installed in the base snapshot, we install it
on demand (the base list only carries `website_blog`, `website_sale`,
`website_slides`).
"""


FORUM_NAME = "Bench Q&A"
QUESTION_TITLE = "How to configure Bench module?"
QUESTION_CONTENT = (
    "<p>I need to install and configure the custom Bench module on a fresh "
    "Odoo database. The standard Apps UI does not always work for me — what "
    "is the canonical programmatic install path?</p>"
)
TAG_NAME = "bench"
CANONICAL_ANSWER_CONTENT = (
    "<p>You can install it via <code>button_immediate_install</code> on "
    "<code>ir.module.module</code>. This triggers the module install "
    "pipeline synchronously and refreshes the registry.</p>"
)
DECOY_ANSWER_CONTENT = (
    "<p>Just edit <code>odoo.conf</code> and add the module name to the "
    "addons path. Then restart the server. That usually works for simple "
    "modules, though it does not install the data files.</p>"
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

    # After install, the forum model must be reachable. If not, abort
    # loudly so the task harness surfaces a real error instead of NPE.
    if "forum.forum" not in env:
        raise RuntimeError(
            "forum.forum model missing even after website_forum install",
        )

    ForumForum = env["forum.forum"].with_context(active_test=False)
    ForumPost = env["forum.post"].with_context(active_test=False)
    ForumTag = env["forum.tag"].with_context(active_test=False)
    Users = env["res.users"].with_context(active_test=False)

    # --- Cleanup prior runs ---
    prior_posts = ForumPost.search([
        "|", ("name", "=", QUESTION_TITLE),
             ("parent_id.name", "=", QUESTION_TITLE),
    ])
    if prior_posts:
        prior_posts.unlink()

    prior_forum = ForumForum.search([("name", "=", FORUM_NAME)])
    if prior_forum:
        # Drop all posts under it, then drop the forum itself.
        (ForumPost.search([("forum_id", "in", prior_forum.ids)])).unlink()
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
    # Generous karma so benchbot passes every threshold if needed.
    benchbot.karma = 5000

    # --- Forum (public, multi-answer) ---
    forum = ForumForum.create({
        "name": FORUM_NAME,
        "mode": "discussions",
        "privacy": "public",
        "active": True,
        "description": "Benchmark forum for Bench module Q&A.",
    })

    # --- Tag 'bench' ---
    tag = ForumTag.search(
        [("name", "=", TAG_NAME), ("forum_id", "=", forum.id)], limit=1,
    )
    if not tag:
        tag = ForumTag.create({
            "name": TAG_NAME,
            "forum_id": forum.id,
            "create_uid": benchbot.id,
        })

    # --- Seed question by benchbot ---
    question = ForumPost.with_user(benchbot).create({
        "name": QUESTION_TITLE,
        "content": QUESTION_CONTENT,
        "forum_id": forum.id,
        "parent_id": False,
        "tag_ids": [(6, 0, [tag.id])],
    })

    # --- Two candidate answers by benchbot (not correct yet) ---
    # Distinct `name` values so state-diff match_key (name, parent_id,
    # create_uid) identifies them unambiguously. The frontend renders
    # answers by content, not name; the title is a backend-only field.
    ForumPost.with_user(benchbot).create([{
        "name": "Bench Bot canonical answer",
        "content": CANONICAL_ANSWER_CONTENT,
        "forum_id": forum.id,
        "parent_id": question.id,
        "is_correct": False,
    }, {
        "name": "Bench Bot decoy answer",
        "content": DECOY_ANSWER_CONTENT,
        "forum_id": forum.id,
        "parent_id": question.id,
        "is_correct": False,
    }])
