"""Oracle for project.create_project_from_template_duplicate.

Calls ``project.project.copy()`` via JSON-RPC with a rename default.
Odoo's native ``copy()`` on ``project.project`` auto-clones tasks
through ``map_tasks``, so the resulting project contains copies of
"Setup", "Build", and "Review".
"""

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


PROJECT_NAME = "Bench Template Project"
COPY_NAME = "Bench Template Project (Copy)"
TASK_NAMES = ["Setup", "Build", "Review"]


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    response = page.evaluate(
        """async (params) => {
            const unwrap = (value) => Array.isArray(value) ? value[0] : value;
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
                throw new Error('Template project not found: ' + params.project_name);
            }
            const templateId = projects[0].id;

            // Clean out any pre-existing copy from a partial prior run so
            // we always end with exactly one copy.
            const existing = await callKw({
                model: 'project.project',
                method: 'search_read',
                args: [[['name', '=', params.copy_name]], ['id']],
                kwargs: {},
            });
            if (existing.length) {
                const existingIds = existing.map(p => p.id);
                const existingTasks = await callKw({
                    model: 'project.task',
                    method: 'search',
                    args: [[['project_id', 'in', existingIds]]],
                    kwargs: { context: { active_test: false } },
                });
                if (existingTasks.length) {
                    await callKw({
                        model: 'project.task',
                        method: 'unlink',
                        args: [existingTasks],
                        kwargs: {},
                    });
                }
                await callKw({
                    model: 'project.project',
                    method: 'unlink',
                    args: [existingIds],
                    kwargs: {},
                });
            }

            // copy() on project.project auto-clones its tasks via map_tasks
            const newId = unwrap(await callKw({
                model: 'project.project',
                method: 'copy',
                args: [[templateId]],
                kwargs: { default: { name: params.copy_name } },
            }));

            // Ensure the name is exactly what we want (in case the default
            // chain appended "(copy)" or similar).
            await callKw({
                model: 'project.project',
                method: 'write',
                args: [[newId], { name: params.copy_name }],
                kwargs: {},
            });

            // Verify tasks were duplicated; if not, create them explicitly.
            const tasks = await callKw({
                model: 'project.task',
                method: 'search_read',
                args: [[['project_id', '=', newId]], ['name']],
                kwargs: {},
            });
            const haveNames = new Set(tasks.map(t => t.name));
            for (const tname of params.task_names) {
                if (!haveNames.has(tname)) {
                    await callKw({
                        model: 'project.task',
                        method: 'create',
                        args: [[{ name: tname, project_id: newId }]],
                        kwargs: {},
                    });
                }
            }

            return 'ok';
        }""",
        {
            "project_name": PROJECT_NAME,
            "copy_name": COPY_NAME,
            "task_names": TASK_NAMES,
        },
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
