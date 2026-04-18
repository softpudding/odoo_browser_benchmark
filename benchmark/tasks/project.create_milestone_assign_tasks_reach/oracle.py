"""Oracle for project.create_milestone_assign_tasks_reach.

Deterministic path: open the Project app, use the project's kebab menu
"Milestones" action to create the milestone via the inline-editable list
view, then open each of T1/T2's task forms and set milestone_id via the
autocomplete, save, and finally flip is_reached on the milestone.

Milestone create + task write are UI fragile (inline-row save + many2one
autocomplete). The oracle performs them via JSON-RPC call_kw after
logging in — this is the documented oracle bypass pattern in
ODOO19_PATTERNS.md for noisy form widgets. Browser-use must still solve
via UI.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


PROJECT_NAME = "Bench Milestone Proj"
MILESTONE_NAME = "Phase 1 Complete"
MILESTONE_DEADLINE = "2026-06-01"

TASK_T1 = "T1 - Draft Spec"
TASK_T2 = "T2 - Build Prototype"
ASSIGNED_TASKS = [TASK_T1, TASK_T2]


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    payload = {
        "project_name": PROJECT_NAME,
        "milestone_name": MILESTONE_NAME,
        "milestone_deadline": MILESTONE_DEADLINE,
        "tasks_to_assign": ASSIGNED_TASKS,
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
                args: [[['name', '=', payload.project_name]], ['id', 'name']],
                kwargs: { limit: 1 },
            });
            if (!projRows.length) {
                throw new Error('Missing project: ' + payload.project_name);
            }
            const projectId = projRows[0].id;

            // 1. Create the milestone (is_reached False for now).
            const milestoneId = await callKw({
                model: 'project.milestone',
                method: 'create',
                args: [{
                    name: payload.milestone_name,
                    project_id: projectId,
                    deadline: payload.milestone_deadline,
                }],
                kwargs: {},
            });

            // 2. Assign T1 + T2 to the milestone via web_save
            //    (simulates the per-task form Save). T3 is left alone.
            for (const taskName of payload.tasks_to_assign) {
                const taskRows = await callKw({
                    model: 'project.task',
                    method: 'search_read',
                    args: [[
                        ['name', '=', taskName],
                        ['project_id', '=', projectId],
                    ], ['id']],
                    kwargs: { limit: 1 },
                });
                if (!taskRows.length) {
                    throw new Error('Missing task: ' + taskName);
                }
                await callKw({
                    model: 'project.task',
                    method: 'web_save',
                    args: [[taskRows[0].id], { milestone_id: milestoneId }],
                    kwargs: {
                        specification: {
                            id: {},
                            milestone_id: { fields: { display_name: {} } },
                        },
                    },
                });
            }

            // 3. Flip is_reached to True on the milestone.
            await callKw({
                model: 'project.milestone',
                method: 'write',
                args: [[milestoneId], { is_reached: true }],
                kwargs: {},
            });

            return 'ok';
        }""",
        payload,
    )
    if response != "ok":
        raise RuntimeError(f"Oracle JSON-RPC failed: {response}")


run_oracle(oracle)
