"""Oracle for website.add_menu_item_reorder.

Uses the same ``website.menu.save`` JSON-RPC entrypoint that the Website
app's Menu Editor dialog uses when saving. Creates a new top-level menu
entry 'Bench Menu' pointing to '/bench-menu-target' and assigns it a
sequence of 15 — strictly between Home (10) and Bench Contact (20) — so
it ends up in position 2 of the top-level navigation.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/website")
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

            // 1. Load the current menu tree for website 1.
            const tree = await callKw({
                model: 'website.menu',
                method: 'get_tree',
                args: [1],
                kwargs: {},
            });

            const rootId = tree.fields.id;
            const data = [];

            // Preserve existing top-level children as-is. We keep their
            // existing sequences so the seeded Home(10) / Bench Contact(20)
            // window remains intact.
            for (const child of tree.children) {
                data.push({
                    id: child.fields.id,
                    name: child.fields.name,
                    url: child.fields.url,
                    new_window: child.fields.new_window,
                    is_mega_menu: child.fields.is_mega_menu,
                    sequence: child.fields.sequence,
                    parent_id: rootId,
                });
            }

            // 2. Append the new Bench Menu entry with sequence=15 so it
            //    slots between Home(10) and Bench Contact(20).
            data.push({
                id: 'new-bench-menu',
                name: 'Bench Menu',
                url: '/bench-menu-target',
                new_window: false,
                is_mega_menu: false,
                sequence: 15,
                parent_id: rootId,
            });

            await callKw({
                model: 'website.menu',
                method: 'save',
                args: [1, { data: data, to_delete: [] }],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
