"""Oracle for website_blog.create_post_with_cta_seo_schedule.

Uses authenticated JSON-RPC to:
  1. Locate the seeded blog 'Bench News'.
  2. Create a new blog.post with the CTA anchor in the body, both SEO
     fields, and a scheduled published_date (2026-05-20 09:00 admin TZ).
  3. Leave is_published / website_published False so the post stays queued.

The browser-use agent must still solve via the UI (Optimize SEO dialog
on a separate surface, drag/drop or insert the button snippet in the
HTML editor, schedule the future date via the Publishing date field).

`published_date` is the underlying stored Datetime (UTC) and `post_date`
is computed/inverse from it. Writing `published_date` is the canonical
way to schedule a blog post.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


BLOG_NAME = "Bench News"
POST_NAME = "Bench Releases Q2 Features"
CTA_HTML = (
    '<p>Announcing our Q2 release highlights.</p>'
    '<p><a class="btn btn-primary" href="/shop">Learn More</a></p>'
)
SEO_TITLE = "Q2 Releases - Bench"
SEO_DESCRIPTION = (
    "Read about our Q2 release highlights and what it means for customers."
)
TARGET_LOCAL = "2026-05-20 09:00:00"


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages")
    page.wait_for_timeout(800)

    payload = {
        "blog_name": BLOG_NAME,
        "post_name": POST_NAME,
        "cta_html": CTA_HTML,
        "seo_title": SEO_TITLE,
        "seo_description": SEO_DESCRIPTION,
        "target_local": TARGET_LOCAL,
    }

    response = page.evaluate(
        """async (p) => {
            const unwrap = (v) => Array.isArray(v) ? v[0] : v;
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const blogRes = await callKw({
                model: 'blog.blog',
                method: 'search_read',
                args: [[['name', '=', p.blog_name]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!blogRes.length) {
                throw new Error('Seeded blog missing: ' + p.blog_name);
            }

            // Compute UTC equivalent of the admin-local datetime.
            const [datePart, timePart] = p.target_local.split(' ');
            const [Y, Mo, D] = datePart.split('-').map(Number);
            const [H, Mi, S] = timePart.split(':').map(Number);
            const localDt = new Date(Y, Mo - 1, D, H, Mi, S);
            const pad = (n) => String(n).padStart(2, '0');
            const utc = (
                localDt.getUTCFullYear() + '-' +
                pad(localDt.getUTCMonth() + 1) + '-' +
                pad(localDt.getUTCDate()) + ' ' +
                pad(localDt.getUTCHours()) + ':' +
                pad(localDt.getUTCMinutes()) + ':' +
                pad(localDt.getUTCSeconds())
            );

            const postId = unwrap(await callKw({
                model: 'blog.post',
                method: 'create',
                args: [[{
                    name: p.post_name,
                    blog_id: blogRes[0].id,
                    content: p.cta_html,
                    website_meta_title: p.seo_title,
                    website_meta_description: p.seo_description,
                    published_date: utc,
                    is_published: false,
                    website_published: false,
                }]],
                kwargs: {},
            }));
            if (!postId) {
                throw new Error('post creation failed');
            }

            // Sanity read-back
            const after = await callKw({
                model: 'blog.post',
                method: 'read',
                args: [[postId], ['name', 'blog_id', 'content',
                                   'website_meta_title',
                                   'website_meta_description',
                                   'published_date', 'post_date',
                                   'is_published', 'website_published']],
                kwargs: {},
            });
            return 'ok:' + JSON.stringify(after[0]);
        }""",
        payload,
    )
    if not response or not str(response).startswith("ok"):
        raise RuntimeError(response)
    print('Oracle created:', response)


run_oracle(oracle)
