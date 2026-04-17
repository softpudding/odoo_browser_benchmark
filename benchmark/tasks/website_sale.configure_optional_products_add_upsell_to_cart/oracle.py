"""Oracle for website_sale.configure_optional_products_add_upsell_to_cart."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/ecommerce-products")
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

            const mainRes = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', 'Docking Console']], ['id', 'product_variant_id']],
                kwargs: { limit: 1 },
            });
            const optionalRes = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', 'Protective Sleeve']], ['id', 'product_variant_id']],
                kwargs: { limit: 1 },
            });
            const websiteRes = await callKw({
                model: 'website',
                method: 'search_read',
                args: [[], ['id']],
                kwargs: { limit: 1 },
            });
            const userRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            if (!mainRes.length || !optionalRes.length || !websiteRes.length || !userRes.length) {
                throw new Error('missing product, website, or user');
            }
            const main = mainRes[0];
            const optional = optionalRes[0];
            const partnerId = userRes[0].partner_id[0];

            await callKw({
                model: 'product.template',
                method: 'write',
                args: [[main.id], { optional_product_ids: [[6, 0, [optional.id]]] }],
                kwargs: {},
            });
            await callKw({
                model: 'product.template',
                method: 'write',
                args: [[optional.id], { website_published: true }],
                kwargs: {},
            });
            await callKw({
                model: 'sale.order',
                method: 'create',
                args: [[{
                    partner_id: partnerId,
                    website_id: websiteRes[0].id,
                    origin: 'website upsell cart',
                    order_line: [
                        [0, 0, {
                            product_id: main.product_variant_id[0],
                            product_uom_qty: 1,
                            price_unit: 249.0,
                            name: 'Docking Console',
                        }],
                        [0, 0, {
                            product_id: optional.product_variant_id[0],
                            product_uom_qty: 1,
                            price_unit: 29.0,
                            name: 'Protective Sleeve',
                        }],
                    ],
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
