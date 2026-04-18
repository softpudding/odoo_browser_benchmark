# Cookbook notes — website_blog.create_post_with_cta_seo_schedule

Reinforced and new Odoo 19 quirks picked up while building this medium task:

## blog.post content field is `content` (Html), not arch_db

- The writable body field on `blog.post` is `content` (`fields.Html`,
  `sanitize=False`, `translate=html_translate`). `arch_db` belongs to
  `ir.ui.view`, not to `blog.post` — don't confuse them.
- `content` is **not** declared in `state_spec.yaml.fields` in this task
  because free-form rich HTML produces noisy diffs (every whitespace or
  attribute reordering becomes an edit). Validation of the CTA goes
  through `check.py` with a regex that accepts any `<a ... href='/shop'
  ...>Learn More</a>` pattern regardless of class list or attribute
  order.

## Scheduled future date keeps is_published / website_published False

- Writing `published_date` (UTC Datetime) to a future moment and leaving
  `is_published=False` puts the post in the *scheduled* state: the
  Published toggle stays OFF and nothing flips to True server-side until
  a cron sweeps the queue.
- For a fresh create-and-schedule run, the state diff therefore emits
  `is_published` and `website_published` as `create` / `norm_value: null`
  (NOT `false`) — same null-vs-false quirk already documented for the
  archive case. `expected_state.json` must use `null` here.
- `post_date` is a computed/inverse alias for `published_date`; writing
  either is enough. Checks should read whichever is populated
  (`post.published_date or post.post_date`).

## Optimize SEO dialog for blog.post is on the form, not only the frontend

- `blog.post` (via `website.seo.metadata` mixin) exposes
  `website_meta_title`, `website_meta_description`, `website_meta_keywords`,
  `is_seo_optimized`. On the `blog.post` form the canonical path to edit
  these is cog **Actions > Optimize SEO** (OptimizeSEODialog), same Owl
  dialog used on the frontend. Writing both meta fields auto-bumps
  `is_seo_optimized` False→True — list it in `ignore_fields` to avoid
  noise.
- Unlike `website_sale` (where the dialog only exists on the frontend
  shop page — see `website_sale.set_product_seo_title_meta`), here the
  dialog is reachable from the backend form via the cog Actions menu,
  because `BlogPostController` inherits `WebsiteSeoMetadataController` and
  the action is registered on `blog.post`.

## The "button block" distinction is semantically important

- A *Call-To-Action button* in the Odoo HTML editor is inserted via the
  `/snippets` `s_button` snippet: `<a class="btn btn-primary" href="...">
  Label</a>`. A plain link inside a paragraph is NOT a CTA button. The
  `check.py` regex in this task accepts any `<a>` with `href='/shop'`
  that encloses "Learn More" (case-insensitive), so both a button-styled
  snippet AND a hand-typed anchor satisfy the postcondition.
- Browser-use failure mode under 360 s: BU reliably handles the Optimize
  SEO dialog and the Publishing date field, but burns its entire step
  budget trying to drag the button snippet into the HTML editor. Typical
  end state: empty `<p></p>`. This is the natural calibration trap —
  stacking three unrelated surfaces where only the body-editor surface
  is non-trivial.

## Oracle pattern

JSON-RPC `create` on `blog.post` with:
- `content` containing the anchor HTML directly (bypass the editor),
- both `website_meta_*` fields set,
- `published_date` written as UTC (computed in JS from the target
  admin-local datetime — same helper pattern as
  `website_blog.edit_post_change_author_add_tags_schedule/oracle.py`),
- `is_published=false`, `website_published=false`.

This produces exactly the 6-edit state diff the BU run produces for the
non-body fields and gives a deterministic check.py-passing state.

## Seed: preserve or create `Bench News`

- The seed performs an idempotent upsert of the blog (`Bench News`) and
  deletes only prior posts titled `Bench Releases Q2 Features`, never
  the blog. `trace_spec.yaml` forbids `blog.blog.create` and
  `blog.blog.unlink` so the agent cannot take the "create a new blog"
  shortcut.
