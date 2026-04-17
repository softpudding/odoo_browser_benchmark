"""Oracle for fleet.create_vehicle_assign_driver_contract."""

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
            const modelRes = await callKw({
                model: 'fleet.vehicle.model',
                method: 'search_read',
                args: [[['name', '=', 'Cargo EV']], ['id']],
                kwargs: { limit: 1 },
            });
            const driverRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Avery Collins']], ['id']],
                kwargs: { limit: 1 },
            });
            const vendorRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Northwind Leasing']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!modelRes.result?.length || !driverRes.result?.length || !vendorRes.result?.length) {
                return 'missing setup data';
            }
            const vehicleRes = await callKw({
                model: 'fleet.vehicle',
                method: 'create',
                args: [[{
                    model_id: modelRes.result[0].id,
                    license_plate: 'FSM-2048',
                    driver_id: driverRes.result[0].id,
                    acquisition_date: '2026-04-12',
                }]],
                kwargs: {},
            });
            const vehicleId = Array.isArray(vehicleRes.result) ? vehicleRes.result[0] : vehicleRes.result;
            await callKw({
                model: 'fleet.vehicle.log.contract',
                method: 'create',
                args: [[{
                    ins_ref: 'LEASE-2048',
                    vehicle_id: vehicleId,
                    insurer_id: vendorRes.result[0].id,
                    start_date: '2026-04-15',
                    expiration_date: '2026-10-15',
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
