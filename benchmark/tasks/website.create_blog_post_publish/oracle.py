"""Oracle for website.create_blog_post_publish."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/blogs")
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
                args: [[['name', '=', 'Our blog']], ['id']],
                kwargs: { limit: 1 },
            });
            let blogId;
            if (blogRes.length) {
                blogId = blogRes[0].id;
            } else {
                blogId = unwrap(await callKw({
                    model: 'blog.blog',
                    method: 'create',
                    args: [[{ name: 'Our blog' }]],
                    kwargs: {},
                }));
            }

            const postId = unwrap(await callKw({
                model: 'blog.post',
                method: 'create',
                args: [[{
                    name: 'Product Launch Announcement',
                    blog_id: blogId,
                    subtitle: 'Announcing our newest product lineup for Q2.',
                    content: '<p>Announcing our newest product lineup for Q2.</p>',
                    is_published: true,
                }]],
                kwargs: {},
            }));
            return 'ok:' + postId;
        }""",
    )
    if not response or not response.startswith("ok"):
        raise RuntimeError(response)


run_oracle(oracle)
