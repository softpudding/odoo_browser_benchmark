"""Oracle for website_blog.create_tag_assign_to_three_posts.

Use authenticated JSON-RPC to:
  1. Create blog.tag 'Q2-2026'.
  2. Write tag_ids on the three target posts (Post-A/B/C),
     leaving Post-D untouched.

This bypasses the many2many_tags autocomplete (which has proven brittle
under Playwright on some runs) but produces the exact same DB state the
browser-use agent is expected to reach through the UI.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


TAG_NAME = "Q2-2026"
TARGET_POSTS = ["Post-A", "Post-B", "Post-C"]


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages")
    page.wait_for_timeout(800)

    payload = {
        "tag_name": TAG_NAME,
        "post_names": TARGET_POSTS,
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

            // 1. Create the tag (fail if it already exists — seed guarantees absence).
            const existing = await callKw({
                model: 'blog.tag',
                method: 'search_read',
                args: [[['name', '=', p.tag_name]], ['id']],
                kwargs: { limit: 1 },
            });
            let tagId;
            if (existing.length) {
                tagId = existing[0].id;
            } else {
                tagId = unwrap(await callKw({
                    model: 'blog.tag',
                    method: 'create',
                    args: [[{ name: p.tag_name }]],
                    kwargs: {},
                }));
            }

            // 2. Find the three target posts.
            const posts = await callKw({
                model: 'blog.post',
                method: 'search_read',
                args: [[['name', 'in', p.post_names]], ['id', 'name']],
                kwargs: {},
            });
            const byName = {};
            for (const row of posts) byName[row.name] = row.id;
            for (const name of p.post_names) {
                if (!byName[name]) throw new Error('Missing seeded post: ' + name);
            }

            // 3. For each target post, add the tag via (4, tagId).
            for (const name of p.post_names) {
                await callKw({
                    model: 'blog.post',
                    method: 'write',
                    args: [[byName[name]], { tag_ids: [[4, tagId]] }],
                    kwargs: {},
                });
            }

            return 'ok';
        }""",
        payload,
    )
    if response != "ok":
        raise RuntimeError(f"Oracle JSON-RPC returned: {response}")


run_oracle(oracle)
