# Cookbook notes — website_blog.change_author_republish_post

Notes picked up while building this medium task (row 430).

## blog.post.author_id is a Many2one to res.partner (not res.users)

- `blog.post.author_id = fields.Many2one('res.partner', 'Author', default=lambda self: self.env.user.partner_id)`.
- When an internal user is created, their `partner_id` is auto-created and is
  the value to pass for `author_id`. The dropdown filter on the form is
  unrestricted (any partner is selectable), so seeding a user just for its
  linked partner is sufficient — no need to expose `bench_editor` through
  a group-based domain.

## Keeping the post published across the Author swap

- The form's **Unpublish** toggle is the only visible surface that can
  flip `is_published` / `website_published`. Writing `author_id` alone via
  `web_save` / JSON-RPC does NOT touch the published flags — seed
  initialises both to True and the agent only needs to change Author + Save.
- In `check.py`, assert `is_published=True` and `website_published=True`
  explicitly; they will NOT appear in the state diff because they do not
  change (pre = post = True). Only `author_id` shows as a single atomic
  edit, matching `expected_state.json`.

## State diff: single atomic edit, null-vs-false quirk not triggered

- Unlike **create-a-post-and-schedule** tasks (see `website_blog.create_post_with_cta_seo_schedule`),
  this is a **pure write on a pre-existing post** — so the state-diff engine
  emits exactly **one** `op: "set"` edit on `author_id`, no null-vs-false
  weirdness. `state_spec.yaml` tracks `author_id, is_published, website_published`
  but only `author_id` changes.

## Calibration — single-shot BU pass (medium, tier 2)

- BU passed single-shot in **79.6s**, F1=1.0, 0 postcondition failures, 37
  non-forbidden writes, 0 forbidden. This confirms the design target: a clean
  "open form, swap m2o, save" is a benign medium that fits the tier-2 band
  and **does not** need escalation to tier-3 traps (Author is a single top-level
  field in the Publishing Options group, not hidden behind a wizard or a tag
  chip).
- Matches the pattern in the sibling task
  `website_blog.edit_post_change_author_add_tags_schedule` where the author
  swap alone is trivial — that task adds tags + scheduled date to escalate
  difficulty. This task keeps it to just the author to give the benchmark
  a clean single-field calibration datapoint.

## Oracle via JSON-RPC

- Reused the JSON-RPC pattern from
  `website_blog.edit_post_change_author_add_tags_schedule/oracle.py`:
  `callKw` on `blog.post.write` with `{author_id: <partner_id>}` and no
  touching of published flags. 31 API calls total, all non-forbidden.
