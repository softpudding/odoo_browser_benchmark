"""Oracle for website_forum.post_question_accept_answer.

Logs in as admin and uses authenticated JSON-RPC to:
  1. Find the seeded forum 'Bench Q&A' and question 'How to configure
     Bench module?' (both authored by benchbot in the seed).
  2. Create a new forum.post answer authored by admin, attached to the
     seeded question (parent_id=question.id). The content contains
     'button_immediate_install' and is >=50 chars (match the real
     browser answer textarea minlength).
  3. Flip is_correct=True on the seeded canonical benchbot answer (the
     one whose content contains 'button_immediate_install'), and leave
     the decoy benchbot answer with is_correct=False.

The frontend controller `/forum/<forum>/post/<post>/toggle_correct`
refuses to toggle is_correct when the accepting user is also the post
author. Admin is an accepting internal user, but benchbot is the
author of the canonical answer — which is fine. In JSON-RPC we bypass
the controller entirely by writing is_correct directly via call_kw
(oracle short-circuit, permitted by ODOO19_PATTERNS.md oracle contract).

The browser-use agent must still:
  * post its own answer through the Your Answer textarea,
  * find and click the Accept checkmark on the benchbot canonical answer.
"""

import json

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
)


FORUM_NAME = "Bench Q&A"
QUESTION_TITLE = "How to configure Bench module?"
ADMIN_ANSWER_CONTENT = (
    "<p>Use button_immediate_install on ir.module.module so that the "
    "install pipeline runs synchronously and the registry is refreshed.</p>"
)
CANONICAL_MARKER = "button_immediate_install"


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

    # Warm the /forum action so the frontend JS bundle loads and session
    # cookies are set before call_kw.
    page.goto(full_url("/forum"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(800)

    # Locate forum + question
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

    # Locate the canonical + decoy benchbot answers.
    answers = _call_kw(
        page, "forum.post", "search_read",
        [[("parent_id", "=", question_id)], ["id", "content", "is_correct"]],
        {},
    )
    if len(answers) < 2:
        raise RuntimeError(
            f"Expected >=2 seeded answers, got {len(answers)}"
        )
    canonical = [
        a for a in answers if CANONICAL_MARKER in (a.get("content") or "")
    ]
    if not canonical:
        raise RuntimeError(
            "Canonical benchbot answer (containing "
            f"{CANONICAL_MARKER!r}) not found among seeded answers"
        )
    canonical_id = canonical[0]["id"]

    # 1. Create the admin answer (mirrors the real Post Answer flow).
    new_answer_id = _call_kw(
        page, "forum.post", "create",
        [[{
            "name": "Re: %s" % QUESTION_TITLE,
            "content": ADMIN_ANSWER_CONTENT,
            "forum_id": forum_id,
            "parent_id": question_id,
            "is_correct": False,
        }]],
        {},
    )
    if isinstance(new_answer_id, list):
        new_answer_id = new_answer_id[0]
    if not new_answer_id:
        raise RuntimeError("admin answer creation failed")

    # 2. Mark benchbot canonical answer as correct. Direct write bypasses
    #    the controller own-post guard, which the agent cannot trip here
    #    because they are NOT the author of this answer.
    _call_kw(
        page, "forum.post", "write",
        [[canonical_id], {"is_correct": True}],
        {},
    )

    # Sanity
    check = _call_kw(
        page, "forum.post", "read",
        [[canonical_id], ["is_correct"]], {},
    )
    if not check or not check[0].get("is_correct"):
        raise RuntimeError("canonical answer is_correct did not persist")

    print(
        "Oracle: admin answer id=%s created; canonical answer id=%s "
        "marked is_correct=True" % (new_answer_id, canonical_id)
    )


run_oracle(oracle)
