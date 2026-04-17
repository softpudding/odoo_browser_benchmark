"""Oracle for website_blog.create_post_with_cover_tag_publish."""

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
                args: [[['name', '=', 'Harbor Newsroom']], ['id']],
                kwargs: { limit: 1 },
            });
            let blogId;
            if (blogRes.length) {
                blogId = blogRes[0].id;
            } else {
                blogId = unwrap(await callKw({
                    model: 'blog.blog',
                    method: 'create',
                    args: [[{ name: 'Harbor Newsroom' }]],
                    kwargs: {},
                }));
            }

            let tagRes = await callKw({
                model: 'blog.tag',
                method: 'search_read',
                args: [[['name', '=', 'Operations Spotlight']], ['id']],
                kwargs: { limit: 1 },
            });
            let tagId;
            if (tagRes.length) {
                tagId = tagRes[0].id;
            } else {
                tagId = unwrap(await callKw({
                    model: 'blog.tag',
                    method: 'create',
                    args: [[{ name: 'Operations Spotlight' }]],
                    kwargs: {},
                }));
            }

            const postId = unwrap(await callKw({
                model: 'blog.post',
                method: 'create',
                args: [[{
                    name: 'Harbor Notes Rollout',
                    blog_id: blogId,
                    subtitle: 'Dock updates for the late-summer operations release.',
                    website_published: true,
                }]],
                kwargs: {},
            }));
            await callKw({
                model: 'blog.tag',
                method: 'write',
                args: [[tagId], {
                    post_ids: [[4, postId]],
                }],
                kwargs: {},
            });
            await callKw({
                model: 'blog.post',
                method: 'write',
                args: [[postId], {
                    cover_properties: '{"background-image": "url(\\'/website_blog/static/src/img/cover_1.jpg\\')", "resize_class": "o_record_has_cover o_half_screen_height", "opacity": "0"}',
                }],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
