"""Oracle for mrp.create_variant_specific_bom.

Uses JSON-RPC `call_kw` against the Odoo backend from an authenticated
browser context. Resolves the Bench T-Shirt template, the Red variant
product.product, and the Bench Fabric component, then creates a
mrp.bom with product_tmpl_id=template and product_id=red variant,
plus a single bom_line for Bench Fabric qty=1.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


TEMPLATE_NAME = "Bench T-Shirt"
RED_VALUE = "Red"
COMPONENT_NAME = "Bench Fabric"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")

    result = page.evaluate(
        """async ({templateName, redValue, componentName}) => {
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

            // 1. Resolve the product template.
            const tmplRecs = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', templateName]], ['id', 'product_variant_ids']],
                kwargs: { limit: 1 },
            });
            if (!tmplRecs.length) throw new Error('Template ' + templateName + ' not found');
            const tmplId = tmplRecs[0].id;

            // 2. Resolve the Red variant (product.product).
            const variantRecs = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[
                    ['product_tmpl_id', '=', tmplId],
                    ['product_template_variant_value_ids.name', '=', redValue],
                ], ['id', 'display_name']],
                kwargs: { limit: 1 },
            });
            if (!variantRecs.length) {
                throw new Error('Red variant for ' + templateName + ' not found');
            }
            const redVariantId = variantRecs[0].id;

            // 3. Resolve the component product.product.
            const compRecs = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', componentName]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!compRecs.length) {
                throw new Error('Component ' + componentName + ' not found');
            }
            const compId = compRecs[0].id;

            // 4. Create the variant-specific BoM with one component line.
            const bomId = await callKw({
                model: 'mrp.bom',
                method: 'create',
                args: [{
                    product_tmpl_id: tmplId,
                    product_id: redVariantId,
                    product_qty: 1.0,
                    type: 'normal',
                    bom_line_ids: [[0, 0, {
                        product_id: compId,
                        product_qty: 1.0,
                    }]],
                }],
                kwargs: {},
            });

            // 5. Read back for verification.
            const [bom] = await callKw({
                model: 'mrp.bom',
                method: 'read',
                args: [[bomId], ['product_tmpl_id', 'product_id', 'product_qty', 'type', 'bom_line_ids']],
                kwargs: {},
            });
            return { bom };
        }""",
        {
            "templateName": TEMPLATE_NAME,
            "redValue": RED_VALUE,
            "componentName": COMPONENT_NAME,
        },
    )

    if not result:
        raise RuntimeError("Oracle: no result returned")
    bom = result.get("bom") or {}
    if not bom.get("product_id"):
        raise RuntimeError(
            f"Oracle: BoM product_id is {bom.get('product_id')!r}, expected the Red variant"
        )
    if abs(float(bom.get("product_qty") or 0.0) - 1.0) > 1e-6:
        raise RuntimeError(
            f"Oracle: BoM product_qty is {bom.get('product_qty')}, expected 1.0"
        )
    if bom.get("type") != "normal":
        raise RuntimeError(
            f"Oracle: BoM type is {bom.get('type')!r}, expected 'normal'"
        )
    if len(bom.get("bom_line_ids") or []) != 1:
        raise RuntimeError(
            f"Oracle: BoM has {len(bom.get('bom_line_ids') or [])} lines, expected 1"
        )


run_oracle(oracle)
