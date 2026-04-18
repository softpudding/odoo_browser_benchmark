"""Oracle for website_blog.create_blog_with_two_posts_archive_one.

Logs in, navigates to the backend Blogs context, then uses authenticated
JSON-RPC to:
  1. Create blog 'Bench Insights'.
  2. Create blog.post 'April Update' (published, active).
  3. Create blog.post 'March Notes' (published, active) — both under the new blog.
  4. Archive (active=False) March Notes via action_archive.

Mirrors what the browser client does (web_save + action_archive).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


BLOG_NAME = "Bench Insights"
POST_APRIL = "April Update"
POST_MARCH = "March Notes"


def oracle(page):
    login(page)
    navigate(page, "/odoo/blogs")
    page.wait_for_timeout(800)

    payload = {
        "blog_name": BLOG_NAME,
        "post_april": POST_APRIL,
        "post_march": POST_MARCH,
    }

    result = page.evaluate(
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

            // 1. Create the blog
            const blogId = unwrap(await callKw({
                model: 'blog.blog',
                method: 'create',
                args: [[{ name: p.blog_name }]],
                kwargs: {},
            }));

            // 2. Create April Update — published
            const aprilId = unwrap(await callKw({
                model: 'blog.post',
                method: 'create',
                args: [[{
                    name: p.post_april,
                    blog_id: blogId,
                    is_published: true,
                    website_published: true,
                }]],
                kwargs: {},
            }));

            // 3. Create March Notes — published, then archive
            const marchId = unwrap(await callKw({
                model: 'blog.post',
                method: 'create',
                args: [[{
                    name: p.post_march,
                    blog_id: blogId,
                    is_published: true,
                    website_published: true,
                }]],
                kwargs: {},
            }));

            // 4. Archive March Notes
            await callKw({
                model: 'blog.post',
                method: 'action_archive',
                args: [[marchId]],
                kwargs: {},
            });

            // Sanity: re-read both
            const after = await callKw({
                model: 'blog.post',
                method: 'read',
                args: [[aprilId, marchId],
                       ['name', 'active', 'is_published', 'website_published',
                        'blog_id']],
                kwargs: { context: { active_test: false } },
            });
            return JSON.stringify({
                blog_id: blogId,
                april_id: aprilId,
                march_id: marchId,
                after,
            });
        }""",
        payload,
    )
    print("Oracle wrote:", result)


run_oracle(oracle)
