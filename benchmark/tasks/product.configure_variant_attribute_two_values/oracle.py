"""Oracle for product.configure_variant_attribute_two_values.

Adds a Size attribute (creating it + three values inline) and attaches
it to Bench Variant Shirt via a single product.template.attribute.line
create. A write on attribute_line_ids triggers _create_variants which
auto-generates three product.product rows.

Implemented as in-browser JSON-RPC calls (same pattern as
website_sale.configure_variant_publish_product) so the oracle is
deterministic and doesn't depend on brittle Attributes-tab UI selectors.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory/products")
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
                args: [[['name', '=', 'Bench Variant Shirt']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!productRes.result?.length) {
                return 'missing product Bench Variant Shirt';
            }
            const productId = productRes.result[0].id;

            let attrId;
            const attrRes = await callKw({
                model: 'product.attribute',
                method: 'search_read',
                args: [[['name', '=', 'Size']], ['id']],
                kwargs: { limit: 1 },
            });
            if (attrRes.result?.length) {
                attrId = attrRes.result[0].id;
            } else {
                const createAttr = await callKw({
                    model: 'product.attribute',
                    method: 'create',
                    args: [{ name: 'Size', create_variant: 'always' }],
                    kwargs: {},
                });
                attrId = createAttr.result;
            }

            const valueIds = [];
            for (const valueName of ['Small', 'Medium', 'Large']) {
                const valRes = await callKw({
                    model: 'product.attribute.value',
                    method: 'search_read',
                    args: [[
                        ['attribute_id', '=', attrId],
                        ['name', '=', valueName],
                    ], ['id']],
                    kwargs: { limit: 1 },
                });
                if (valRes.result?.length) {
                    valueIds.push(valRes.result[0].id);
                } else {
                    const createVal = await callKw({
                        model: 'product.attribute.value',
                        method: 'create',
                        args: [{ name: valueName, attribute_id: attrId }],
                        kwargs: {},
                    });
                    valueIds.push(createVal.result);
                }
            }

            const writeRes = await callKw({
                model: 'product.template',
                method: 'write',
                args: [[productId], {
                    attribute_line_ids: [[0, 0, {
                        attribute_id: attrId,
                        value_ids: [[6, 0, valueIds]],
                    }]],
                }],
                kwargs: {},
            });
            if (writeRes.error) {
                return 'write failed: ' + JSON.stringify(writeRes.error);
            }

            const variantsRes = await callKw({
                model: 'product.product',
                method: 'search_count',
                args: [[['product_tmpl_id', '=', productId]]],
                kwargs: {},
            });
            return 'variants=' + variantsRes.result;
        }""",
    )
    if not isinstance(response, str) or not response.startswith("variants="):
        raise RuntimeError(f"oracle rpc error: {response!r}")
    count = int(response.split("=", 1)[1])
    if count != 3:
        raise RuntimeError(
            f"expected 3 variants after write, got {count}"
        )


run_oracle(oracle)
