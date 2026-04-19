# Result — website_blog.delete_comment_moderate

Row 482, hard tier (tier 3), website_blog moderation.

## Oracle

- Command: `uv run benchmark-eval run website_blog.delete_comment_moderate --agent oracle --headless`
- Outcome: **PASS** (strict PASS)
- StateDiffF1: **1.0** (0/0 atomic edits matched)
- Postcondition failures: **0**
- Wall clock: **14.4s**, 0 agent steps
- Writes: 14 non-forbidden, 0 forbidden
- Total API calls: 35
- Artifacts: `benchmark/reports/runs/website_blog.delete_comment_moderate__oracle__1776603465/`

Oracle logs in, navigates to `/odoo/blog-post-pages`, and uses
authenticated `/web/dataset/call_kw` to:
1. `blog.post.search_read` the seeded 'Bench Mod Post'.
2. Resolve `mail.mt_comment` subtype id via `ir.model.data`.
3. `mail.message.search_read` the two chatter comments on the post.
4. Identify the spam comment by body marker `BUY CHEAP`.
5. `mail.message.unlink` the spam row.
6. Sanity-read remaining comments.

Admin super-user bypass on `mail.message.unlink` is the accepted
oracle short-circuit; check.py accepts either unlink or body-cleared
as a valid end-state.

## Browser-Use (single-shot calibration)

- Command: `uv run benchmark-eval run website_blog.delete_comment_moderate --agent browser-use --headless`
- Outcome: **PASS** (strict PASS)
- StateDiffF1: **1.0** (0/0 atomic edits)
- Postcondition failures: **0**
- Wall clock: **120.9s**, 22 agent steps
- Writes: 55 non-forbidden, 0 forbidden
- Total API calls: 122
- Delete action confirmed via `custom:/mail/message/update_content: 1`
  trace entry.
- Artifacts: `benchmark/reports/runs/website_blog.delete_comment_moderate__browser-use__1776603544/`

BU's path: login → list view → accidentally landed on the Website
Preview twice → clicked the **Blog Post** breadcrumb to return to the
back-office form → hovered the Spam Bot comment via JS `mouseover`
dispatch → clicked the `button[aria-label="Expand"]` on the
per-message action toolbar → clicked the `role="menuitem" name="delete"`
Delete item in the dropdown → confirmed in `MessageConfirmDialog`.

## Calibration summary

Stated risk was **hard, ≤40% pass** (tier 3). Empirical: BU PASS
single-shot, F1=1.0, 22 steps / 121s. This task calibrates EASIER
than the stated hard target because:

1. `aria-label="Expand"` on the overflow button + `aria-label="Delete"`
   on the menu item expose the entire delete path to BU's element
   scorer (same dynamic as the forum `aria-label="Upvote"` in row 477).
2. Only ONE spam vs. ONE good comment — no multi-decoy
   disambiguation. The body-marker cue `BUY CHEAP` is obvious.
3. The confirmation dialog's "Delete" primary button is the default
   keyboard focus — agents that press Enter or click the primary
   button succeed.

Consistent with the project's calibration-risk acceptance policy for
website_blog (shared with row 430 `change_author_republish_post`,
which also PASSes BU single-shot), the task is kept as hard/tier-3
because (a) the chatter hover + overflow + confirm sequence is a
genuine deep-UI pattern not covered elsewhere in the benchmark,
(b) the oracle + postcondition machinery is stable, and (c) the
task is realistic (moderation is a common Odoo admin workflow).

## Calibration tightening (future work, not applied)

- Seed multiple spam comments to force a multi-click hover + expand
  + confirm loop.
- Remove "Expand" / overflow menu wording from prompt — BU fails
  more often when the affordance isn't named.
- Add a decoy lookalike good review (same author, slightly spammy
  body) to force disambiguation on body content, not author name.
