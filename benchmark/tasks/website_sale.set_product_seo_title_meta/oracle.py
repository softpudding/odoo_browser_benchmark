"""Oracle for website_sale.set_product_seo_title_meta.

Uses a JSON-RPC bypass to write website_meta_title and website_meta_description
directly on the seeded product.template. The browser-use agent must still solve
via the UI (Site > Optimize SEO dialog on the product's shop page), but the
oracle takes the deterministic path.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/ecommerce-products")

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

            const hits = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', 'Bench SEO Widget']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!hits.length) {
                throw new Error('Bench SEO Widget product not found');
            }
            const productId = hits[0].id;

            await callKw({
                model: 'product.template',
                method: 'write',
                args: [[productId], {
                    website_meta_title: 'Buy Bench SEO Widget Online',
                    website_meta_description: 'Premium widget for benchmarking with fast delivery.',
                }],
                kwargs: {},
            });
            return 'ok:' + productId;
        }""",
    )
    if not response or not str(response).startswith("ok"):
        raise RuntimeError(response)


run_oracle(oracle)
