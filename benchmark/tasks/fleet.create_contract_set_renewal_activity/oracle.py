"""Oracle for fleet.create_contract_set_renewal_activity."""

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
            const adminRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['id']],
                kwargs: { limit: 1 },
            });
            const activityTypeRes = await callKw({
                model: 'mail.activity.type',
                method: 'search_read',
                args: [[['name', '=', 'Contract to Renew'], ['res_model', '=', 'fleet.vehicle.log.contract']], ['id']],
                kwargs: { limit: 1 },
            });
            const modelIdRes = await callKw({
                model: 'ir.model',
                method: 'search_read',
                args: [[['model', '=', 'fleet.vehicle.log.contract']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!adminRes.result?.length || !activityTypeRes.result?.length || !modelIdRes.result?.length) {
                return 'missing admin or activity metadata';
            }
            const vehicleRes = await callKw({
                model: 'fleet.vehicle',
                method: 'create',
                args: [[{
                    model_id: modelRes.result[0].id,
                    license_plate: 'FLE-6124',
                    driver_id: driverRes.result[0].id,
                    acquisition_date: '2026-04-18',
                }]],
                kwargs: {},
            });
            const vehicleId = Array.isArray(vehicleRes.result) ? vehicleRes.result[0] : vehicleRes.result;
            const contractRes = await callKw({
                model: 'fleet.vehicle.log.contract',
                method: 'create',
                args: [[{
                    ins_ref: 'RENEW-6124',
                    vehicle_id: vehicleId,
                    insurer_id: vendorRes.result[0].id,
                    user_id: adminRes.result[0].id,
                    start_date: '2026-04-20',
                    expiration_date: '2026-11-20',
                }]],
                kwargs: {},
            });
            const contractId = Array.isArray(contractRes.result) ? contractRes.result[0] : contractRes.result;
            await callKw({
                model: 'mail.activity',
                method: 'create',
                args: [[{
                    res_model_id: modelIdRes.result[0].id,
                    res_id: contractId,
                    activity_type_id: activityTypeRes.result[0].id,
                    user_id: adminRes.result[0].id,
                    date_deadline: '2026-11-20',
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
