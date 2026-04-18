"""Oracle for hr_expense.create_with_currency_eur_to_usd.

Uses JSON-RPC to create the expense deterministically. The browser-use agent
must still solve via the UI; the oracle just proves the task is reachable
through the browser session (logged-in cookies + same RPC endpoint).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    response = page.evaluate(
        """async () => {
            const unwrapId = (value) => {
                if (Array.isArray(value) && value.length === 1 && Number.isInteger(value[0])) {
                    return value[0];
                }
                if (Array.isArray(value) && value.length === 1 && Array.isArray(value[0])) {
                    return value[0][0];
                }
                if (Number.isInteger(value)) {
                    return value;
                }
                return null;
            };
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };

            const employeeRes = await callKw({
                model: 'hr.employee',
                method: 'search_read',
                args: [[['user_id.login', '=', 'admin']], ['id']],
                kwargs: { limit: 1 },
            });
            const productRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Hotel'], ['can_be_expensed', '=', true]], ['id']],
                kwargs: { limit: 1 },
            });
            const eurRes = await callKw({
                model: 'res.currency',
                method: 'search_read',
                args: [[['name', '=', 'EUR']], ['id']],
                kwargs: { limit: 1, context: { active_test: false } },
            });
            if (!employeeRes.result?.length) {
                return 'missing employee';
            }
            if (!productRes.result?.length) {
                return 'missing Hotel product';
            }
            if (!eurRes.result?.length) {
                return 'missing EUR currency';
            }
            const expenseRes = await callKw({
                model: 'hr.expense',
                method: 'create',
                args: [[{
                    name: 'NYC Hotel',
                    employee_id: employeeRes.result[0].id,
                    product_id: productRes.result[0].id,
                    currency_id: eurRes.result[0].id,
                    total_amount_currency: 185.00,
                    date: '2026-04-01',
                    payment_mode: 'own_account',
                }]],
                kwargs: {},
            });
            const expenseId = unwrapId(expenseRes.result);
            if (!expenseId) {
                return `unexpected expense result ${JSON.stringify(expenseRes.result)}`;
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
