"""Oracle for crm.update_lead_phone."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    response = page.evaluate(
        """async (phoneValue) => {
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

            const leads = await callKw({
                model: 'crm.lead',
                method: 'search_read',
                args: [
                    [['name', '=', 'Summit Energy Expansion'], ['type', '=', 'lead']],
                    ['id'],
                ],
                kwargs: { limit: 1 },
            });

            if (!leads.result || !leads.result.length) {
                return 'CRM lead not found';
            }

            const leadId = leads.result[0].id;
            const ok = await callKw({
                model: 'crm.lead',
                method: 'write',
                args: [[leadId], { phone: phoneValue }],
                kwargs: {},
            });
            return ok.result === true ? 'ok' : `crm write failed: ${JSON.stringify(ok)}`;
        }""",
        "+1 555 0222",
    )
    if response != "ok":
        raise RuntimeError(f"Failed to update lead phone via RPC: {response}")
    _wait_no_loading(page)


run_oracle(oracle)
