"""Oracle for hr_expense.submit_report_with_receipt_approve."""

import base64
from pathlib import Path

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")

    receipt_b64 = base64.b64encode(
        Path("/tmp/hr_expense_submit_report_with_receipt_approve.svg").read_bytes()
    ).decode()
    response = page.evaluate(
        """async ({receiptB64}) => {
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
                args: [[['name', '=', '[HOTEL] Hotel Stay']], ['id']],
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
                    name: 'Harbor Summit Hotel',
                    date: '2026-04-08',
                    total_amount_currency: 486.75,
                    payment_mode: 'own_account',
                }]],
                kwargs: {},
            });
            const expenseId = unwrapId(expenseRes.result);
            if (!expenseId) {
                return `unexpected expense result ${JSON.stringify(expenseRes.result)}`;
            }
            const attachmentRes = await callKw({
                model: 'ir.attachment',
                method: 'create',
                args: [[{
                    name: 'hr_expense_submit_report_with_receipt_approve.svg',
                    res_model: 'hr.expense',
                    res_id: expenseId,
                    type: 'binary',
                    mimetype: 'image/svg+xml',
                    datas: receiptB64,
                }]],
                kwargs: {},
            });
            const attachmentId = unwrapId(attachmentRes.result);
            if (!attachmentId) {
                return `unexpected attachment result ${JSON.stringify(attachmentRes.result)}`;
            }
            await callKw({
                model: 'hr.expense',
                method: 'write',
                args: [[expenseId], { attachment_ids: [[4, attachmentId]] }],
                kwargs: {},
            });
            await callKw({
                model: 'hr.expense',
                method: 'action_submit',
                args: [[expenseId]],
                kwargs: {},
            });
            await callKw({
                model: 'hr.expense',
                method: 'action_approve',
                args: [[expenseId]],
                kwargs: {},
            });
            return 'ok';
        }""",
        {"receiptB64": receipt_b64},
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
