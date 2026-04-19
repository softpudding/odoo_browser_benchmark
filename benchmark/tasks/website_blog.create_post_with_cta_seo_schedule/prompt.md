# Create a scheduled blog post with call-to-action and SEO metadata

Create a new blog post in the existing blog `Bench Tech Blog`, schedule it for a future publication date, add a specific call-to-action line inside its content, and fill SEO metadata (meta title + meta description). The post must stay **unpublished** (it is merely scheduled).

## Step 1 - Create the post

1. Open **Website > Site > Blog Posts** (or navigate to the Blog Posts back-office list at `/odoo/blog-post-pages`).
2. Click **New** to create a new blog post.
3. Set the post **Title** to `Bench New Feature Launch`.
4. Set the post **Blog** to the existing blog `Bench Tech Blog` (pick it from the dropdown — do NOT create a new blog).

## Step 2 - Add the call-to-action in the content

5. In the post's **Content** (the main body / rich text area of the post form), make sure the exact call-to-action text `Click here for details` appears somewhere in the body. You may type it as its own line / paragraph; as long as the exact string `Click here for details` is part of the saved content, it counts.

## Step 3 - Set the SEO metadata

6. Still on the post form, set the **Website meta title** to `Bench New Feature` and the **Website meta description** to `Announcing our new bench feature`. These fields live in the "Promote" / "Optimize SEO" dialog that you open from the top of the form (the Odoo SEO optimizer). You can also set them via the `website_meta_title` / `website_meta_description` fields on the form if the Promote dialog is not available — either path is acceptable as long as the saved values match exactly.

## Step 4 - Schedule the publishing date

7. In the "Publishing Options" group on the post form, set the **Publishing date** to `05/20/2026 10:00:00` (May 20, 2026 at 10:00 AM, admin local time).

## Step 5 - Save (but do NOT publish)

8. Save the form. The **Published** toggle must remain **off** — the post is scheduled, not published.

## Rules

- Post title must be exactly `Bench New Feature Launch`.
- Blog must be the existing `Bench Tech Blog` — do NOT create a new blog and do NOT pick the distractor blog `Bench Marketing Blog`.
- `website_meta_title` must be exactly `Bench New Feature`.
- `website_meta_description` must be exactly `Announcing our new bench feature`.
- Publishing date must be `2026-05-20 10:00:00` (admin local TZ).
- The content must contain the literal call-to-action text `Click here for details`.
- Do NOT publish the post. The Published toggle / `is_published` must stay False.
- Do NOT create any extra blog post. Exactly one post named `Bench New Feature Launch` must exist.
