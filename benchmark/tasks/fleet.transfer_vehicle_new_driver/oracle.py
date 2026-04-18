"""Oracle for fleet.transfer_vehicle_new_driver.

Use authenticated JSON-RPC to:
  1. Find the seeded vehicle by license_plate = 'BENCH-01'.
  2. Find the 'New Driver Alice' partner.
  3. Write driver_id = Alice on the vehicle (fleet.vehicle.write hook
     auto-closes Bob's assignation log with date_end = today and creates
     a new assignation log for Alice with date_start = today).
  4. Update Alice's assignation log's date_start to 2026-03-15.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
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

            const vehicleRes = await callKw({
                model: 'fleet.vehicle',
                method: 'search_read',
                args: [[['license_plate', '=', 'BENCH-01']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!vehicleRes.result?.length) return 'vehicle not found';
            const vehicleId = vehicleRes.result[0].id;

            const aliceRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['email', '=', 'new.alice@bench.test']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!aliceRes.result?.length) return 'New Driver Alice not found';
            const aliceId = aliceRes.result[0].id;

            // 1. Find Bob's open assignation log so we can manually close
            //    it after switching drivers (the auto-close hook is unreliable).
            const bobRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['email', '=', 'old.bob@bench.test']], ['id']],
                kwargs: { limit: 1 },
            });
            const bobId = bobRes.result?.[0]?.id;
            const bobLogIds = bobId ? (await callKw({
                model: 'fleet.vehicle.assignation.log',
                method: 'search',
                args: [[
                    ['vehicle_id', '=', vehicleId],
                    ['driver_id', '=', bobId],
                    ['date_end', '=', false],
                ]],
                kwargs: {},
            })).result || [] : [];

            // 2. Switch the vehicle's driver to New Driver Alice.
            await callKw({
                model: 'fleet.vehicle',
                method: 'write',
                args: [[vehicleId], { driver_id: aliceId }],
                kwargs: {},
            });

            // 3. Defensively close Bob's previously-open assignation log.
            if (bobLogIds.length) {
                const today = new Date().toISOString().slice(0, 10);
                await callKw({
                    model: 'fleet.vehicle.assignation.log',
                    method: 'write',
                    args: [bobLogIds, { date_end: today }],
                    kwargs: {},
                });
            }

            // 2. Find Alice's freshly-created assignation log entry and update
            //    its date_start to 2026-03-15.
            const aliceLogRes = await callKw({
                model: 'fleet.vehicle.assignation.log',
                method: 'search_read',
                args: [
                    [
                        ['vehicle_id', '=', vehicleId],
                        ['driver_id', '=', aliceId],
                    ],
                    ['id'],
                ],
                kwargs: { order: 'create_date desc', limit: 1 },
            });
            if (!aliceLogRes.result?.length) {
                return 'New Driver Alice assignation log was not auto-created';
            }
            await callKw({
                model: 'fleet.vehicle.assignation.log',
                method: 'write',
                args: [[aliceLogRes.result[0].id], { date_start: '2026-03-15' }],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
