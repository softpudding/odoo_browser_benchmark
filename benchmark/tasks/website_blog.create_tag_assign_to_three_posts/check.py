"""Postcondition checks for website_blog.create_tag_assign_to_three_posts.

Validates:
1. blog.tag 'Q2-2026' exists (exactly one).
2. blog posts Post-A, Post-B, Post-C all carry the tag.
3. Distractor post Post-D does NOT carry the tag.
4. No extra post was created / no post was archived.
5. Post titles and blog unchanged from seed.
6. Posts remain unpublished.
"""


BLOG_NAME = "Harbor Quarterly"
TAG_NAME = "Q2-2026"
TARGET_POSTS = ["Post-A", "Post-B", "Post-C"]
DISTRACTOR_POST = "Post-D"
ALL_POSTS = TARGET_POSTS + [DISTRACTOR_POST]


def check(env):
    failures = []

    tags = env["blog.tag"].search([("name", "=", TAG_NAME)])
    if not tags:
        return [f"blog.tag '{TAG_NAME}' not found"]
    if len(tags) > 1:
        failures.append(
            f"Expected exactly one blog.tag '{TAG_NAME}', found {len(tags)}"
        )
    tag = tags[:1]

    for name in TARGET_POSTS:
        post = env["blog.post"].with_context(active_test=False).search(
            [("name", "=", name)], limit=1,
        )
        if not post:
            failures.append(f"Post '{name}' missing")
            continue
        if not post.active:
            failures.append(f"Post '{name}' was archived")
        if tag.id not in post.tag_ids.ids:
            tag_names = post.tag_ids.mapped("name")
            failures.append(
                f"Post '{name}' missing tag '{TAG_NAME}'; "
                f"tags are {tag_names!r}"
            )
        if post.is_published or post.website_published:
            failures.append(
                f"Post '{name}' must remain unpublished "
                f"(is_published={post.is_published}, "
                f"website_published={post.website_published})"
            )
        if not post.blog_id or post.blog_id.name != BLOG_NAME:
            failures.append(
                f"Post '{name}' blog is {post.blog_id.name!r}, "
                f"expected {BLOG_NAME!r}"
            )

    distractor = env["blog.post"].with_context(active_test=False).search(
        [("name", "=", DISTRACTOR_POST)], limit=1,
    )
    if not distractor:
        failures.append(f"Distractor post '{DISTRACTOR_POST}' missing")
    else:
        if tag.id in distractor.tag_ids.ids:
            failures.append(
                f"Distractor post '{DISTRACTOR_POST}' must NOT carry tag "
                f"'{TAG_NAME}'"
            )

    # No extra post created with any of these names
    total_posts = env["blog.post"].with_context(active_test=False).search_count(
        [("name", "in", ALL_POSTS)],
    )
    if total_posts != len(ALL_POSTS):
        failures.append(
            f"Expected exactly {len(ALL_POSTS)} seeded posts present, "
            f"found {total_posts}"
        )

    return failures
