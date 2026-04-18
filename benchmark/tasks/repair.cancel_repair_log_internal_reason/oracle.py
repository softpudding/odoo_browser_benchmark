"""Oracle for repair.cancel_repair_log_internal_reason.

Uses authenticated JSON-RPC: locate the seeded repair order, post an internal
note via message_post (subtype mail.mt_note), then call action_repair_cancel.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


NOTE_TEXT = "Customer requested cancellation - replacement parts no longer needed"


def oracle(page):
    login(page)
    navigate(page, "/odoo/repairs")

    response = page.evaluate(
        """async (noteText) => {
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const repairs = await callKw({
                model: 'repair.order',
                method: 'search_read',
                args: [[['name', '=', 'RO/CANCEL/0001']], ['id', 'state']],
                kwargs: { limit: 1 },
            });
            if (!repairs.length) throw new Error('Repair order missing');
            const repairId = repairs[0].id;

            const subtypeRes = await callKw({
                model: 'ir.model.data',
                method: 'search_read',
                args: [
                    [['module', '=', 'mail'], ['name', '=', 'mt_note']],
                    ['res_id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!subtypeRes.length) throw new Error('mail.mt_note subtype missing');
            const noteSubtype = subtypeRes[0].res_id;

            await callKw({
                model: 'repair.order',
                method: 'message_post',
                args: [[repairId]],
                kwargs: {
                    body: noteText,
                    subtype_id: noteSubtype,
                    message_type: 'comment',
                },
            });

            await callKw({
                model: 'repair.order',
                method: 'action_repair_cancel',
                args: [[repairId]],
                kwargs: {},
            });

            return 'ok';
        }""",
        NOTE_TEXT,
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
