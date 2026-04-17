"""Oracle for hr_expense.create_mileage_expense_submit_report."""

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
                args: [[['name', '=', 'Administrator']], ['id']],
                kwargs: { limit: 1 },
            });
            const productRes = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['default_code', '=', 'MIL']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!employeeRes.result?.length || !productRes.result?.length) {
                return 'missing employee or product';
            }
            const expenseRes = await callKw({
                model: 'hr.expense',
                method: 'create',
                args: [[{
                    employee_id: employeeRes.result[0].id,
                    product_id: productRes.result[0].id,
                    name: 'Client Visit Mileage',
                    date: '2026-04-14',
                    total_amount_currency: 128.40,
                    payment_mode: 'own_account',
                }]],
                kwargs: {},
            });
            const expenseId = unwrapId(expenseRes.result);
            if (!expenseId) {
                return `unexpected expense result ${JSON.stringify(expenseRes.result)}`;
            }
            await callKw({
                model: 'hr.expense',
                method: 'action_submit',
                args: [[expenseId]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
