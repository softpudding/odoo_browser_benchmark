"""Oracle for website_blog.edit_post_change_author_add_tags_schedule.

Approach: log in, visit /odoo/blog-post-pages so the session is in the
backend website-blog context, then use authenticated /web/dataset/call_kw
to write author_id, tag_ids, and published_date on the seeded post. This
mirrors what the browser client does under the hood (web_save / write).

We send 'published_date' (the underlying Datetime field) as an ISO UTC
string converted from the user's local timezone (admin's TZ as known to
the server). post_date is computed from published_date.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


POST_NAME = "Spring Planning Recap"
ALICE_LOGIN = "alice.authoress"
TAG_PLANNING = "Planning"
TAG_QUARTERLY = "Quarterly"

# 2026-04-25 09:00:00 in admin local time. We pass this to the server as
# a naive string with a timezone hint via the user_context so Odoo
# interprets it as local. The simplest reliable approach: just write the
# datetime in the admin TZ — the server will store it as UTC. To remain
# robust across TZs, we explicitly compute the UTC equivalent below in
# JS using Intl.
TARGET_LOCAL = "2026-04-25 09:00:00"


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages")
    page.wait_for_timeout(1000)

    payload = {
        "post_name": POST_NAME,
        "alice_login": ALICE_LOGIN,
        "tag_planning": TAG_PLANNING,
        "tag_quarterly": TAG_QUARTERLY,
        "target_local": TARGET_LOCAL,
    }

    response = page.evaluate(
        """async (p) => {
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

            // 1. Find the seeded post
            const posts = await callKw({
                model: 'blog.post',
                method: 'search_read',
                args: [[['name', '=', p.post_name]], ['id', 'author_id']],
                kwargs: { limit: 1 },
            });
            if (!posts.length) {
                throw new Error('Seeded post not found: ' + p.post_name);
            }
            const postId = posts[0].id;

            // 2. Find Alice's partner via her user record
            const aliceUsers = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', p.alice_login]], ['id', 'partner_id']],
                kwargs: { limit: 1 },
            });
            if (!aliceUsers.length) {
                throw new Error('Seeded user not found: ' + p.alice_login);
            }
            const alicePartnerId = Array.isArray(aliceUsers[0].partner_id)
                ? aliceUsers[0].partner_id[0]
                : aliceUsers[0].partner_id;

            // 3. Find tag IDs
            const tagRows = await callKw({
                model: 'blog.tag',
                method: 'search_read',
                args: [[['name', 'in', [p.tag_planning, p.tag_quarterly]]],
                       ['id', 'name']],
                kwargs: {},
            });
            const tagIds = tagRows.map(r => r.id);
            if (tagIds.length < 2) {
                throw new Error('Expected 2 tags, found ' + tagRows.length);
            }

            // 4. Compute the UTC datetime that, when displayed in the
            //    admin's local TZ, reads as 2026-04-25 09:00:00.
            //    Strategy: parse the target as if it were in the
            //    browser's local TZ (which equals the admin's TZ when
            //    we run via Playwright on the same host) and serialize
            //    to "YYYY-MM-DD HH:MM:SS" UTC.
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

            // 5. Write the changes. published_date is the storage field;
            //    post_date is computed/inverse from it.
            await callKw({
                model: 'blog.post',
                method: 'write',
                args: [[postId], {
                    author_id: alicePartnerId,
                    tag_ids: [[6, 0, tagIds]],
                    published_date: utc,
                }],
                kwargs: {},
            });

            // 6. Sanity: re-read to confirm.
            const after = await callKw({
                model: 'blog.post',
                method: 'read',
                args: [[postId], ['author_id', 'tag_ids', 'published_date',
                                   'post_date', 'is_published']],
                kwargs: {},
            });
            return JSON.stringify(after[0]);
        }""",
        payload,
    )
    print('Oracle wrote:', response)


run_oracle(oracle)
