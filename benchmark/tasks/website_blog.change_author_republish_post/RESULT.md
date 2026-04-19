# Result — website_blog.change_author_republish_post

## Oracle

- **Verdict:** PASS
- **F1:** 1.0 (1/1 atomic edits matched, 0 postcondition failures)
- **Wall clock:** 19.0s
- **Writes:** 11 non-forbidden, 0 forbidden
- **Total API calls:** 31

Oracle opens `/odoo/blog-post-pages`, uses authenticated `/web/dataset/call_kw`
to look up the seeded `Bench Blog Post`, resolve `bench_editor`'s `partner_id`,
and `write({'author_id': partner_id})`. Published flags are left untouched.

## Browser-Use

- **Verdict:** PASS
- **F1:** 1.0 (1/1 atomic edits matched, 0 postcondition failures)
- **Wall clock:** 79.6s (single-shot)
- **Writes:** 37 non-forbidden, 0 forbidden
- **Total API calls:** 84

BU completed the task on first attempt, matching the calibration target: a
top-level many2one swap on an already-published post is within tier-2 medium
budget. No retry required.

## Calibration note

This task is intentionally **not** BU-failing — it provides a clean
medium-difficulty single-field datapoint (contrast with
`website_blog.edit_post_change_author_add_tags_schedule` which layers Author
+ two tags + scheduled date and does fail BU).
