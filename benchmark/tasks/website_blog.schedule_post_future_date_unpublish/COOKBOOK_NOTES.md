# Cookbook notes — website_blog.schedule_post_future_date_unpublish

Hard-tier (row 461) task notes. This task deliberately pairs two
separately-fragile surfaces (publish pill + datetime widget) that are
both known to break BU on single-shot runs.

## Hard pattern: publish pill OFF + datetime widget, same save

- `blog.post` surfaces `is_published` through `widget="website_publish_button"`
  (Bootstrap pill in the form header). Toggling OFF flips both
  `is_published` and `website_published` via the `website.published.mixin`
  inverse — the diff engine emits TWO `op: "set"` edits on a
  single save. In `expected_state.json` both show `norm_value: null` (NOT
  `false`) — same null-vs-false quirk documented for archive/create
  flows, but in a `set` rather than `create` context (pre=True → post=null).
- `post_date` is the inverse alias of `published_date` (storage field is
  UTC Datetime). Writing either is enough; check.py reads
  `post.published_date or post.post_date`.
- The datetime widget's button-vs-input Owl swap is the well-known
  fragile anchor (see `create_post_with_cta_seo_schedule/oracle.py`
  `_set_post_date`). Oracles MUST focus the widget's button first to
  surface the `<input>`, then set value via the native setter + dispatch
  `input`/`change`, then press Enter to commit — plain `.fill()` misses
  the Owl parser and silently reverts.

## set-op null-vs-false quirk (new datapoint)

- Unlike `create_post_with_cta_seo_schedule` (where `is_published` is
  `op:"create"`, `norm_value: null`), this task transitions True→False on
  an already-existing post. The diff engine STILL normalizes False to
  `null` under the `set` op — i.e. the quirk is property of the engine's
  value normalizer, not of the create-vs-set code path. `expected_state.json`:
  ```json
  { "op": "set", "field": "is_published",       "norm_value": null }
  { "op": "set", "field": "website_published",  "norm_value": null }
  ```
  Encoding `false` instead of `null` drops F1 to 0 via a mirror-image
  "missing + extra" edit pair.

## Seed details

- Seed sets `published_date = datetime.utcnow()` on the fresh post so
  the record is genuinely live-now, not pre-scheduled. The agent's
  `post_date` write to `2026-08-15 12:00:00` is therefore a true
  *reschedule into the future* — combined with `is_published=False`
  this reproduces Odoo's "scheduled (queued)" state.
- Blog `Bench News` is shared across multiple `website_blog` tasks;
  cleanup never unlinks it, and seed is idempotent (re-activates if
  archived, creates if missing).

## Oracle: JSON-RPC single `write` covers all three fields

Driving the pill + datetime + save through Playwright is brittle even in
oracle mode, so the oracle uses authenticated `/web/dataset/call_kw`:
```js
await callKw({
    model: 'blog.post',
    method: 'write',
    args: [[postId], {
        is_published: false,
        website_published: false,
        published_date: utcStr,   // admin-local 12:00:00 → UTC via Intl
    }],
    kwargs: {},
});
```
The admin TZ is resolved at runtime (`res.users.login='admin'.tz`), and
the target wall-clock 2026-08-15 12:00:00 is converted to the real UTC
instant via a `probeUTC/offsetMs` dance with `Intl.DateTimeFormat` — same
idea as the helper in other website_blog oracles, but inlined so the
oracle is hermetic. 35 API calls, 13 writes, 0 forbidden.

## Calibration — hard (tier 3) confirmed

- **Oracle**: PASS, F1=1.0, 2/2 edits, 0 postcondition failures, 12–15s
  wall clock, 33–35 API calls, StrictClean=True. Reproducible across
  two consecutive runs on isolated DBs.
- **Browser-Use single-shot**: Observed 2/2 state-diff matches on
  `is_published`/`website_published` (BU DID toggle the pill off), and
  the trace shows BU wrote `post_date='2026-08-15 04:00:00'` UTC — i.e.
  it typed `12:00` in the widget and the Owl datetime service converted
  via the harness's browser local tz (PDT on this machine), storing
  **04:00 UTC** which renders as `04:00` in admin-local (tz=UTC on the
  benchmark admin). The check.py tz math flags this as
  `Publishing date (admin local) is 2026-08-15T04:00:00, expected
  2026-08-15T12:00:00` — exactly the intended hard-tier trap.
- The specific BU run we captured also had a transient `odoo-bin shell`
  infra failure (the `.conf` temp file was cleaned up by a concurrent
  worktree) that forced `state_diff_f1=0.0` via the
  "Postcondition check failed to return JSON" short-circuit in
  `eval.py:503-506`. Design-side verdict still holds: BU gets the pill
  right but the datetime wrong, matching the proven hard-tier calibration
  band (≤40% pass).

## Trace spec

- No `required_ops` — the BU client uses `web_save` which isn't a
  unique-success indicator; check.py is authoritative.
- `forbidden_ops`: `blog.post.unlink`, `blog.post.create`,
  `blog.blog.create/unlink`, `blog.post.action_archive` (the last
  blocks the "archive as a shortcut to unpublish" escape — archive
  auto-flips publish flags via the mixin, which would satisfy F1 but
  violate the "do not archive" rule).

## Distinct from neighbouring blog tasks

- Row 430 (`change_author_republish_post`): pure author swap, KEEPS
  published. No publish-flag edits in state diff.
- Row 358 (`create_post_with_cta_seo_schedule`): creates a fresh
  scheduled post from scratch (never-published → null flags on create).
- Row 461 (this task): unpublish an already-published post AND
  reschedule — the only task in the suite exercising the True→False
  transition on `is_published`/`website_published` of a pre-existing
  record simultaneously with a `post_date` future reschedule.
