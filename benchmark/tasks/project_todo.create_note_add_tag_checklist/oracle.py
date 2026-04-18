"""Oracle for project_todo.create_note_add_tag_checklist.

Approach: log in, navigate to /odoo/to-do so the session is bound to the
To-do controller, then use /web/dataset/call_kw to create a personal
project.task named 'Bench Todo Note' assigned to the admin user,
tagged with 'BenchTag', with a description that contains a checklist
item 'First step' (Odoo 19 uses <ul class="o_checklist"><li>...</li></ul>).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


TARGET_NAME = "Bench Todo Note"
TARGET_TAG = "BenchTag"
CHECKLIST_ITEM = "First step"


def oracle(page):
    login(page)
    navigate(page, "/odoo/to-do")
    page.wait_for_timeout(800)

    response = page.evaluate(
        """async (payload) => {
            const unwrapId = (value) => Array.isArray(value) ? value[0] : value;
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

            let tagRes = await callKw({
                model: 'project.tags',
                method: 'search_read',
                args: [[['name', '=', payload.tag]], ['id']],
                kwargs: { limit: 1 },
            });
            let tagId;
            if (tagRes.length) {
                tagId = tagRes[0].id;
            } else {
                tagId = unwrapId(await callKw({
                    model: 'project.tags',
                    method: 'create',
                    args: [[{ name: payload.tag }]],
                    kwargs: {},
                }));
            }

            const description = (
                '<p>Checklist:</p>'
                + '<ul class="o_checklist">'
                + '<li id="checkId-oracle-1">' + payload.item + '</li>'
                + '</ul>'
            );

            const taskId = unwrapId(await callKw({
                model: 'project.task',
                method: 'create',
                args: [[{
                    name: payload.name,
                    user_ids: [[6, 0, [adminId]]],
                    tag_ids: [[6, 0, [tagId]]],
                    description: description,
                    project_id: false,
                    active: true,
                }]],
                kwargs: {},
            }));
            if (!taskId) {
                throw new Error('failed to create todo');
            }
            return 'ok';
        }""",
        {"name": TARGET_NAME, "tag": TARGET_TAG, "item": CHECKLIST_ITEM},
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
