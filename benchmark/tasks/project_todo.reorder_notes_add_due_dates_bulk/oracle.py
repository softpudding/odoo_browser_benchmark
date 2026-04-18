"""Oracle for project_todo.reorder_notes_add_due_dates_bulk.

Navigates to the To-Do app and sets deadlines on the three seeded notes.

Approach: log in, visit /odoo/to-do so the session is in the right
context, then use the authenticated /web/dataset/call_kw endpoint to
write ``date_deadline`` on each of the three seeded notes. This mirrors
what the browser client does under the hood (web_save / write) and is
deterministic.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


ALPHA = "Benchmark Note Alpha"
BETA = "Benchmark Note Beta"
GAMMA = "Benchmark Note Gamma"

DEADLINES = {
    ALPHA: "2026-04-25",
    BETA: "2026-04-30",
    GAMMA: "2026-05-02",
}


def oracle(page):
    login(page)
    navigate(page, "/odoo/to-do")
    page.wait_for_timeout(1000)

    deadlines = {
        "alpha": DEADLINES[ALPHA],
        "beta": DEADLINES[BETA],
        "gamma": DEADLINES[GAMMA],
    }

    response = page.evaluate(
        """async (payload) => {
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

            const fields = ['id', 'name'];
            const targets = [
                ['Benchmark Note Alpha', payload.alpha],
                ['Benchmark Note Beta', payload.beta],
                ['Benchmark Note Gamma', payload.gamma],
            ];

            for (const [name, deadline] of targets) {
                const rows = await callKw({
                    model: 'project.task',
                    method: 'search_read',
                    args: [[['name', '=', name]], fields],
                    kwargs: { limit: 1 },
                });
                if (!rows.length) {
                    throw new Error('Missing seeded to-do: ' + name);
                }
                await callKw({
                    model: 'project.task',
                    method: 'write',
                    args: [[rows[0].id], { date_deadline: deadline }],
                    kwargs: {},
                });
            }
            return 'ok';
        }""",
        deadlines,
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
