"""Oracle for account.reconcile_bank_statement_line_manual.

Reconciles the seeded bank statement line against the open customer
invoice by modifying the statement line's counterpart line to point at the
invoice's receivable account, re-posting, and calling reconcile() on the
two receivable-side move lines.

Pure JSON-RPC via /web/dataset/call_kw from an authenticated browser.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting")

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

            // Resolve partner
            const partners = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Bench Reconcile Customer']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!partners.length) throw new Error('Partner not found');
            const partnerId = partners[0].id;

            // Find invoice
            const invoices = await callKw({
                model: 'account.move',
                method: 'search_read',
                args: [[
                    ['partner_id', '=', partnerId],
                    ['move_type', '=', 'out_invoice'],
                    ['state', '=', 'posted'],
                ], ['id']],
                kwargs: { limit: 1 },
            });
            if (!invoices.length) throw new Error('Invoice not found');
            const invoiceId = invoices[0].id;

            // Invoice receivable line
            const invRecvLines = await callKw({
                model: 'account.move.line',
                method: 'search_read',
                args: [[
                    ['move_id', '=', invoiceId],
                    ['account_id.account_type', '=', 'asset_receivable'],
                ], ['id', 'account_id', 'debit', 'credit', 'reconciled']],
                kwargs: { limit: 1 },
            });
            if (!invRecvLines.length) throw new Error('Invoice receivable line not found');
            const invRecvLine = invRecvLines[0];
            const receivableAccountId = invRecvLine.account_id[0];

            // Find statement line
            const stls = await callKw({
                model: 'account.bank.statement.line',
                method: 'search_read',
                args: [[['payment_ref', '=', 'Bench Reconcile 500']], ['id', 'move_id']],
                kwargs: { limit: 1 },
            });
            if (!stls.length) throw new Error('Statement line not found');
            const stlId = stls[0].id;
            const stlMoveId = stls[0].move_id[0];

            // Statement line move lines: find the non-liquidity (credit) line
            const stlLines = await callKw({
                model: 'account.move.line',
                method: 'search_read',
                args: [[['move_id', '=', stlMoveId]], ['id', 'account_id', 'debit', 'credit']],
                kwargs: {},
            });
            const counterpartLine = stlLines.find(l => l.credit > 0);
            if (!counterpartLine) throw new Error('Counterpart line not found');

            // Draft the statement line move so we can edit it
            await callKw({
                model: 'account.move',
                method: 'button_draft',
                args: [[stlMoveId]],
                kwargs: {},
            });

            // Repoint the counterpart to the invoice's receivable account & partner
            await callKw({
                model: 'account.move.line',
                method: 'write',
                args: [[counterpartLine.id], {
                    account_id: receivableAccountId,
                    partner_id: partnerId,
                }],
                kwargs: {},
            });

            // Re-post the statement line move
            await callKw({
                model: 'account.move',
                method: 'action_post',
                args: [[stlMoveId]],
                kwargs: {},
            });

            // Reconcile the invoice receivable line with the statement counterpart line
            await callKw({
                model: 'account.move.line',
                method: 'reconcile',
                args: [[invRecvLine.id, counterpartLine.id]],
                kwargs: {},
            });

            // Verify
            const stlAfter = await callKw({
                model: 'account.bank.statement.line',
                method: 'read',
                args: [[stlId], ['is_reconciled', 'amount_residual']],
                kwargs: {},
            });
            const invAfter = await callKw({
                model: 'account.move',
                method: 'read',
                args: [[invoiceId], ['payment_state', 'amount_residual']],
                kwargs: {},
            });
            if (!stlAfter[0].is_reconciled) {
                throw new Error('STL not reconciled: ' + JSON.stringify(stlAfter));
            }
            if (invAfter[0].payment_state !== 'paid') {
                throw new Error('Invoice not paid: ' + JSON.stringify(invAfter));
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
