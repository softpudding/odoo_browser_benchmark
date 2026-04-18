"""Oracle for hr_holidays.approve_multiple_requests_bulk.

Uses JSON-RPC via page.evaluate to deterministically call action_approve
on the three pending ('confirm') bench leaves — Alice, Bob, Carol —
while leaving Diana's draft request untouched.

Browser-use agents on this task typically either:
  - Approve Diana's Draft request too (violating the distractor rule),
  - Open each leave individually on the form (violating bulk requirement), or
  - Get lost clearing the default "Waiting For Me" / "This Year" search
    facets and never find all three rows.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


BENCH_CONFIRM_LEAVES = [
    "Bench Alice vacation",
    "Bench Bob vacation",
    "Bench Carol vacation",
]
DIANA_REFUSED_LEAVE = "Bench Diana vacation"


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)

    payload = {
        "confirm_names": BENCH_CONFIRM_LEAVES,
        "diana_name": DIANA_REFUSED_LEAVE,
    }

    response = page.evaluate(
        """async (payload) => {
            const callKw = async (model, method, args, kwargs) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { model, method, args, kwargs: kwargs || {} },
                    }),
                });
                const j = await res.json();
                if (j.error) {
                    throw new Error(JSON.stringify(j.error));
                }
                return j.result;
            };

            // Find the three confirm-state bench leaves.
            const leaves = await callKw(
                'hr.leave',
                'search_read',
                [[['name', 'in', payload.confirm_names],
                  ['state', '=', 'confirm']],
                 ['id', 'name', 'state']],
                {},
            );
            if (leaves.length !== payload.confirm_names.length) {
                throw new Error(
                    'Expected ' + payload.confirm_names.length +
                    ' confirm-state bench leaves, found ' + leaves.length
                );
            }

            const ids = leaves.map(l => l.id);

            // Bulk action_approve in a single call (like the list view's
            // MultiRecordViewButton does under the hood).
            await callKw('hr.leave', 'action_approve', [ids], {});

            // Verify Diana's leave is still 'refuse' (distractor).
            const diana = await callKw(
                'hr.leave',
                'search_read',
                [[['name', '=', payload.diana_name]],
                 ['id', 'state']],
                { limit: 1 },
            );
            if (!diana.length) {
                throw new Error('Diana leave missing');
            }
            if (diana[0].state !== 'refuse') {
                throw new Error(
                    'Diana leave state is ' + diana[0].state +
                    ', expected refuse'
                );
            }

            // Verify the three bench leaves are validate.
            const after = await callKw(
                'hr.leave',
                'search_read',
                [[['name', 'in', payload.confirm_names]],
                 ['id', 'name', 'state']],
                {},
            );
            for (const l of after) {
                if (l.state !== 'validate') {
                    throw new Error(
                        'Leave "' + l.name + '" state is ' + l.state +
                        ', expected validate'
                    );
                }
            }

            return 'ok';
        }""",
        payload,
    )

    if response != "ok":
        raise RuntimeError(f"Unexpected oracle response: {response!r}")


run_oracle(oracle)
