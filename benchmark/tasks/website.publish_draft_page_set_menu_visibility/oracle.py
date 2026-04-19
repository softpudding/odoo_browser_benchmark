"""Oracle for website.publish_draft_page_set_menu_visibility.

Two-phase JSON-RPC solve (oracles are allowed to bypass brittle UI,
per ODOO19_PATTERNS.md):

  1. write({'is_published': True, 'website_published': True}) on the
     seeded /about-us website.page.
  2. Call website.menu.save(website_id, {data, to_delete}) with a new
     top-level entry keyed by a temp-id string 'new-about-us' pointing
     at '/about-us'. The backend's website.menu.save auto-resolves
     page_id by matching the url to an existing website.page.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PAGE_URL = "/about-us"
MENU_NAME = "About Us"


def oracle(page):
    login(page)
    navigate(page, "/odoo/website-pages")
    page.wait_for_timeout(800)

    payload = {"page_url": PAGE_URL, "menu_name": MENU_NAME}

    response = page.evaluate(
        """async (p) => {
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0', method: 'call', params,
                    }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(
                        json.error.data?.message || json.error.message
                    );
                }
                return json.result;
            };

            // ---- Phase 1: publish the /about-us page. ----
            const pages = await callKw({
                model: 'website.page',
                method: 'search_read',
                args: [[['url', '=', p.page_url]],
                       ['id', 'name', 'is_published', 'website_published']],
                kwargs: { limit: 1 },
            });
            if (!pages.length) {
                throw new Error('Seeded page not found: ' + p.page_url);
            }
            const pageId = pages[0].id;
            await callKw({
                model: 'website.page',
                method: 'write',
                args: [[pageId], {
                    is_published: true,
                    website_published: true,
                }],
                kwargs: {},
            });

            // ---- Phase 2: add a new top-level menu entry for /about-us.
            // Use website.menu.create directly (with page_id resolved
            // locally) instead of website.menu.save — the save helper
            // iterates ALL existing children and writes page_id on each,
            // which introduces noisy side effects on the distractor
            // 'About' menu that shares a URL with the pre-existing
            // 'Contact us' menu.
            const websites = await callKw({
                model: 'website',
                method: 'read',
                args: [[1], ['menu_id']],
                kwargs: {},
            });
            const unwrap = (v) => Array.isArray(v) ? v[0] : v;
            const rootId = unwrap(websites[0].menu_id);

            await callKw({
                model: 'website.menu',
                method: 'create',
                args: [{
                    name: p.menu_name,
                    url: p.page_url,
                    parent_id: rootId,
                    website_id: 1,
                    page_id: pageId,
                    // Sequence 15 sits between Home (10) and every other
                    // top-level entry (Contact us=60, Shop=*, etc.)
                    // so About Us lands in the 2nd slot.
                    sequence: 15,
                }],
                kwargs: {},
            });

            // Sanity re-read.
            const after = await callKw({
                model: 'website.page',
                method: 'read',
                args: [[pageId],
                       ['is_published', 'website_published']],
                kwargs: {},
            });
            return JSON.stringify(after[0]);
        }""",
        payload,
    )
    print('Oracle wrote:', response)


run_oracle(oracle)
