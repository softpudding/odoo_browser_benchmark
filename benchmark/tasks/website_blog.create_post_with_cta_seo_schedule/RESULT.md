# website_blog.create_post_with_cta_seo_schedule — RESULT

## Oracle

- Command: `PYTHONPATH=. .venv/bin/benchmark-eval run website_blog.create_post_with_cta_seo_schedule --agent oracle --headless`
- Outcome: **PASS**
- StateDiffF1: **1.0** (precision=1.0, recall=1.0)
- Expected/observed/matching: 6/6/6 edits
- Postcondition failures: 0
- Wall clock: ~16.5 s
- Artifacts: `benchmark/reports/runs/website_blog.create_post_with_cta_seo_schedule__oracle__1776526706/`

## Browser-Use (single-shot BU calibration)

- Command: `PYTHONPATH=. .venv/bin/benchmark-eval run website_blog.create_post_with_cta_seo_schedule --agent browser-use --headless`
- Outcome: **FAIL** (strict FAIL)
- StateDiffF1: 0.0 (postcondition override — the raw diff match was 6/6, i.e. BU set name/blog/SEO fields correctly)
- Postcondition failures: **1** — `CTA button/link missing: expected an <a href='/shop'>Learn More</a> pattern in post content, got: Markup('\n\n<p></p>\n')`
- Wall clock: 360.0 s (hit task `time_limit_sec`)
- Gave-up: true (timeout)
- Writes: 70 non-forbidden, 0 forbidden
- Artifacts: `benchmark/reports/runs/website_blog.create_post_with_cta_seo_schedule__browser-use__1776526774/`

### Calibration summary

BU reliably handles the easier sub-steps (creating the post in the right
blog, filling the SEO dialog, leaving the post unpublished) but exhausts
its 360 s budget trying to insert a CTA **button block** with `href='/shop'`
in the content editor. The content field ends up empty. This is exactly
the intended failure mode: three unrelated surfaces (HTML editor snippet
drag, Optimize SEO dialog, Publishing date scheduler) stacked into one
medium task, with the body editor being the hard step.

State-diff calibration is clean: the 6 expected create-edits match BU's
observed edits exactly (name, blog_id, website_meta_title,
website_meta_description, is_published=null, website_published=null).
The only distinguishing signal between a correct and an incomplete run
is the `check.py` CTA regex, which is why the task lives or dies on the
postcondition rather than F1.
