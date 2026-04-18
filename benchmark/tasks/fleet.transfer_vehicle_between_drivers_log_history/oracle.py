"""Oracle for fleet.transfer_vehicle_between_drivers_log_history."""

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
                args: [[['license_plate', '=', 'BS-1001']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!vehicleRes.result?.length) return 'vehicle not found';
            const vehicleId = vehicleRes.result[0].id;

            const bobRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Driver Bob'], ['is_company', '=', false]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!bobRes.result?.length) return 'Driver Bob not found';
            const bobId = bobRes.result[0].id;

            // 1. Switch the vehicle's driver to Driver Bob.
            //    The fleet.vehicle.write hook auto-creates an assignation log
            //    for Bob with date_start = today.
            await callKw({
                model: 'fleet.vehicle',
                method: 'write',
                args: [[vehicleId], { driver_id: bobId }],
                kwargs: {},
            });

            // 2. Find Bob's freshly-created assignation log entry and update
            //    its date_start to 2026-04-18.
            const bobLogRes = await callKw({
                model: 'fleet.vehicle.assignation.log',
                method: 'search_read',
                args: [
                    [
                        ['vehicle_id', '=', vehicleId],
                        ['driver_id', '=', bobId],
                    ],
                    ['id'],
                ],
                kwargs: { order: 'create_date desc', limit: 1 },
            });
            if (!bobLogRes.result?.length) {
                return 'Driver Bob assignation log was not auto-created';
            }
            await callKw({
                model: 'fleet.vehicle.assignation.log',
                method: 'write',
                args: [[bobLogRes.result[0].id], { date_start: '2026-04-18' }],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
