# Unpublish and reschedule a blog post to a future date

The blog post **Bench Future Post** in blog **Bench News** is currently
published and live on the website. We need to pull it back off the live
site and reschedule it for a future release.

## Steps

1. Open **Website > Site > Blog Posts** (back-office list at
   `/odoo/blog-post-pages`).
2. Open the existing blog post titled `Bench Future Post` (it lives in
   the blog `Bench News`).
3. Unpublish the post. You can click the website indicator in the
   top-right of the form to go to the website preview, then toggle the
   publish switch OFF in the website systray.
4. In the Publishing Options group on the right-hand side, change the
   **Publishing date** (field label "Publishing date", internal name
   `post_date`) to `08/15/2026 12:00:00`. This date is in the future —
   it schedules the post instead of publishing it now.
5. **Save** the form.

## Rules

- The final state must have the post **unpublished**: the Published
  pill must be OFF, and both `is_published` and `website_published`
  must be False.
- The Publishing date must be exactly `2026-08-15 12:00:00` (admin's
  local timezone).
- Do NOT change the post's title, blog, author, subtitle, or body
  content.
- Do NOT delete, duplicate, or archive the post. Exactly one post
  named `Bench Future Post` must remain at the end.
- Do NOT create a new blog or a new post — edit the seeded one in
  place.
