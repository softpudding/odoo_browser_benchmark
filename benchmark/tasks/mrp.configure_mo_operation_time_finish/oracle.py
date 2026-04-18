"""Oracle for mrp.configure_mo_operation_time_finish.

Uses JSON-RPC `call_kw` against the Odoo backend from an authenticated
browser context. Finds the work order for WH/MO/BENCH0001, sets
`duration_expected` to 45 minutes, starts the work order, and then
finishes it so that its state becomes 'done'.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


MO_NAME = "WH/MO/BENCH0001"
OPERATION_NAME = "Assembly Station"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")

    result = page.evaluate(
        """async ({moName, operationName}) => {
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

            // 1. Find the MO by name.
            const moIds = await callKw({
                model: 'mrp.production',
                method: 'search',
                args: [[['name', '=', moName]]],
                kwargs: { limit: 1 },
            });
            if (!moIds.length) throw new Error('MO ' + moName + ' not found');

            // 2. Find the work order for that MO.
            const woIds = await callKw({
                model: 'mrp.workorder',
                method: 'search',
                args: [[['production_id', '=', moIds[0]], ['name', '=', operationName]]],
                kwargs: { limit: 1 },
            });
            if (!woIds.length) throw new Error('Work order ' + operationName + ' not found on ' + moName);
            const woId = woIds[0];

            // 3. Set expected duration to 45 minutes.
            await callKw({
                model: 'mrp.workorder',
                method: 'write',
                args: [[woId], { duration_expected: 45 }],
                kwargs: {},
            });

            // 4. Start the work order (moves state -> progress).
            await callKw({
                model: 'mrp.workorder',
                method: 'button_start',
                args: [[woId]],
                kwargs: {},
            });

            // 5. Finish the work order (moves state -> done).
            await callKw({
                model: 'mrp.workorder',
                method: 'button_finish',
                args: [[woId]],
                kwargs: {},
            });

            // 6. Read back state + duration for verification.
            const [wo] = await callKw({
                model: 'mrp.workorder',
                method: 'read',
                args: [[woId], ['state', 'duration_expected']],
                kwargs: {},
            });
            return wo;
        }""",
        {"moName": MO_NAME, "operationName": OPERATION_NAME},
    )

    if not result:
        raise RuntimeError("Oracle: no work order state returned")
    if result.get("state") != "done":
        raise RuntimeError(
            f"Oracle: work order state is {result.get('state')!r}, expected 'done'"
        )
    if abs(float(result.get("duration_expected") or 0) - 45.0) > 0.5:
        raise RuntimeError(
            f"Oracle: duration_expected is {result.get('duration_expected')}, expected 45"
        )


run_oracle(oracle)
