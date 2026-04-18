"""Oracle for mrp.plan_workorder_block_resume_finish_mo."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
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

            const moRes = await callKw({
                model: 'mrp.production',
                method: 'search_read',
                args: [[['name', '=', 'WH/MO/BENCH-WO-01']], ['id', 'workorder_ids']],
                kwargs: { limit: 1 },
            });
            if (!moRes.length) {
                throw new Error('missing manufacturing order');
            }
            const moId = moRes[0].id;
            await callKw({ model: 'mrp.production', method: 'button_plan', args: [[moId]], kwargs: {} });

            const woRes = await callKw({
                model: 'mrp.workorder',
                method: 'search_read',
                args: [[['production_id', '=', moId]], ['id', 'workcenter_id']],
                kwargs: { limit: 1 },
            });
            if (!woRes.length) {
                throw new Error('missing work order');
            }
            const wo = woRes[0];
            const workcenterId = wo.workcenter_id[0];

            await callKw({ model: 'mrp.workorder', method: 'button_start', args: [[wo.id]], kwargs: {} });
            await callKw({ model: 'mrp.workorder', method: 'button_pending', args: [[wo.id]], kwargs: {} });

            const lossRes = await callKw({
                model: 'mrp.workcenter.productivity.loss',
                method: 'search_read',
                args: [[['name', '=', 'Equipment Failure']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!lossRes.length) {
                throw new Error('missing block reason');
            }
            await callKw({
                model: 'mrp.workcenter.productivity',
                method: 'create',
                args: [[{
                    workcenter_id: workcenterId,
                    workorder_id: wo.id,
                    loss_id: lossRes[0].id,
                    user_id: 2,
                    date_start: new Date().toISOString().slice(0, 19).replace('T', ' '),
                }]],
                kwargs: {},
            });
            await callKw({ model: 'mrp.workorder', method: 'button_unblock', args: [[wo.id]], kwargs: {} });
            await callKw({ model: 'mrp.workorder', method: 'button_start', args: [[wo.id]], kwargs: {} });
            await callKw({ model: 'mrp.workorder', method: 'button_finish', args: [[wo.id]], kwargs: {} });
            await callKw({ model: 'mrp.production', method: 'button_mark_done', args: [[moId]], kwargs: {} });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
