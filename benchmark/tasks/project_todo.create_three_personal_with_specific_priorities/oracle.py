"""Oracle for project_todo.create_three_personal_with_specific_priorities.

Approach: log in, navigate to /odoo/to-do so the session is on the right
controller, then use the authenticated /web/dataset/call_kw endpoint to
create the three personal to-do notes with the expected priority values.
This mirrors what the browser client does under the hood (web_save / create).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


TODOS = [
    {"name": "Plan Sprint", "priority": "1"},
    {"name": "Write Docs", "priority": "0"},
    {"name": "Refactor CSS", "priority": "0"},
]


def oracle(page):
    login(page)
    navigate(page, "/odoo/to-do")
    page.wait_for_timeout(1000)

    response = page.evaluate(
        """async (todos) => {
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

            // Find the admin user id so the new tasks belong to the current user
            const session = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!session.length) {
                throw new Error('admin user not found');
            }
            const adminId = session[0].id;

            for (const t of todos) {
                await callKw({
                    model: 'project.task',
                    method: 'create',
                    args: [[{
                        name: t.name,
                        priority: t.priority,
                        user_ids: [[6, 0, [adminId]]],
                        project_id: false,
                        active: true,
                    }]],
                    kwargs: {},
                });
            }
            return 'ok';
        }""",
        TODOS,
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
