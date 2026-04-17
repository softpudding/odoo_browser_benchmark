"""Oracle for purchase.update_rfq_note."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    response = page.evaluate(
        """async (noteValue) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: payload,
                    }),
                });
                return res.json();
            };

            const rfqs = await callKw({
                model: 'purchase.order',
                method: 'search_read',
                args: [[['origin', '=', 'BENCH-NOTE-01']], ['id']],
                kwargs: { limit: 1 },
            });

            if (!rfqs.result || !rfqs.result.length) {
                return 'RFQ not found';
            }

            const rfqId = rfqs.result[0].id;
            const ok = await callKw({
                model: 'purchase.order',
                method: 'write',
                args: [[rfqId], { note: noteValue }],
                kwargs: {},
            });
            return ok.result === true ? 'ok' : `purchase write failed: ${JSON.stringify(ok)}`;
        }""",
        "Verified supplier confirmation. Keep shipping date tight.",
    )
    if response != "ok":
        raise RuntimeError(f"Failed to update RFQ note via RPC: {response}")


run_oracle(oracle)
