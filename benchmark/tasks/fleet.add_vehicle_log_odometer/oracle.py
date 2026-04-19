"""Oracle for fleet.add_vehicle_log_odometer.

Use authenticated JSON-RPC to:
  1. Find the seeded Tesla Motors/Model 3 fleet.vehicle.model.
  2. Create a new fleet.vehicle (plate FLEET-ADD-01, model Tesla/Model 3).
  3. Create a fleet.vehicle.odometer log for that vehicle with
     value=15000 and date=2026-04-15.
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

            // 1. Find the Tesla Motors brand.
            const brandRes = await callKw({
                model: 'fleet.vehicle.model.brand',
                method: 'search_read',
                args: [[['name', '=', 'Tesla Motors']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!brandRes.result?.length) return 'Tesla Motors brand not found';
            const brandId = brandRes.result[0].id;

            // 2. Find the Model 3 model under Tesla Motors.
            const modelRes = await callKw({
                model: 'fleet.vehicle.model',
                method: 'search_read',
                args: [[['name', '=', 'Model 3'], ['brand_id', '=', brandId]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!modelRes.result?.length) return 'Tesla Motors/Model 3 not found';
            const modelId = modelRes.result[0].id;

            // 3. Create the vehicle.
            const vehicleRes = await callKw({
                model: 'fleet.vehicle',
                method: 'create',
                args: [{
                    model_id: modelId,
                    license_plate: 'FLEET-ADD-01',
                }],
                kwargs: {},
            });
            if (!vehicleRes.result) return 'vehicle create failed: ' + JSON.stringify(vehicleRes);
            const vehicleId = Array.isArray(vehicleRes.result)
                ? vehicleRes.result[0]
                : vehicleRes.result;

            // 4. Create the odometer log.
            const odoRes = await callKw({
                model: 'fleet.vehicle.odometer',
                method: 'create',
                args: [{
                    vehicle_id: vehicleId,
                    value: 15000,
                    date: '2026-04-15',
                }],
                kwargs: {},
            });
            if (!odoRes.result) return 'odometer create failed: ' + JSON.stringify(odoRes);

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
