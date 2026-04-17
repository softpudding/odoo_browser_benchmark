"""Seed for project_todo.duplicate_note_retag_archive_original."""


TARGET_NAME = "Welcome Administrator!"
DISTRACTOR_NAME = "Welcome Administrator West"
FOLLOW_UP_NAME = "Welcome Administrator Follow-up"
ORIGINAL_TAG = "Needs Review"
FOLLOW_UP_TAG = "Harbor Ops"


def setup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", [DISTRACTOR_NAME, FOLLOW_UP_NAME]),
    ]).unlink()

    review_tag = env["project.tags"].search([("name", "=", ORIGINAL_TAG)], limit=1)
    if not review_tag:
        review_tag = env["project.tags"].create({"name": ORIGINAL_TAG})

    harbor_tag = env["project.tags"].search([("name", "=", FOLLOW_UP_TAG)], limit=1)
    if not harbor_tag:
        harbor_tag = env["project.tags"].create({"name": FOLLOW_UP_TAG})

    user = env.user

    target = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ], limit=1)
    if target:
        target.write({
            "tag_ids": [(6, 0, [review_tag.id])],
            "active": True,
        })
    env["project.task"].create({
        "name": DISTRACTOR_NAME,
        "user_ids": [(6, 0, [user.id])],
        "tag_ids": [(6, 0, [review_tag.id])],
        "description": "<p>Leave this distractor note unchanged.</p>",
        "active": True,
    })
