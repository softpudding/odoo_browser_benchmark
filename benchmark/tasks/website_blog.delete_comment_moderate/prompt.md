# Moderate comments on a blog post: delete the spam

The published blog post `Bench Mod Post` (in the blog `Bench News`) has two public comments in its chatter:

1. A legitimate review from `Reviewer Good` that starts with `Great write-up` — keep this one.
2. A spam comment from `Spam Bot` that starts with `BUY CHEAP` — delete this one.

You are logged in as admin; admin may delete any chatter message.

## Steps

1. Open **Website > Site > Blog Posts** (or navigate directly to the blog-post back-office list at `/odoo/blog-post-pages`).
2. Open the post titled `Bench Mod Post`.
3. Scroll to the chatter at the bottom of the form. Two **comments** (not Log notes) are visible — one by `Reviewer Good`, one by `Spam Bot`.
4. On the spam comment authored by `Spam Bot` (body starts with `BUY CHEAP`), hover over the message so the per-message action toolbar appears. Open the overflow / `...` (Expand) menu of that toolbar if the trash icon is not directly visible.
5. Click the red **Delete** action (trash / `fa-trash` icon).
6. In the confirmation dialog (`Are you sure you want to bid farewell to this message forever?`), click **Confirm** (or the equivalent primary confirmation button).
7. The spam message should disappear from the chatter immediately. The `Reviewer Good` comment must still be visible and unchanged.

## Rules

- Delete ONLY the spam comment by `Spam Bot`. Do NOT delete the `Reviewer Good` comment.
- Do NOT edit, reply to, pin, bookmark, or log-note either comment. A reply, edit, or new comment counts as a failure.
- Do NOT unpublish, archive, rename, or change the author of the blog post itself.
- Do NOT post a new chatter message of your own (no "Spam removed" note, no summary comment).
- Do NOT touch any other blog post. Exactly one post named `Bench Mod Post` must remain, still published, unchanged in title / blog / body / author.
- After the run, the post's chatter must show exactly **one** visible comment (the Reviewer Good review). The spam message must be gone from the chatter view (its underlying `mail.message` row may be either unlinked or its body cleared — both are acceptable outcomes of the chatter Delete action).
