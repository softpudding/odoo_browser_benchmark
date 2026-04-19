"""Oracle for website_blog.create_post_with_cta_seo_schedule.

Use authenticated JSON-RPC to:
  1. Look up the seeded blog "Bench Tech Blog".
  2. Create a blog.post with name, blog_id, content (containing the
     call-to-action "Click here for details"), website_meta_title,
     website_meta_description, and a scheduled published_date.
  3. Make sure is_published / website_published remain False.

The published_date on blog.post is a Datetime stored as UTC. We convert
the target local datetime (2026-05-20 10:00:00) to the equivalent UTC
string using the browser's local timezone (which matches the admin's TZ
when running Playwright on the same host).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


BLOG_NAME = "Bench Tech Blog"
POST_NAME = "Bench New Feature Launch"
META_TITLE = "Bench New Feature"
META_DESCRIPTION = "Announcing our new bench feature"
CTA_TEXT = "Click here for details"
TARGET_LOCAL = "2026-05-20 10:00:00"


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages")
    page.wait_for_timeout(800)

    payload = {
        "blog_name": BLOG_NAME,
        "post_name": POST_NAME,
        "meta_title": META_TITLE,
        "meta_description": META_DESCRIPTION,
        "cta_text": CTA_TEXT,
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

            // 1. Look up the target blog.
            const blogs = await callKw({
                model: 'blog.blog',
                method: 'search_read',
                args: [[['name', '=', p.blog_name]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!blogs.length) {
                throw new Error('Seeded blog not found: ' + p.blog_name);
            }
            const blogId = blogs[0].id;

            // 2. Convert target local datetime -> UTC string.
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

            // 3. Compose HTML body that embeds the literal CTA text.
            const body = (
                '<p>Bench is launching a new feature.</p>' +
                '<p>' + p.cta_text + '</p>'
            );

            // 4. Create the post. Pass published_date as UTC datetime;
            //    keep is_published / website_published false.
            const postId = unwrap(await callKw({
                model: 'blog.post',
                method: 'create',
                args: [[{
                    name: p.post_name,
                    blog_id: blogId,
                    content: body,
                    website_meta_title: p.meta_title,
                    website_meta_description: p.meta_description,
                    published_date: utc,
                    is_published: false,
                    website_published: false,
                }]],
                kwargs: {},
            }));

            // 5. Re-read and sanity-check.
            const after = await callKw({
                model: 'blog.post',
                method: 'read',
                args: [[postId], [
                    'name', 'blog_id', 'content',
                    'website_meta_title', 'website_meta_description',
                    'published_date', 'post_date',
                    'is_published', 'website_published',
                ]],
                kwargs: {},
            });
            return JSON.stringify(after[0]);
        }""",
        payload,
    )
    print('Oracle wrote:', response)


run_oracle(oracle)
