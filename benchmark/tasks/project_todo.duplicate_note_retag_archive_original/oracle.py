"""Oracle for project_todo.duplicate_note_retag_archive_original."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/to-do")
    response = page.evaluate(
        """async () => {
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

            const original = await callKw({
                model: 'project.task',
                method: 'search_read',
                args: [[['name', '=', 'Welcome Administrator!']], ['id', 'user_ids', 'description']],
                kwargs: { limit: 1 },
            });
            const tag = await callKw({
                model: 'project.tags',
                method: 'search_read',
                args: [[['name', '=', 'Harbor Ops']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!original.length || !tag.length) {
                throw new Error('missing original task or follow-up tag');
            }

            await callKw({
                model: 'project.task',
                method: 'create',
                args: [[{
                    name: 'Welcome Administrator Follow-up',
                    user_ids: [[6, 0, original[0].user_ids || []]],
                    description: original[0].description || false,
                    tag_ids: [[6, 0, [tag[0].id]]],
                    active: true,
                }]],
                kwargs: {},
            });
            await callKw({
                model: 'project.task',
                method: 'write',
                args: [[original[0].id], { active: false }],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
