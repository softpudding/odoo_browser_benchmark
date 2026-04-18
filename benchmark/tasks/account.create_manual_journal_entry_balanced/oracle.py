"""Oracle for account.create_manual_journal_entry_balanced.

Uses JSON-RPC (allowed for oracle scripts) from an authenticated browser
context to create a balanced three-line manual journal entry in the
Miscellaneous Operations journal and post it. This bypasses the tricky
move_type='entry' form UI that browser agents must operate manually.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting")

    response = page.evaluate(
        """async () => {
            const unwrapId = (v) => Array.isArray(v) ? v[0] : v;
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

            const journalRes = await callKw({
                model: 'account.journal',
                method: 'search_read',
                args: [
                    [['type', '=', 'general'], ['name', '=', 'Miscellaneous Operations']],
                    ['id'],
                ],
                kwargs: { limit: 1 },
            });
            if (!journalRes.length) {
                throw new Error('Miscellaneous Operations journal missing');
            }
            const journalId = journalRes[0].id;

            const recvAccRes = await callKw({
                model: 'account.account',
                method: 'search_read',
                args: [[['name', '=', 'Bench Receivable']], ['id']],
                kwargs: { limit: 1 },
            });
            const salesAccRes = await callKw({
                model: 'account.account',
                method: 'search_read',
                args: [[['name', '=', 'Bench Sales Revenue']], ['id']],
                kwargs: { limit: 1 },
            });
            const otherAccRes = await callKw({
                model: 'account.account',
                method: 'search_read',
                args: [[['name', '=', 'Bench Other Revenue']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!recvAccRes.length || !salesAccRes.length || !otherAccRes.length) {
                throw new Error('Seeded accounts missing');
            }

            const partnerRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Bench Entity']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!partnerRes.length) {
                throw new Error('Bench Entity partner missing');
            }

            const moveId = unwrapId(await callKw({
                model: 'account.move',
                method: 'create',
                args: [[{
                    move_type: 'entry',
                    journal_id: journalId,
                    ref: 'Bench Manual Adj 2026-04',
                    date: '2026-04-30',
                    line_ids: [
                        [0, 0, {
                            account_id: recvAccRes[0].id,
                            partner_id: partnerRes[0].id,
                            name: 'Manual adjustment receivable',
                            debit: 100.0,
                            credit: 0.0,
                        }],
                        [0, 0, {
                            account_id: salesAccRes[0].id,
                            name: 'Manual adjustment \u2014 sales',
                            debit: 0.0,
                            credit: 60.0,
                        }],
                        [0, 0, {
                            account_id: otherAccRes[0].id,
                            name: 'Manual adjustment \u2014 other income',
                            debit: 0.0,
                            credit: 40.0,
                        }],
                    ],
                }]],
                kwargs: {},
            }));

            await callKw({
                model: 'account.move',
                method: 'action_post',
                args: [[moveId]],
                kwargs: {},
            });

            const after = await callKw({
                model: 'account.move',
                method: 'read',
                args: [[moveId], ['state', 'move_type', 'ref']],
                kwargs: {},
            });
            if (!after || !after[0] || after[0].state !== 'posted') {
                throw new Error('move not posted: ' + JSON.stringify(after));
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
