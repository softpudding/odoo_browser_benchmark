Create a scheduled blog post with a CTA button and SEO metadata.

1. Open the Blog app (`/odoo/blogs`). In the Blog kanban, pick the blog `Bench News`.
2. Create a new blog post with this exact title: `Bench Releases Q2 Features`.
3. In the post body, add a CTA button block labeled `Learn More` whose link target is `/shop` (i.e. the button's href must be `/shop`). The label and the link are both required.
4. Open the **Optimize SEO** dialog (via the form's cog **Actions > Optimize SEO**, or via the page's Optimize SEO entry point) and set:
   - **Meta Title**: `Q2 Releases - Bench`
   - **Meta Description**: `Read about our Q2 release highlights and what it means for customers.`
   Save the SEO dialog.
5. Set the post's **Publishing date** (`Publishing date` field in the Publishing Options group) to `05/20/2026 09:00:00`. This is in the future, so the post is scheduled, not published now.
6. Save the post. Do NOT publish it — the Published toggle must remain OFF.

Rules:
- Use the existing blog `Bench News`. Do NOT create another blog.
- Create exactly ONE post named `Bench Releases Q2 Features`.
- The post must remain unpublished (scheduled); the Published toggle stays OFF.
- The CTA button's href must be exactly `/shop`.
- Both the SEO Meta Title and Meta Description must be set via the Optimize SEO dialog.
