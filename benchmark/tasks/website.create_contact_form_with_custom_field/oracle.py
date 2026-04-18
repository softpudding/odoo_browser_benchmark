"""Oracle for website.create_contact_form_with_custom_field.

The website builder iframe is far too fragile to drive deterministically (the
options panel re-mounts on every option change, the field-type selector is a
custom Owl dropdown, and adding an option requires clicking a tiny "+" button
inside a re-rendered list). This oracle takes the JSON-RPC bypass route allowed
by the benchmark spec for oracle.py only: it writes a Selection field directly
into the page's underlying ``ir.ui.view`` arch.

The resulting markup matches what the website builder produces when a user adds
a custom Selection field with three options: a ``s_website_form_field`` div
with ``data-type="selection"`` and ``s_website_form_required`` class, containing
a ``s_website_form_multiple`` row with three radio inputs sharing the same
``name`` (slugified label).
"""

from benchmark.oracle_helpers import login, full_url, run_oracle


SELECTION_FIELD_HTML = (
    '<div data-name="Field" '
    'class="s_website_form_field mb-3 col-12 s_website_form_custom s_website_form_required" '
    'data-type="selection">'
    '<div class="row s_col_no_resize s_col_no_bgcolor">'
    '<label class="col-form-label col-sm-auto s_website_form_label" '
    'style="width: 200px" for="bench_inquiry_type">'
    '<span class="s_website_form_label_content">Inquiry Type</span>'
    '<span class="s_website_form_mark"> *</span>'
    '</label>'
    '<div class="col-sm">'
    '<div class="row s_col_no_resize s_col_no_bgcolor s_website_form_multiple" '
    'data-name="Inquiry Type" data-display="horizontal">'
    '<div class="radio col-12 col-lg-4 col-md-6">'
    '<div class="form-check">'
    '<input type="radio" class="s_website_form_input form-check-input" '
    'id="bench_inquiry_type0" name="Inquiry Type" value="Sales" required="1"/>'
    '<label class="form-check-label s_website_form_check_label" '
    'for="bench_inquiry_type0">Sales</label>'
    '</div>'
    '</div>'
    '<div class="radio col-12 col-lg-4 col-md-6">'
    '<div class="form-check">'
    '<input type="radio" class="s_website_form_input form-check-input" '
    'id="bench_inquiry_type1" name="Inquiry Type" value="Support" required="1"/>'
    '<label class="form-check-label s_website_form_check_label" '
    'for="bench_inquiry_type1">Support</label>'
    '</div>'
    '</div>'
    '<div class="radio col-12 col-lg-4 col-md-6">'
    '<div class="form-check">'
    '<input type="radio" class="s_website_form_input form-check-input" '
    'id="bench_inquiry_type2" name="Inquiry Type" value="Partnership" required="1"/>'
    '<label class="form-check-label s_website_form_check_label" '
    'for="bench_inquiry_type2">Partnership</label>'
    '</div>'
    '</div>'
    '</div>'
    '</div>'
    '</div>'
    '</div>'
)


def oracle(page):
    login(page)

    # Use the same /web/dataset/call_kw entry point a normal browser session
    # uses. We:
    #   1. find the website.page record at /contactus-bench
    #   2. read its view_id arch
    #   3. inject the Selection field markup just before the Submit button div
    #   4. write the new arch back to the view (this is the same field the
    #      builder save would update).
    page.goto(full_url("/odoo"))
    page.wait_for_load_state("load")
    page.wait_for_selector(".o_action_manager, .o_home_menu", timeout=30000)

    field_html = SELECTION_FIELD_HTML

    response = page.evaluate(
        """async (fieldHtml) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0', method: 'call', params: payload,
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

            const pages = await callKw({
                model: 'website.page',
                method: 'search_read',
                args: [[['url', '=', '/contactus-bench']],
                       ['id', 'view_id']],
                kwargs: {limit: 1},
            });
            if (!pages.length) {
                throw new Error('contactus-bench page not found');
            }
            const viewId = pages[0].view_id[0];

            const views = await callKw({
                model: 'ir.ui.view',
                method: 'read',
                args: [[viewId], ['arch_db', 'arch']],
                kwargs: {},
            });
            let arch = views[0].arch;

            // Insert just before the Submit button container.
            const marker = '<div class="mb-0 py-2 col-12 s_website_form_submit';
            const idx = arch.indexOf(marker);
            if (idx === -1) {
                throw new Error('submit button marker not found in arch');
            }
            arch = arch.slice(0, idx) + fieldHtml + arch.slice(idx);

            await callKw({
                model: 'ir.ui.view',
                method: 'write',
                args: [[viewId], {arch: arch}],
                kwargs: {},
            });

            // Make sure the page is still published.
            await callKw({
                model: 'website.page',
                method: 'write',
                args: [[pages[0].id], {is_published: true}],
                kwargs: {},
            });

            return 'ok';
        }""",
        field_html,
    )
    if response != "ok":
        raise RuntimeError(f"oracle JSON-RPC failed: {response}")


run_oracle(oracle)
