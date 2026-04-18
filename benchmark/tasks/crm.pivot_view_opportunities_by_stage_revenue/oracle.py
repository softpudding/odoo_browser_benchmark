"""Oracle for crm.pivot_view_opportunities_by_stage_revenue.

Uses a JSON-RPC bypass to create an ir.filters favorite named
"Bench Stage Revenue Pivot" on model crm.lead, with a context that encodes
the pivot row grouping (stage_id) and the Expected Revenue measure. The
browser-use agent must still solve via the UI (Pivot view + Save current
search), but the oracle takes the deterministic path.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")

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

            // Look up the admin user id (the favorite is per-user).
            const adminHits = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!adminHits.length) {
                throw new Error('admin user not found');
            }
            const adminId = adminHits[0].id;

            // Remove any previous favorite with this exact name on crm.lead.
            const existing = await callKw({
                model: 'ir.filters',
                method: 'search',
                args: [[
                    ['name', '=', 'Bench Stage Revenue Pivot'],
                    ['model_id', '=', 'crm.lead'],
                ]],
                kwargs: {},
            });
            if (existing.length) {
                await callKw({
                    model: 'ir.filters',
                    method: 'unlink',
                    args: [existing],
                    kwargs: {},
                });
            }

            // Create the pivot favorite.
            const context = "{'pivot_row_groupby': ['stage_id'], 'pivot_measures': ['expected_revenue']}";
            const filterId = await callKw({
                model: 'ir.filters',
                method: 'create',
                args: [{
                    name: 'Bench Stage Revenue Pivot',
                    model_id: 'crm.lead',
                    user_ids: [[6, 0, [adminId]]],
                    domain: '[]',
                    context: context,
                    sort: '[]',
                }],
                kwargs: {},
            });
            return 'ok:' + filterId;
        }""",
    )
    if not response or not str(response).startswith("ok"):
        raise RuntimeError(response)


run_oracle(oracle)
