"""Oracle for website.create_new_page_publish.

Logs in, navigates to the Website backend, then uses authenticated JSON-RPC
to:
  1. Call website.new_page with name='Bench New Page' (mirrors what the
     '+ New > Page' dialog does from the UI).
  2. Write is_published=True and a minimal arch containing the H1
     'Welcome to Bench' on the created view (mirrors Save + Publish from
     the website editor).
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PAGE_NAME = "Bench New Page"
PAGE_URL = "/bench-new-page"
HEADING_TEXT = "Welcome to Bench"

PAGE_ARCH = """<t name="Bench New Page" t-name="website.bench_new_page">
    <t t-call="website.layout">
        <div id="wrap" class="oe_structure oe_empty">
            <section class="s_text_block pt48 pb48">
                <div class="container">
                    <h1>Welcome to Bench</h1>
                </div>
            </section>
        </div>
    </t>
</t>"""


def oracle(page):
    login(page)
    navigate(page, "/odoo/website")
    page.wait_for_timeout(800)

    payload = {
        "page_name": PAGE_NAME,
        "page_url": PAGE_URL,
        "page_arch": PAGE_ARCH,
    }

    result = page.evaluate(
        """async (p) => {
            const unwrap = (v) => Array.isArray(v) ? v[0] : v;
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

            // 1. Create the new page via website.new_page (same entrypoint
            //    as the '+ New > Page' dialog uses).
            const newPageResult = await callKw({
                model: 'website',
                method: 'new_page',
                args: [],
                kwargs: {
                    name: p.page_name,
                    add_menu: false,
                    template: 'website.default_page',
                    ispage: true,
                },
            });

            if (!newPageResult || !newPageResult.page_id) {
                throw new Error('new_page did not return a page_id: ' + JSON.stringify(newPageResult));
            }
            const pageId = newPageResult.page_id;
            const viewId = newPageResult.view_id;

            // 2. Force the url + publish state on the page.
            await callKw({
                model: 'website.page',
                method: 'write',
                args: [[pageId], {
                    url: p.page_url,
                    name: p.page_name,
                    is_published: true,
                    website_published: true,
                }],
                kwargs: {},
            });

            // 3. Write the arch with the required H1 heading on the view.
            await callKw({
                model: 'ir.ui.view',
                method: 'write',
                args: [[viewId], { arch: p.page_arch }],
                kwargs: {},
            });

            const after = await callKw({
                model: 'website.page',
                method: 'read',
                args: [[pageId],
                       ['name', 'url', 'is_published', 'website_published']],
                kwargs: {},
            });
            return JSON.stringify({
                page_id: pageId,
                view_id: viewId,
                after,
            });
        }""",
        payload,
    )
    print("Oracle created:", result)


run_oracle(oracle)
