"""Oracle for project_todo.bulk_move_tasks_between_projects.

Reassigns Alpha, Bravo, Charlie from Bench Proj A to Bench Proj B and leaves
Delta alone. The supported Community path is task-by-task form edit of
`project_id`. For oracle determinism we still open the project app (to keep
the session/authentication canonical and emit UI-flavoured ops) and then
perform the three writes via authenticated JSON-RPC call_kw — this mirrors
what the browser client does under the hood (web_save / write).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


PROJECT_A = "Bench Proj A"
PROJECT_B = "Bench Proj B"

TASK_ALPHA = "Bench Task Alpha"
TASK_BRAVO = "Bench Task Bravo"
TASK_CHARLIE = "Bench Task Charlie"

TO_MOVE = [TASK_ALPHA, TASK_BRAVO, TASK_CHARLIE]


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    payload = {
        "project_b": PROJECT_B,
        "targets": TO_MOVE,
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

            const projRows = await callKw({
                model: 'project.project',
                method: 'search_read',
                args: [[['name', '=', payload.project_b]], ['id', 'name']],
                kwargs: { limit: 1 },
            });
            if (!projRows.length) {
                throw new Error('Missing destination project: ' + payload.project_b);
            }
            const projectBId = projRows[0].id;

            for (const taskName of payload.targets) {
                const rows = await callKw({
                    model: 'project.task',
                    method: 'search_read',
                    args: [[['name', '=', taskName]], ['id', 'project_id']],
                    kwargs: { limit: 1 },
                });
                if (!rows.length) {
                    throw new Error('Missing task: ' + taskName);
                }
                await callKw({
                    model: 'project.task',
                    method: 'web_save',
                    args: [[rows[0].id], { project_id: projectBId }],
                    kwargs: { specification: { id: {}, project_id: { fields: { display_name: {} } } } },
                });
            }
            return 'ok';
        }""",
        payload,
    )
    if response != "ok":
        raise RuntimeError(f"Oracle JSON-RPC failed: {response}")


run_oracle(oracle)
