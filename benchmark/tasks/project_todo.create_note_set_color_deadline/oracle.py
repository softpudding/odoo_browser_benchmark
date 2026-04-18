"""Oracle for project_todo.create_note_set_color_deadline."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/to-do")
    response = page.evaluate(
        """async () => {
            const unwrapId = (value) => Array.isArray(value) ? value[0] : value;
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

            const adminRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!adminRes.length) {
                throw new Error('admin user not found');
            }
            const adminId = adminRes[0].id;
            const taskId = unwrapId(await callKw({
                model: 'project.task',
                method: 'create',
                args: [[{
                    name: 'Crane Audit Memo',
                    user_ids: [[6, 0, [adminId]]],
                    date_deadline: '2026-05-20',
                    color: 3,
                }]],
                kwargs: {},
            }));
            if (!taskId) {
                throw new Error('failed to create todo');
            }
            await callKw({
                model: 'project.task',
                method: 'write',
                args: [[taskId], { user_ids: [[5, 0, 0]] }],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
