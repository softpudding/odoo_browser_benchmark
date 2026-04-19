# Change the author of a published blog post

The published blog post `Bench Blog Post` is authored by the admin user. Reassign it to the internal user `Bench Editor` while keeping it published.

## Steps

1. Open **Website > Site > Blog Posts** (or navigate to the Blog Posts back-office list at `/odoo/blog-post-pages`).
2. Open the existing blog post titled `Bench Blog Post` (it lives in the blog `Bench News`).
3. In the backend form, locate the **Author** many2one field (in the "Publishing Options" group on the right-hand side of the form).
4. Change the **Author** from the current value (admin / `Mitchell Admin`) to `Bench Editor`. Pick the existing `Bench Editor` entry from the autocomplete dropdown — do NOT create a new contact or user.
5. **Save** the form.

## Rules

- The post **must remain published** when you finish. Do NOT click the Unpublish toggle or otherwise flip `Published` to off.
- The new Author must be the existing internal user `Bench Editor` (the partner linked to the user whose login is `bench_editor`). Do not pick any other partner/contact, and do not create a new one.
- Do NOT change the post's title, blog, subtitle, or body content.
- Do NOT change the Publishing date.
- Do NOT delete, duplicate, or archive the post. Exactly one post named `Bench Blog Post` must remain at the end.
