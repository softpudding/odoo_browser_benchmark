"""Oracle for website.edit_menu_add_page_link.

Uses the same ``website.menu.save`` JSON-RPC entrypoint that the Website
app's Menu Editor dialog uses when saving. The backend auto-links the
new menu entry to the existing website.page at the same URL, and sets
``page_id`` accordingly.
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

            // 1. Load the current menu tree for website 1 so we know the
            //    root menu id and the existing top-level children.
            const tree = await callKw({
                model: 'website.menu',
                method: 'get_tree',
                args: [1],
                kwargs: {},
            });

            const rootId = tree.fields.id;
            const data = [];
            // Preserve existing top-level children as-is.
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
            // Append the new Benchmark Contact entry. The `id` must be a
            // fresh string prefixed like a temp-id so website.menu.save
            // knows to create it.
            data.push({
                id: 'new-benchmark-contact',
                name: 'Benchmark Contact',
                url: '/benchmark-contact',
                new_window: false,
                is_mega_menu: false,
                sequence: 100,
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
