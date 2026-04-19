"""Oracle for website_forum.upvote_question_mark_as_answer.

Logs in as admin and uses authenticated JSON-RPC to:
  1. Find the seeded forum 'Bench Forum' and question 'How do I install?'
     (both authored by benchbot in the seed).
  2. Create a `forum.post.vote` row on the question with vote='1' and
     user_id=admin.id, mirroring what a user click on the caret-up
     upvote arrow would do via the `/forum/<forum>/post/<post>/upvote`
     controller (which itself calls `forum.post.vote(upvote=True)`).
  3. Flip is_correct=True on the seeded benchbot answer.

The frontend upvote + toggle_correct controllers both refuse when
`request.env.uid == post.create_uid.id`. Admin is NOT the author of
either post, so admin can both upvote the question and accept the
answer. In JSON-RPC we bypass the controllers by calling the ORM
methods directly (oracle short-circuit, permitted by
ODOO19_PATTERNS.md oracle contract).

The browser-use agent must still:
  * click the question's caret-up (`button.vote_up`) upvote button,
  * click the Accept checkmark (`.o_wforum_validate_toggler`) on the
    benchbot answer.
"""

import json

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
)


FORUM_NAME = "Bench Forum"
QUESTION_TITLE = "How do I install?"
ANSWER_MARKER = "button_immediate_install"


def _call_kw(page, model, method, args, kwargs=None):
    kwargs = kwargs or {}
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args,
            "kwargs": kwargs,
        },
    }
    result = page.evaluate(
        """async (payload) => {
            const resp = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'same-origin',
                body: JSON.stringify(payload),
            });
            return resp.json();
        }""",
        payload,
    )
    if isinstance(result, dict) and result.get("error"):
        raise RuntimeError(
            f"call_kw {model}.{method} error: "
            f"{json.dumps(result['error'])[:600]}"
        )
    return result.get("result") if isinstance(result, dict) else result


def oracle(page):
    login(page)

    # Warm the /forum frontend so JS bundle loads and session cookies set
    # before call_kw.
    page.goto(full_url("/forum"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(800)

    # --- Resolve seeded forum + question + answer ids -------------------
    forums = _call_kw(
        page, "forum.forum", "search_read",
        [[("name", "=", FORUM_NAME)], ["id", "name"]],
        {"limit": 1},
    )
    if not forums:
        raise RuntimeError(f"Seeded forum missing: {FORUM_NAME}")
    forum_id = forums[0]["id"]

    questions = _call_kw(
        page, "forum.post", "search_read",
        [[
            ("forum_id", "=", forum_id),
            ("name", "=", QUESTION_TITLE),
            ("parent_id", "=", False),
        ], ["id", "name"]],
        {"limit": 1},
    )
    if not questions:
        raise RuntimeError(f"Seeded question missing: {QUESTION_TITLE}")
    question_id = questions[0]["id"]

    answers = _call_kw(
        page, "forum.post", "search_read",
        [[("parent_id", "=", question_id)], ["id", "content", "is_correct"]],
        {},
    )
    if len(answers) != 1:
        raise RuntimeError(
            f"Expected exactly 1 seeded answer, got {len(answers)}"
        )
    answer_id = answers[0]["id"]

    # --- Get admin user id (for vote ownership) --------------------------
    admin_users = _call_kw(
        page, "res.users", "search_read",
        [[("login", "=", "admin")], ["id"]], {"limit": 1},
    )
    if not admin_users:
        raise RuntimeError("admin user not found")
    admin_uid = admin_users[0]["id"]

    # --- 1. Upvote the question (create forum.post.vote row) -------------
    # Mirror what post.vote(upvote=True) does: create a vote row with
    # post_id=question, user_id=admin, vote='1'. Admin bypasses karma
    # and is not the post author, so no controller guard fires.
    # Use the ORM-level `forum.post.vote` method which is safer w.r.t.
    # karma bookkeeping than raw create on forum.post.vote.
    _call_kw(
        page, "forum.post", "vote",
        [[question_id]],
        {"upvote": True},
    )

    # Sanity: fetch vote rows on the question.
    vote_rows = _call_kw(
        page, "forum.post.vote", "search_read",
        [[("post_id", "=", question_id)], ["id", "user_id", "vote"]],
        {},
    )
    if not any(
        (v.get("user_id") or [None])[0] == admin_uid and v.get("vote") == "1"
        for v in vote_rows
    ):
        raise RuntimeError(
            f"Expected admin upvote row on question; got {vote_rows!r}"
        )

    # --- 2. Mark benchbot answer as the correct answer -------------------
    _call_kw(
        page, "forum.post", "write",
        [[answer_id], {"is_correct": True}],
        {},
    )

    # Sanity: is_correct persisted.
    check = _call_kw(
        page, "forum.post", "read",
        [[answer_id], ["is_correct"]], {},
    )
    if not check or not check[0].get("is_correct"):
        raise RuntimeError("seeded answer is_correct did not persist")

    print(
        "Oracle: question id=%s upvoted by admin; answer id=%s "
        "marked is_correct=True" % (question_id, answer_id)
    )


run_oracle(oracle)
