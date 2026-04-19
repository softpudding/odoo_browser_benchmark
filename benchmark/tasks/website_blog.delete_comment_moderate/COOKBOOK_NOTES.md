# Cookbook notes — website_blog.delete_comment_moderate

Row 482 (hard-tier). New patterns / quirks discovered while building this
moderation task.

## Chatter Delete action = `/mail/message/update_content` with body=''

- The per-message hover toolbar's trash icon (or its overflow / Expand
  menu entry labelled **Delete**, `fa-trash`) is registered in
  `addons/mail/static/src/core/common/message_actions.js` under the
  name `"delete"`. Its `onSelected` opens `MessageConfirmDialog` and,
  on confirm, calls `message.remove({ removeFromThread })`.
- `message.remove()` in `message_model.js` POSTs to
  `/mail/message/update_content` with `body: ""` and empty
  `attachment_ids`. It does NOT call `mail.message.unlink` by default.
- Server side, `mail.thread._message_update_content` writes the empty
  body, then calls `_clean_empty_message(message)`. On plain
  `mail.thread` (as blog.post), `_clean_empty_message` only unlinks
  link previews — the mail.message row survives with body=''.
- Consequence: after the chatter Delete, the spam mail.message record
  typically still exists in the DB, just with body=''. Only the
  `discuss.channel` override actively unlinks empty messages. Admin
  can optionally unlink directly via `mail.message.unlink(ids)` from
  dev-mode list view / JSON-RPC — both outcomes satisfy the task.

## check.py must accept either unlink OR body-cleared

- Gate on body content, not record existence. The check iterates the
  `mail.message` rows where `model='blog.post' and res_id=post.id and
  message_type='comment' and subtype_id=mail.mt_comment`, strips
  tags, and requires:
  * No surviving row whose plain body contains 'BUY CHEAP' (the spam
    marker) — this is true both after unlink and after body='' blank.
  * Exactly one row whose plain body contains 'Great write-up' (the
    good-review marker) and is authored by the Reviewer Good partner.
- Do NOT assert on `len(all_msgs)` directly: chatter Delete leaves a
  zombie row; counting rows gives 2 even though only 1 is visible.

## Seeding public chatter comments on a mail.thread record

- Comments must be `message_type='comment'` AND
  `subtype_xmlid='mail.mt_comment'` to render on the chatter's public
  tab and be "deletable" by admin (the `editable` getter in
  `mail/static/src/core/common/message_model.js` returns True only
  for `message_type === 'comment'`).
- Seed uses
  `post.with_user(admin).sudo().message_post(
       body=..., author_id=<portal_partner>,
       message_type='comment', subtype_xmlid='mail.mt_comment')`
  for each of the two comments. Setting `author_id` explicitly makes
  the chatter display name read 'Reviewer Good' / 'Spam Bot' so the
  agent can disambiguate which to delete.
- Portal group users (`base.group_portal`) are enough — no need to
  grant them internal access. Their linked partners are what
  author_id points to.

## Oracle via JSON-RPC unlink (admin short-circuit)

- Oracle calls `mail.message.unlink([spam_id])` via
  `/web/dataset/call_kw`. Admin is super-user, `mail.message` has no
  access restriction that stops admin, so unlink returns synchronously
  and the spam row is gone.
- This is cleaner than driving the chatter DOM (two hover steps +
  overflow dropdown + confirm dialog) while still satisfying check.py
  since the postcondition accepts unlink as equivalent to body=''.

## Calibration — BU single-shot PASS in 22 steps / 121s

- BU solved the task single-shot. It (1) navigated to
  `/odoo/blog-post-pages`, (2) tripped the Website Preview redirect
  and had to click the **Blog Post** breadcrumb to get back to the
  backend form, (3) hovered the spam message via a JS `mouseover`
  dispatch, (4) clicked the Expand (`...`) button on the
  per-message action toolbar (`button[aria-label="Expand"]`), (5)
  clicked **Delete** in the dropdown, and (6) confirmed in the modal.
- The `Delete` menu item exposes `aria-label="Delete"` and
  `role="menuitem"`, which BU's element scorer locks onto
  immediately — same pattern as the forum upvote task
  (`aria-label="Upvote"` is similarly easy). Per `RESULT.md` on row
  477 (forum upvote), **aria-label surfaced actions are not a
  reliable hard-tier calibration**.
- The `Expand` overflow menu adds mild difficulty (one extra hover +
  click over a direct-visible trash icon), but BU's built-in
  mouse-over dispatch cleared it on step 19.
- F1 = 1.0 because expected_state is `[]` (no blog.post field
  changes) and check.py passed.

## Future hard-tier tightening ideas

- Seed THREE comments (one good, two spammy) and require the agent
  to delete BOTH spams without touching the legit review — the
  multi-step hover/expand loop compounds.
- Require the agent to ALSO archive a fourth follow-up spam on a
  sibling post — cross-post moderation in a single run.
- Remove the explicit "Expand" / "overflow menu" hint from prompt.md
  — BU has been observed to miss hidden-under-overflow actions when
  the prompt doesn't name them.

## Diff-engine quirk

- `expected_state.json` is `[]`: the moderation action does not
  change any tracked `blog.post` field. The only state change is in
  `mail.message`, which is untracked in state_spec.yaml because its
  match-key semantics (body as a Many2one-ish string) don't round-trip
  cleanly and because the check.py assertion is more precise.
- Strict PASS requires `state_diff_f1 = 1.0` with empty expected =
  empty observed; this holds as long as `state_spec.yaml` ignores all
  chatter/mail-thread computed fields (message_ids, website_message_ids,
  message_* counters, activity_ids) — those flip as a side effect of
  message_post/unlink and would break strict PASS otherwise.
