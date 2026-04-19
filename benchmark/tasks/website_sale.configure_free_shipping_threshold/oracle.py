"""Oracle for website_sale.configure_free_shipping_threshold.

Writes the two toggled fields (free_over=True, amount=100.00) on the seeded
delivery.carrier 'Bench Ship' via JSON-RPC. The oracle lands on the Delivery
Methods backend list first so it looks like a normal user session.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


CARRIER_NAME = "Bench Ship"


def oracle(page):
    login(page)
    navigate(page, "/odoo/delivery-methods")

    result = page.evaluate(
        """async (name) => {
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

            const hits = await callKw({
                model: 'delivery.carrier',
                method: 'search_read',
                args: [[['name', '=', name]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!hits.length) {
                throw new Error('Bench Ship carrier not found');
            }
            const carrierId = hits[0].id;

            await callKw({
                model: 'delivery.carrier',
                method: 'write',
                args: [[carrierId], {
                    free_over: true,
                    amount: 100.0,
                }],
                kwargs: {},
            });
            return 'ok:' + carrierId;
        }""",
        CARRIER_NAME,
    )
    if not result or not str(result).startswith("ok"):
        raise RuntimeError(result)


run_oracle(oracle)
