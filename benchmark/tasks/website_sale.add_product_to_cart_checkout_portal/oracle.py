"""Oracle for website_sale.add_product_to_cart_checkout_portal.

Strategy:
  The "truly public" cart-then-checkout flow via JSON-RPC is brittle because
  it requires session cookies for the website.sale.controller and a valid
  payment transaction redirect. Instead, the oracle builds the final state
  the browser agent would have produced had they completed checkout:

  1. Log in as admin and navigate to /odoo/sales to land somewhere realistic.
  2. Via JSON-RPC:
       a. Resolve the seeded 'Bench Portal Product' variant + default website.
       b. Create the res.partner 'Bench Portal Customer' with the exact
          delivery address described in the prompt.
       c. Create a sale.order on the website with website_id set, one order
          line for the product (qty 1, price 25.00, no taxes), then call
          action_confirm so the state transitions out of 'draft'.
  3. Sanity: read the order back and assert amount_total == 25.00 and the
     state is one of ('sale', 'sent', 'done').
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
)


PRODUCT_NAME = "Bench Portal Product"
CUSTOMER_NAME = "Bench Portal Customer"


def oracle(page):
    login(page)

    # Land on the backend Sales app — a realistic place for the oracle to
    # "look" like an admin operator finalising a webshop order.
    navigate(page, "/odoo/sales")

    result = page.evaluate(
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

            // 1. Resolve seeded product variant.
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

            // 2. Resolve website + country.
            const websites = await callKw({
                model: 'website',
                method: 'search_read',
                args: [[], ['id', 'company_id']],
                kwargs: { limit: 1 },
            });
            if (!websites.length) {
                throw new Error('No website record found');
            }
            const websiteId = websites[0].id;
            const companyRef = websites[0].company_id;
            const companyId = Array.isArray(companyRef) ? companyRef[0] : companyRef;

            const countries = await callKw({
                model: 'res.country',
                method: 'search_read',
                args: [[['code', '=', 'US']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!countries.length) {
                throw new Error('Country US not found');
            }
            const countryId = countries[0].id;

            // 3. Create the checkout customer with delivery address fields.
            const partnerIds = await callKw({
                model: 'res.partner',
                method: 'create',
                args: [[{
                    name: payload.customerName,
                    company_type: 'person',
                    customer_rank: 1,
                    street: '12 Bench Street',
                    city: 'Benchtown',
                    zip: '90001',
                    country_id: countryId,
                    email: 'bench.portal@example.com',
                    phone: '+1 555-0199',
                }]],
                kwargs: {},
            });
            const partnerId = Array.isArray(partnerIds) ? partnerIds[0] : partnerIds;

            // 4. Create the sale.order marked as a website order.
            const orderIds = await callKw({
                model: 'sale.order',
                method: 'create',
                args: [[{
                    partner_id: partnerId,
                    website_id: websiteId,
                    company_id: companyId,
                    order_line: [[0, 0, {
                        product_id: variantId,
                        product_uom_qty: 1.0,
                        price_unit: 25.0,
                        tax_ids: [[5, 0, 0]],
                    }]],
                }]],
                kwargs: {},
            });
            const orderId = Array.isArray(orderIds) ? orderIds[0] : orderIds;

            // 5. Confirm so the order leaves the draft quotation state.
            await callKw({
                model: 'sale.order',
                method: 'action_confirm',
                args: [[orderId]],
                kwargs: {},
            });

            // 6. Read back for sanity.
            const orderData = await callKw({
                model: 'sale.order',
                method: 'read',
                args: [[orderId], ['state', 'amount_total', 'website_id', 'partner_id']],
                kwargs: {},
            });
            return { order: orderData[0] };
        }""",
        {
            "productName": PRODUCT_NAME,
            "customerName": CUSTOMER_NAME,
        },
    )

    order = result["order"]
    if order["state"] not in ("sale", "sent", "done"):
        raise RuntimeError(
            f"Oracle: order state is {order['state']}, expected sale/sent/done"
        )
    if abs(order["amount_total"] - 25.0) > 0.05:
        raise RuntimeError(
            f"Oracle: amount_total is {order['amount_total']}, expected 25.0"
        )
    if not order.get("website_id"):
        raise RuntimeError("Oracle: order has no website_id set")


run_oracle(oracle)
