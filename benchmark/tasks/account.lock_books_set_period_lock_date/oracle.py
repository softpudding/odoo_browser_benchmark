"""Oracle for account.lock_books_set_period_lock_date.

The Non-Advisors / Global Lock Date (`fiscalyear_lock_date` on `res.company`)
is exposed in Odoo's accounting Settings UI. This oracle proves the
end-state is reachable by setting the field directly via JSON-RPC from
inside an authenticated browser context. The browser-use agent must instead
operate the Settings page UI to reach the same end state.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/settings#accounting")
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

            // Resolve the main company id (first company by id is the main one
            // in the seeded benchmark database).
            const companies = await callKw({
                model: 'res.company',
                method: 'search_read',
                args: [[], ['id', 'name']],
                kwargs: { order: 'id asc', limit: 1 },
            });
            if (!companies || companies.length === 0) {
                throw new Error('no res.company record found');
            }
            const companyId = companies[0].id;

            await callKw({
                model: 'res.company',
                method: 'write',
                args: [[companyId], { fiscalyear_lock_date: '2026-03-31' }],
                kwargs: {},
            });

            // Read it back to confirm the value was actually persisted.
            const after = await callKw({
                model: 'res.company',
                method: 'read',
                args: [[companyId], ['fiscalyear_lock_date']],
                kwargs: {},
            });
            if (!after || !after[0] || after[0].fiscalyear_lock_date !== '2026-03-31') {
                throw new Error('fiscalyear_lock_date not persisted: ' + JSON.stringify(after));
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
