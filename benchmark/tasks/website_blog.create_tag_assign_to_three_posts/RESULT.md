ROW: 334
TASK_ID: website_blog.create_tag_assign_to_three_posts
DIFFICULTY: medium
SUMMARY: Create blog.tag 'Q2-2026' then bulk-assign it to three seeded posts (Post-A/B/C) via tag_ids m2m; distractor Post-D must stay untagged.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches (harder edge — BU created tag but added it to 0/3 posts before timing out)

DETAIL_SECTION:
## website_blog.create_tag_assign_to_three_posts

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (gave_up=True at 360s) |
| **F1** | 0.0 |
| **Odoo modules** | website_blog |
| **Workflow** | Create a new `blog.tag` named `Q2-2026` via `/odoo/blog-tags`, then loop through three seeded `blog.post` records (Post-A, Post-B, Post-C) and add the tag on each post's `tag_ids` m2m (many2many_tags widget). A fourth seeded post (Post-D) acts as a distractor that must remain untagged. |
| **Capability tested** | Tag creation + bulk m2m assignment across multiple records with a "do-not-touch-the-distractor" negative constraint. |
| **Notes** | BU successfully created the `Q2-2026` tag (1 matching create edit on `blog.tag`) and issued 172 writes total, but timed out with `steps=0 gave_up=True` at 360s without ever landing the tag on a single post. Postconditions flagged Post-A/B/C all missing the tag. Failure is harsher than the "forget one" trap predicted for row 321-style bulk tasks — BU never made it past the tag creation into the per-post loop, so calibration holds as "matches / harder edge". Distractor Post-D never received spurious tags (check confirmed clean). Oracle writes via JSON-RPC because `many2many_tags` autocomplete can be brittle under Playwright; BU's UI route is the authentic test of the failure mode. |
