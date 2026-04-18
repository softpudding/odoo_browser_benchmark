"""Oracle for website.set_page_seo_fields.

Uses a JSON-RPC bypass to write website_meta_title, website_meta_description,
and website_meta_keywords directly on the seeded website.page. The browser-use
agent must still solve via the UI (Site > Promote / Optimize SEO dialog on the
page), but the oracle takes the deterministic path.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/website")

    response = page.evaluate(
        """async () => {
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

            const hits = await callKw({
                model: 'website.page',
                method: 'search_read',
                args: [[['url', '=', '/bench-seo-page']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!hits.length) {
                throw new Error('Bench SEO Page not found');
            }
            const pageId = hits[0].id;

            await callKw({
                model: 'website.page',
                method: 'write',
                args: [[pageId], {
                    website_meta_title: 'Bench SEO Meta Title',
                    website_meta_description: 'Bench SEO meta description text.',
                    website_meta_keywords: 'bench, seo, odoo',
                }],
                kwargs: {},
            });
            return 'ok:' + pageId;
        }""",
    )
    if not response or not str(response).startswith("ok"):
        raise RuntimeError(response)


run_oracle(oracle)
