"""Oracle for website_sale.configure_delivery_method_weight.

Strategy:
  1. Log in as admin and navigate to the Delivery Methods backend list
     (/odoo/delivery-methods) so the oracle lands on the same page a
     human agent would use.
  2. Look up the seeded 'Bench Delivery Product' so we can use it as the
     new carrier's Delivery Product.
  3. Create the delivery.carrier via JSON-RPC with delivery_type='base_on_rule',
     is_published=True, website_published=True, and two delivery.price.rule
     children (<=5 kg -> 10, >5 kg -> 20).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


CARRIER_NAME = "Bench Weight Shipping"
DELIVERY_PRODUCT_NAME = "Bench Delivery Product"


def oracle(page):
    login(page)

    # Land on the Delivery Methods list so the oracle "looks" like a user.
    navigate(page, "/odoo/delivery-methods")

    carrier_id = page.evaluate(
        """async (payload) => {
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

            // Resolve the seeded delivery product (template -> default variant).
            const tmplHits = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', payload.productName]], ['product_variant_id']],
                kwargs: { limit: 1 },
            });
            if (!tmplHits.length) {
                throw new Error('Seeded product not found: ' + payload.productName);
            }
            const variantRef = tmplHits[0].product_variant_id;
            const variantId = Array.isArray(variantRef) ? variantRef[0] : variantRef;
            if (!variantId) {
                throw new Error('Seeded product has no variant');
            }

            const ids = await callKw({
                model: 'delivery.carrier',
                method: 'create',
                args: [[{
                    name: payload.carrierName,
                    delivery_type: 'base_on_rule',
                    product_id: variantId,
                    is_published: true,
                    website_published: true,
                    active: true,
                    price_rule_ids: [
                        [0, 0, {
                            sequence: 10,
                            variable: 'weight',
                            operator: '<=',
                            max_value: 5.0,
                            list_base_price: 10.0,
                            list_price: 0.0,
                            variable_factor: 'weight',
                        }],
                        [0, 0, {
                            sequence: 20,
                            variable: 'weight',
                            operator: '>',
                            max_value: 5.0,
                            list_base_price: 20.0,
                            list_price: 0.0,
                            variable_factor: 'weight',
                        }],
                    ],
                }]],
                kwargs: {},
            });
            return Array.isArray(ids) ? ids[0] : ids;
        }""",
        {
            "carrierName": CARRIER_NAME,
            "productName": DELIVERY_PRODUCT_NAME,
        },
    )
    if not carrier_id:
        raise RuntimeError("Could not create delivery.carrier")

    # Sanity read the carrier back so we fail loudly if publish didn't stick.
    data = page.evaluate(
        """async (cid) => {
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
            const [carrier] = await callKw({
                model: 'delivery.carrier',
                method: 'read',
                args: [[cid], ['name', 'delivery_type', 'is_published', 'price_rule_ids']],
                kwargs: {},
            });
            return carrier;
        }""",
        carrier_id,
    )
    if data.get("delivery_type") != "base_on_rule":
        raise RuntimeError(f"delivery_type is {data.get('delivery_type')}, expected base_on_rule")
    if not data.get("is_published"):
        raise RuntimeError("Carrier is not published after create")
    if len(data.get("price_rule_ids") or []) != 2:
        raise RuntimeError(
            f"Expected 2 price rules, got {len(data.get('price_rule_ids') or [])}"
        )


run_oracle(oracle)
