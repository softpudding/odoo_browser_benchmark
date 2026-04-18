ROW: 300
TASK_ID: website_blog.create_blog_with_two_posts_archive_one
DIFFICULTY: medium
SUMMARY: Create blog 'Bench Insights' + 2 published posts, then archive only March Notes (active=False, kept in DB)
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## website_blog.create_blog_with_two_posts_archive_one

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | website_blog |
| **Workflow** | Agent must create blog 'Bench Insights' from scratch, then create two blog.posts under it ('April Update' and 'March Notes', both published), then open March Notes and archive it via Action > Archive (active=False) without deleting it or touching April Update. |
| **Capability tested** | Multi-record creation followed by selective archive among siblings — tests attention to which of two newly created records to archive. |
| **Notes** | Browser-use created blog + both published posts correctly (9/12 atomic edits matched) but failed to archive March Notes within the 360s budget — exactly the predicted "selective archive among siblings" failure mode. Calibration matches: medium-tier failure as expected. State diff for the archived post serializes False booleans as `null` on a `create` op (active/is_published/website_published all show `norm_value: null`); expected_state.json must mirror that. |
