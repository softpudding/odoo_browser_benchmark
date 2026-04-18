"""Oracle for point_of_sale.close_session_reconcile_cash_diff.

Uses JSON-RPC (allowed for oracle scripts only) to replicate the POS
closing-control flow without driving the kiosk UI. Posts a counted cash
amount of 97.00 on the seeded session whose expected cash is 100.00,
transitions the session into closing_control, and then closes it via
close_session_from_ui, leaving a cash_register_difference of -3.00.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/point-of-sale")

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

            const configRes = await callKw({
                model: 'pos.config',
                method: 'search_read',
                args: [[['name', '=', 'Bench Close POS']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!configRes.length) {
                throw new Error('POS config missing');
            }
            const sessionRes = await callKw({
                model: 'pos.session',
                method: 'search_read',
                args: [[['config_id', '=', configRes[0].id]], ['id', 'state']],
                kwargs: { limit: 1 },
            });
            if (!sessionRes.length) {
                throw new Error('POS session missing');
            }
            const sessionId = sessionRes[0].id;

            if (sessionRes[0].state === 'opening_control') {
                await callKw({
                    model: 'pos.session',
                    method: 'set_opening_control',
                    args: [[sessionId], 0, ''],
                    kwargs: {},
                });
            }

            // Step 1: record the counted cash (97.00) for the closing control.
            const postRes = await callKw({
                model: 'pos.session',
                method: 'post_closing_cash_details',
                args: [[sessionId]],
                kwargs: { counted_cash: 97.0 },
            });
            if (postRes && postRes.successful === false) {
                throw new Error(postRes.message || 'post_closing_cash_details failed');
            }

            // Step 2: transition the session into closing_control state.
            try {
                await callKw({
                    model: 'pos.session',
                    method: 'update_closing_control_state_session',
                    args: [[sessionId], ''],
                    kwargs: {},
                });
            } catch (err) {
                if (!/already closed/i.test(err.message || '')) {
                    throw err;
                }
            }

            // Step 3: close the session, accepting the -3.00 cash difference.
            const closeRes = await callKw({
                model: 'pos.session',
                method: 'close_session_from_ui',
                args: [[sessionId], []],
                kwargs: {},
            });
            if (closeRes && closeRes.successful === false) {
                throw new Error(closeRes.message || 'close_session_from_ui failed');
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
