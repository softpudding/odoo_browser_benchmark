"""Oracle for website_blog.schedule_post_future_date_unpublish.

Approach: log in, navigate to /odoo/blog-post-pages so the session is in
the backend website-blog context, then use authenticated JSON-RPC
`call_kw` to write the target end state directly onto the seeded post:

    is_published = False
    website_published = False
    published_date = <UTC datetime that renders as 2026-08-15 12:00:00
                      in the admin's local timezone>

The datetime widget on `post_date` and the `website_publish_button` pill
are both empirically fragile under Playwright (see ODOO19_PATTERNS.md
§website_blog archive + state-diff null-vs-false and
§create_post_with_cta_seo_schedule oracle `_set_post_date` helper).
Driving both via JSON-RPC is deterministic and mirrors what Odoo's
web client ultimately persists through `web_save` — the state diff
emits the same `op: "set"` entries either way.

The browser-use agent is still required to perform the *UI* workflow
(pill click + datetime input); check.py + state diff validate the
resulting DB state.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


POST_NAME = "Bench Future Post"
# Admin's local-TZ wallclock target. The JS side resolves admin tz
# at runtime and sends the UTC equivalent as the ORM datetime string.
TARGET_LOCAL = "2026-08-15 12:00:00"


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages")
    page.wait_for_timeout(1000)

    payload = {
        "post_name": POST_NAME,
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

            // --- 1. Locate the seeded post. -------------------------------
            const posts = await callKw({
                model: 'blog.post',
                method: 'search_read',
                args: [[['name', '=', p.post_name]],
                       ['id', 'is_published', 'website_published',
                        'published_date', 'post_date']],
                kwargs: { limit: 1 },
            });
            if (!posts.length) {
                throw new Error('Seeded post not found: ' + p.post_name);
            }
            const postId = posts[0].id;

            // --- 2. Resolve admin timezone via login lookup (robust). ----
            const adminRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['tz']],
                kwargs: { limit: 1 },
            });
            let tzName = (adminRes?.[0]?.tz) || 'UTC';
            if (!tzName) tzName = 'UTC';

            // --- 3. Build UTC datetime string from admin-local target. ----
            // Parse "YYYY-MM-DD HH:MM:SS" as wallclock in admin's tz and
            // convert to UTC via Intl.
            const parseLocalAsUTC = (localStr, tz) => {
                const [datePart, timePart] = localStr.split(' ');
                const [Y, M, D] = datePart.split('-').map(Number);
                const [h, m, s] = (timePart || '00:00:00').split(':').map(Number);
                // Construct a 'probe' UTC instant that corresponds to these
                // wallclock numbers interpreted *as UTC*. Measure the tz's
                // offset at that instant and shift it back to get the real
                // UTC instant that prints as the desired wallclock in tz.
                const probeUTC = Date.UTC(Y, M - 1, D, h, m, s);
                const fmt = new Intl.DateTimeFormat('en-US', {
                    timeZone: tz,
                    year: 'numeric', month: '2-digit', day: '2-digit',
                    hour: '2-digit', minute: '2-digit', second: '2-digit',
                    hour12: false,
                });
                const parts = fmt.formatToParts(new Date(probeUTC));
                const get = (t) => parts.find(pt => pt.type === t)?.value;
                const tzY = Number(get('year'));
                const tzM = Number(get('month'));
                const tzD = Number(get('day'));
                let tzh = Number(get('hour'));
                if (tzh === 24) tzh = 0;
                const tzm = Number(get('minute'));
                const tzs = Number(get('second'));
                const shown = Date.UTC(tzY, tzM - 1, tzD, tzh, tzm, tzs);
                const offsetMs = shown - probeUTC;
                const realUTC = probeUTC - offsetMs;
                const d = new Date(realUTC);
                const pad = (n) => String(n).padStart(2, '0');
                return `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())} ${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())}`;
            };
            const utcStr = parseLocalAsUTC(p.target_local, tzName);

            // --- 4. Write target end state. -------------------------------
            await callKw({
                model: 'blog.post',
                method: 'write',
                args: [[postId], {
                    is_published: false,
                    website_published: false,
                    published_date: utcStr,
                }],
                kwargs: {},
            });

            // --- 5. Sanity re-read. ---------------------------------------
            const after = await callKw({
                model: 'blog.post',
                method: 'read',
                args: [[postId], ['is_published', 'website_published',
                                   'published_date', 'post_date']],
                kwargs: {},
            });
            return { utcStr, tzName, after: after[0] };
        }""",
        payload,
    )
    print('Oracle wrote:', response)


run_oracle(oracle)
