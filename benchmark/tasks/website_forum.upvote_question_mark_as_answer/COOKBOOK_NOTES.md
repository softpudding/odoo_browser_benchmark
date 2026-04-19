# Cookbook notes — website_forum.upvote_question_mark_as_answer

New Odoo 19 quirks discovered (and reinforced) while building this medium
task. Merged into `ODOO19_PATTERNS.md § website_forum`.

## `forum.post.vote` model

- The upvote caret-up arrow on the question page is rendered as
  `<button type="button" class="btn vote_up ..."
   data-href="/forum/<forum>/post/<post>/upvote" aria-label="Upvote" title="Upvote">`
  (template `website_forum.post_vote` in
  `forum_forum_templates_tools.xml`).
- Clicking it hits the JSON-RPC controller `post_upvote` which calls
  `forum.post.vote(upvote=True)`. That method creates a
  `forum.post.vote` row with:
  * `post_id` = question
  * `user_id` = admin (from env.uid via `default=lambda self: self.env.uid`)
  * `vote` = `'1'`
  * `forum_id` (related to post.forum_id, stored)
  * `recipient_id` (related to post.create_uid, stored)
- All 5 non-id fields become `create` edits in state-diff. Match key
  `(post_id, user_id, vote)` normalizes to
  `("How do I install?", "Mitchell Admin", "1")` — the vote field is
  a Selection string, not an int.

## Self-upvote + self-accept guards

- `/forum/<forum>/post/<post>/upvote` controller has
  `if request.env.uid == post.create_uid.id: return {'error': 'own_post'}`
  — identical guard shape to `/toggle_correct`. Admin bypasses karma but
  NOT the own-post guard.
- Therefore: tasks where admin upvotes a question AND accepts its answer
  must seed BOTH posts under a different user (benchbot). This task
  authors both question and answer under benchbot; admin is only the
  voter + accepter.

## Upvote button is aria-label-discoverable

- Unlike the Accept checkmark (`o_wforum_validate_toggler`, no aria-label
  — row 394 showed BU fails to find it), the upvote button DOES carry
  `aria-label="Upvote"`, making it trivially discoverable by BU's
  element-scoring LLM. This is WHY this task calibrates easier than
  row 394.
- Observed BU behavior: finds `aria-label=Upvote` and
  `aria-label=Mark as Best Answer` in a single step-8 action pair. No
  loop-detection nudges, no More-dropdown hunting.
- Conclusion for future forum tasks: if calibration requires BU FAIL,
  the Accept checkmark is the robust failure locus; the upvote caret
  is too easy.

## `forum.forum.mode='questions'` allows exactly 1 answer

- `mode='questions'` → one answer per question (enforced at template
  render time via `t-if` on the Your Answer block after an answer
  exists). Good for this task because we want the one seeded answer to
  be the only one the agent can Accept.
- `mode='discussions'` allows many — use for multi-answer distractor
  tasks (row 394).

## Karma grants in seed

- Admin grants NOT needed: `forum.post._compute_post_karma_rights`
  short-circuits on `self.env.is_admin()` and sets every `can_*` flag
  to True regardless of karma_upvote / karma_answer_accept_* / etc.
- Benchbot gets karma=5000 so benchbot's seeded question doesn't
  land in `state='pending'` (karma_post=3 threshold) and so answers
  survive post-moderation.

## State-diff match_key for forum.post.vote

- `(post_id, user_id, vote)` is uniquely sufficient for vote rows
  because `forum.post.vote._vote_uniq = unique(post_id, user_id)`.
  Adding `vote` in the match key makes the diff stable when a vote is
  changed from 1 to -1 to 0 via write (not just create).
- For this task only create+1 happens, so the match key collapses
  cleanly.

## `forum.post.vote` NOT NULL recipient_id

- `recipient_id` is `related="post_id.create_uid"` stored, so it fills
  automatically at create time. State-diff captures it as a `create`
  edit with the post author's display name ("Bench Bot" here) —
  include it in state_spec `fields` to lock it in.
