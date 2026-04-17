"""Oracle for website_sale.configure_variant_publish_product."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/products")
    response = page.evaluate(
        """async () => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };
            const productRes = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', 'Field Pack Duffel']], ['id']],
                kwargs: { limit: 1 },
            });
            const attrRes = await callKw({
                model: 'product.attribute',
                method: 'search_read',
                args: [[['name', '=', 'Bench Size']], ['id']],
                kwargs: { limit: 1 },
            });
            const valuesRes = await callKw({
                model: 'product.attribute.value',
                method: 'search_read',
                args: [[['attribute_id', '=', attrRes.result[0].id], ['name', 'in', ['Carry-On', 'Weekender']]], ['id', 'name']],
                kwargs: {},
            });
            if (!productRes.result?.length || !attrRes.result?.length || valuesRes.result?.length !== 2) {
                return 'missing product or values';
            }
            const productId = productRes.result[0].id;
            const attrId = attrRes.result[0].id;
            const valueIds = valuesRes.result.map((v) => v.id);
            await callKw({
                model: 'product.template',
                method: 'write',
                args: [[productId], {
                    attribute_line_ids: [[0, 0, { attribute_id: attrId, value_ids: [[6, 0, valueIds]] }]],
                    website_published: true,
                }],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
