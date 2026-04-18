"""Oracle for hr_expense.split_expense_analytic_distribution.

Uses JSON-RPC ``call_kw`` from an authenticated browser context to set
``analytic_distribution`` on the draft expense (50% Bench Project
Alpha + 50% Bench Project Beta) and then call ``action_submit`` so
the expense transitions out of draft into the submitted state.

Doing it via RPC avoids the fragile Analytic Distribution popover UI,
which is the exact failure mode we expect from browser agents.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


EXPENSE_NAME = "Bench Split Travel"
ALPHA_NAME = "Bench Project Alpha"
BETA_NAME = "Bench Project Beta"


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)

    response = page.evaluate(
        """async ({ expenseName, alphaName, betaName }) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: payload,
                    }),
                });
                return res.json();
            };

            // Find the expense.
            const expenses = await callKw({
                model: 'hr.expense',
                method: 'search_read',
                args: [[['name', '=', expenseName]], ['id', 'state']],
                kwargs: { limit: 1 },
            });
            if (!expenses.result || !expenses.result.length) {
                return `Expense '${expenseName}' not found`;
            }
            const expense = expenses.result[0];

            // Find the two analytic accounts.
            const accounts = await callKw({
                model: 'account.analytic.account',
                method: 'search_read',
                args: [
                    [['name', 'in', [alphaName, betaName]]],
                    ['id', 'name'],
                ],
                kwargs: {},
            });
            if (!accounts.result) {
                return `search analytic accounts failed: ${JSON.stringify(accounts)}`;
            }
            const byName = {};
            for (const a of accounts.result) {
                byName[a.name] = a.id;
            }
            if (!byName[alphaName] || !byName[betaName]) {
                return `Missing analytic accounts: ${JSON.stringify(byName)}`;
            }

            // Write 50/50 analytic_distribution on the expense.
            const distribution = {};
            distribution[String(byName[alphaName])] = 50.0;
            distribution[String(byName[betaName])] = 50.0;
            const wrote = await callKw({
                model: 'hr.expense',
                method: 'write',
                args: [[expense.id], { analytic_distribution: distribution }],
                kwargs: {},
            });
            if (wrote.result !== true) {
                return `write failed: ${JSON.stringify(wrote)}`;
            }

            // Submit the expense (draft -> submitted).
            const submitted = await callKw({
                model: 'hr.expense',
                method: 'action_submit',
                args: [[expense.id]],
                kwargs: {},
            });
            if (submitted.error) {
                return `action_submit failed: ${JSON.stringify(submitted.error)}`;
            }

            // Re-read to confirm the expected end state.
            const verify = await callKw({
                model: 'hr.expense',
                method: 'read',
                args: [[expense.id], ['state', 'analytic_distribution']],
                kwargs: {},
            });
            if (!verify.result || !verify.result.length) {
                return `verify read failed: ${JSON.stringify(verify)}`;
            }
            const rec = verify.result[0];
            if (rec.state !== 'submitted') {
                return `expense state is ${rec.state}, expected submitted`;
            }
            const dist = rec.analytic_distribution || {};
            let total = 0;
            for (const v of Object.values(dist)) total += Number(v);
            if (Math.abs(total - 100.0) > 0.01) {
                return `distribution total ${total}, expected 100`;
            }
            return 'ok';
        }""",
        {
            "expenseName": EXPENSE_NAME,
            "alphaName": ALPHA_NAME,
            "betaName": BETA_NAME,
        },
    )
    if response != "ok":
        raise RuntimeError(
            f"Failed to split analytic distribution via RPC: {response}"
        )


run_oracle(oracle)
