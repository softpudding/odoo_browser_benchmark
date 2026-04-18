"""Oracle for project.recurring_task_configure_frequency.

Uses JSON-RPC inside the logged-in browser to flip the seeded task to
recurring with weekly cadence and an end date 8 weeks out.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


PROJECT_NAME = "Bench Recurring Project"
TASK_NAME = "Weekly Status Update"
REPEAT_UNTIL = "2026-06-13"


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    response = page.evaluate(
        """async (params) => {
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

            const projects = await callKw({
                model: 'project.project',
                method: 'search_read',
                args: [[['name', '=', params.project_name]], ['id']],
                kwargs: {},
            });
            if (!projects.length) {
                throw new Error('Project not found: ' + params.project_name);
            }
            const projectId = projects[0].id;

            const tasks = await callKw({
                model: 'project.task',
                method: 'search_read',
                args: [
                    [
                        ['name', '=', params.task_name],
                        ['project_id', '=', projectId],
                    ],
                    ['id'],
                ],
                kwargs: {},
            });
            if (!tasks.length) {
                throw new Error('Task not found: ' + params.task_name);
            }
            const taskId = tasks[0].id;

            // Write recurring_task + rec_fields in one call so that the
            // server-side write() creates the recurrence with the chosen
            // values (see project.task.write: rec_fields go to the new
            // recurrence record when recurring_task flips True).
            await callKw({
                model: 'project.task',
                method: 'web_save',
                args: [
                    [taskId],
                    {
                        recurring_task: true,
                        repeat_interval: 1,
                        repeat_unit: 'week',
                        repeat_type: 'until',
                        repeat_until: params.repeat_until,
                    },
                ],
                kwargs: { specification: { id: {} } },
            });

            return 'ok';
        }""",
        {
            "project_name": PROJECT_NAME,
            "task_name": TASK_NAME,
            "repeat_until": REPEAT_UNTIL,
        },
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
