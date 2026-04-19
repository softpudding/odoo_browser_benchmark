"""Oracle for website_blog.change_author_republish_post.

Approach: log in, navigate to /odoo/blog-post-pages so the session is in
the backend website-blog context, then use authenticated /web/dataset/call_kw
to write author_id on the seeded post. is_published / website_published
remain True (untouched). This mirrors what the browser client does under
the hood (web_save / write).

blog.post.author_id is a Many2one to res.partner — we pass the
res.partner.id that corresponds to the seeded user's partner_id.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


POST_NAME = "Bench Blog Post"
EDITOR_LOGIN = "bench_editor"


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages")
    page.wait_for_timeout(1000)

    payload = {
        "post_name": POST_NAME,
        "editor_login": EDITOR_LOGIN,
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

            // 1. Find the seeded post.
            const posts = await callKw({
                model: 'blog.post',
                method: 'search_read',
                args: [[['name', '=', p.post_name]],
                       ['id', 'author_id', 'is_published', 'website_published']],
                kwargs: { limit: 1 },
            });
            if (!posts.length) {
                throw new Error('Seeded post not found: ' + p.post_name);
            }
            const postId = posts[0].id;

            // 2. Find Bench Editor's partner via the user record.
            const editorUsers = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', p.editor_login]], ['id', 'partner_id']],
                kwargs: { limit: 1 },
            });
            if (!editorUsers.length) {
                throw new Error('Seeded user not found: ' + p.editor_login);
            }
            const editorPartnerId = unwrap(editorUsers[0].partner_id);

            // 3. Write the author_id. Do NOT touch is_published /
            //    website_published — seed already set them True.
            await callKw({
                model: 'blog.post',
                method: 'write',
                args: [[postId], { author_id: editorPartnerId }],
                kwargs: {},
            });

            // 4. Sanity re-read.
            const after = await callKw({
                model: 'blog.post',
                method: 'read',
                args: [[postId],
                       ['author_id', 'is_published', 'website_published']],
                kwargs: {},
            });
            return JSON.stringify(after[0]);
        }""",
        payload,
    )
    print('Oracle wrote:', response)


run_oracle(oracle)
