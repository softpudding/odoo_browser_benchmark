# Cookbook notes — website_blog.create_tag_assign_to_three_posts

## blog.tag backend menu + form

- URL path: `/odoo/blog-tags` (action `website_blog.action_tags`,
  menu under Website > Site > Blog Tags, groups=`website.group_website_designer`).
- Tag form exposes `name` (required, UNIQUE), `category_id`, `color`
  (color_picker), plus a reverse m2m `post_ids` labeled "Used in:".
  The reverse field is tempting for "select all posts" shortcuts —
  always add a distractor post when the prompt specifies "exactly N posts".
- `_name_uniq` constraint on `blog.tag.name` — seed must delete any
  stale tag before recreating, otherwise oracle/seed raises
  `UniqueViolation`.

## blog.post.tag_ids widget

- Declared `fields.Many2many('blog.tag', string='Tags')`.
- Rendered as `widget="many2many_tags"` in
  `website_blog/views/website_pages_views.xml`; standard autocomplete
  dropdown with chip badges.
- `add_many2many_tag(page, 'tag_ids', 'Q2-2026')` from oracle_helpers
  works for this widget.

## Calibration — bulk m2m with distractor

Pattern mirrors `hr.create_department_assign_manager_three_employees`
(row 321): BU tends to drop one record in an N-record loop. Here BU
failed *harder* than predicted — it got the tag created but never
managed to land it on a single post within 360s. Likely causes:
after saving the tag, the form navigates to the tag's detail view and
BU starts exploring the reverse `post_ids` field instead of returning
to the blog.post list. Prompt explicitly says "Go back to the Blog
Posts back-office list" to push BU away from the tag form's reverse
m2m shortcut, but BU still burned budget navigating.

Key design lever: keeping the tag creation as Step 1 (before the loop)
naturally tempts BU into a detour via the tag form's "Used in:" field,
which is the ideal distractor trap for this workflow family.

## Oracle via JSON-RPC

The `many2many_tags` autocomplete is reliable in real browsers but
flaky under headless Playwright on some runs (dropdown positioning,
timing). Oracle writes `tag_ids: [[4, tagId]]` via authenticated
`call_kw` — same end DB state as the UI path, with no flakes.
