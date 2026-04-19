"""Oracle for website_blog.delete_comment_moderate.

Logs in as admin and uses authenticated JSON-RPC to:
  1. Find the seeded blog.post 'Bench Mod Post'.
  2. List its mail.message comments (message_type='comment',
     subtype_id=mail.mt_comment).
  3. Identify the Spam Bot comment via body marker 'BUY CHEAP'.
  4. Unlink that single mail.message row.

Admin is super-user and can unlink mail.message directly. This is
equivalent to — and more deterministic than — driving the chatter
Delete action in the browser (which hits
`/mail/message/update_content` with body=''). The check.py
postcondition accepts either outcome: spam message unlinked OR spam
body cleared, so long as no non-empty spam body survives on the
post.
"""

import json

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


POST_NAME = "Bench Mod Post"
SPAM_MARKER = "BUY CHEAP"


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
    navigate(page, "/odoo/blog-post-pages")
    page.wait_for_timeout(800)

    # 1. Find the seeded post.
    posts = _call_kw(
        page, "blog.post", "search_read",
        [[("name", "=", POST_NAME)], ["id"]],
        {"limit": 1},
    )
    if not posts:
        raise RuntimeError(f"Seeded post not found: {POST_NAME}")
    post_id = posts[0]["id"]

    # 2. Resolve the mt_comment subtype id.
    subtypes = _call_kw(
        page, "ir.model.data", "search_read",
        [[
            ("module", "=", "mail"),
            ("name", "=", "mt_comment"),
        ], ["res_id"]],
        {"limit": 1},
    )
    if not subtypes:
        raise RuntimeError("mail.mt_comment subtype not found")
    mt_comment_id = subtypes[0]["res_id"]

    # 3. Fetch comment messages on the post and identify the spam.
    messages = _call_kw(
        page, "mail.message", "search_read",
        [[
            ("model", "=", "blog.post"),
            ("res_id", "=", post_id),
            ("message_type", "=", "comment"),
            ("subtype_id", "=", mt_comment_id),
        ], ["id", "body", "author_id"]],
        {},
    )
    if len(messages) < 2:
        raise RuntimeError(
            f"Expected at least 2 chatter comments on the post, got "
            f"{len(messages)}: {messages!r}"
        )

    spam_ids = [
        m["id"] for m in messages if SPAM_MARKER in (m.get("body") or "")
    ]
    if not spam_ids:
        raise RuntimeError(
            f"Could not find spam comment by marker {SPAM_MARKER!r} in "
            f"{messages!r}"
        )
    if len(spam_ids) > 1:
        raise RuntimeError(
            f"Found multiple spam comments ({len(spam_ids)}); "
            f"seed should have produced exactly one."
        )

    # 4. Unlink the spam comment as admin.
    _call_kw(page, "mail.message", "unlink", [spam_ids], {})

    # 5. Sanity re-read.
    remaining = _call_kw(
        page, "mail.message", "search_read",
        [[
            ("model", "=", "blog.post"),
            ("res_id", "=", post_id),
            ("message_type", "=", "comment"),
            ("subtype_id", "=", mt_comment_id),
        ], ["id", "body"]],
        {},
    )
    still_spammy = [m for m in remaining if SPAM_MARKER in (m.get("body") or "")]
    if still_spammy:
        raise RuntimeError(
            f"Spam comment still present after unlink: {still_spammy!r}"
        )

    print(
        "Oracle: spam comment id=%s unlinked; %d comment(s) remain on post "
        "id=%s" % (spam_ids[0], len(remaining), post_id)
    )


run_oracle(oracle)
