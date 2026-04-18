"""Oracle for website.duplicate_page_rename_unpublish.

Logs in, navigates to the Website backend, then uses authenticated JSON-RPC
to:
  1. Find the seeded 'Bench Original' website.page.
  2. Call copy() on it (mirrors what the Pages list's Actions > Duplicate
     menu does in the browser).
  3. Write the new name/url on the copy and unpublish it.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


ORIGINAL_URL = "/bench-original"
DRAFT_NAME = "Bench Original Draft"
DRAFT_URL = "/bench-original-draft"


def oracle(page):
    login(page)
    navigate(page, "/odoo/website")
    page.wait_for_timeout(800)

    payload = {
        "original_url": ORIGINAL_URL,
        "draft_name": DRAFT_NAME,
        "draft_url": DRAFT_URL,
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

            // 1. Find the seeded original page.
            const originals = await callKw({
                model: 'website.page',
                method: 'search_read',
                args: [[['url', '=', p.original_url]], ['id', 'name']],
                kwargs: { limit: 1 },
            });
            if (!originals.length) {
                throw new Error('Original page not found at ' + p.original_url);
            }
            const originalId = originals[0].id;

            // 2. Duplicate the page (same entrypoint the Pages list's
            //    Actions > Duplicate menu uses).
            const copyId = unwrap(await callKw({
                model: 'website.page',
                method: 'copy',
                args: [[originalId]],
                kwargs: { default: {} },
            }));

            // 3. Rename the copy and unpublish it.
            await callKw({
                model: 'website.page',
                method: 'write',
                args: [[copyId], {
                    name: p.draft_name,
                    url: p.draft_url,
                    is_published: false,
                    website_published: false,
                }],
                kwargs: {},
            });

            const after = await callKw({
                model: 'website.page',
                method: 'read',
                args: [[originalId, copyId],
                       ['name', 'url', 'is_published', 'website_published']],
                kwargs: {},
            });
            return JSON.stringify({
                original_id: originalId,
                copy_id: copyId,
                after,
            });
        }""",
        payload,
    )
    print("Oracle wrote:", result)


run_oracle(oracle)
