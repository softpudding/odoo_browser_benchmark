"""Oracle for website_blog.create_post_with_cta_seo_schedule."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages")
    response = page.evaluate(
        """async () => {
            const unwrap = (value) => Array.isArray(value) ? value[0] : value;
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            let blogRes = await callKw({
                model: 'blog.blog',
                method: 'search_read',
                args: [[['name', '=', 'Bench Content Studio']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!blogRes.length) {
                throw new Error('target blog missing');
            }

            const postId = unwrap(await callKw({
                model: 'blog.post',
                method: 'create',
                args: [[{
                    name: 'Quarterly Launch Playbook',
                    blog_id: blogRes[0].id,
                    subtitle: 'Prepare your team before release day.',
                    content: '<p>Download the launch checklist now.</p>',
                    website_meta_title: 'Quarterly Launch Playbook | Bench Content',
                    website_meta_description: 'Download the launch checklist and prepare your release team.',
                    published_date: '2026-06-15 02:30:00',
                    is_published: false,
                    website_published: false,
                }]],
                kwargs: {},
            }));
            if (!postId) {
                throw new Error('post creation failed');
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
