"""Oracle for website.create_contact_form_block.

The canonical success shape is the seeded page `/bench-contact-form` with a
Form snippet dropped into the body, its `data-model_name` set to
`res.partner`, the default Subject field kept, and a new 'Your Message'
custom Long Text field added.  The Odoo 19 website builder's snippet
drag-and-drop + model-switch + custom-field flow is extremely hard to
script reliably from Playwright (the form options panel re-renders on
every model change, the custom field badges jitter).  This oracle
therefore takes the JSON-RPC shortcut: log in, open the editor once so
the asset pipeline is warm, then overwrite the underlying `ir.ui.view`
arch via `/web/dataset/call_kw` with the expected persisted shape.  The
browser agent must still solve the task via UI drag + options editing.
"""

import json

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
    _wait_no_loading,
)


# The arch for the seeded page WITH a Form snippet configured for
# res.partner, the default Subject field kept, and a 'Your Message'
# textarea (Long Text) custom field appended.  This matches the persisted
# shape after doing the task via the website builder UI.
TARGET_ARCH = """
<t t-call="website.layout">
    <div id="wrap" class="oe_structure oe_empty">
        <section class="pt48 pb24">
            <div class="container">
                <h1 class="text-center mb-3">Contact Us</h1>
                <p class="lead text-center">Add a Form block below, point it at Contact (res.partner), keep the Subject field, and add a 'Your Message' Long Text field.</p>
            </div>
        </section>
        <section class="s_website_form pt16 pb16" data-vcss="001" data-snippet="s_website_form">
            <div class="container-fluid">
                <form action="/website/form/" method="post" enctype="multipart/form-data" class="o_mark_required" data-mark="*" data-pre-fill="true" data-model_name="res.partner" data-success-mode="redirect" data-success-page="/contactus-thank-you">
                    <div class="s_website_form_rows row s_col_no_bgcolor">
                        <div data-name="Field" class="s_website_form_field mb-3 col-12 s_website_form_model_required" data-type="char">
                            <div class="row s_col_no_resize s_col_no_bgcolor">
                                <label class="col-form-label col-sm-auto s_website_form_label" style="width: 200px" for="bcf_subject">
                                    <span class="s_website_form_label_content">Subject</span>
                                    <span class="s_website_form_mark"> *</span>
                                </label>
                                <div class="col-sm">
                                    <input class="form-control s_website_form_input" type="text" name="subject" required="" id="bcf_subject"/>
                                </div>
                            </div>
                        </div>
                        <div data-name="Field" class="s_website_form_field mb-3 col-12 s_website_form_custom" data-type="text">
                            <div class="row s_col_no_resize s_col_no_bgcolor">
                                <label class="col-form-label col-sm-auto s_website_form_label" style="width: 200px" for="bcf_your_message">
                                    <span class="s_website_form_label_content">Your Message</span>
                                </label>
                                <div class="col-sm">
                                    <textarea class="form-control s_website_form_input" name="Your Message" id="bcf_your_message" rows="3"></textarea>
                                </div>
                            </div>
                        </div>
                        <div class="mb-0 py-2 col-12 s_website_form_submit text-end s_website_form_no_submit_label" data-name="Submit Button">
                            <div style="width: 200px;" class="s_website_form_label"/>
                            <span id="s_website_form_result"/>
                            <a href="#" role="button" class="btn btn-primary s_website_form_send">Submit</a>
                        </div>
                    </div>
                </form>
            </div>
        </section>
    </div>
</t>
"""


def _call_kw(page, model, method, args, kwargs=None):
    """Run a JSON-RPC call_kw from the browser context."""
    kwargs = kwargs or {}
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args,
            "kwargs": kwargs,
        },
    }
    result = page.evaluate(
        """async (payload) => {
            const resp = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload),
            });
            return resp.json();
        }""",
        payload,
    )
    if isinstance(result, dict) and result.get("error"):
        raise RuntimeError(
            f"call_kw {model}.{method} error: {json.dumps(result['error'])[:500]}"
        )
    return result.get("result") if isinstance(result, dict) else result


def oracle(page):
    login(page)

    # Open the builder briefly so the editor asset pipeline loads and the
    # post-task state capture sees a warm editor.
    editor_url = (
        "/odoo/action-website.website_preview"
        "?path=%2Fbench-contact-form&enable_editor=1"
    )
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Find the target view id for /bench-contact-form via JSON-RPC.
    pages = _call_kw(
        page,
        "website.page",
        "search_read",
        [[("url", "=", "/bench-contact-form")], ["id", "view_id"]],
        {"limit": 1},
    )
    if not pages:
        raise RuntimeError("Seeded page /bench-contact-form not found")
    view_id = pages[0]["view_id"][0]

    # Write the new arch directly — this is the canonical persisted form
    # of "Form snippet added + model switched + custom field appended +
    # Save".
    _call_kw(
        page,
        "ir.ui.view",
        "write",
        [[view_id], {"arch": TARGET_ARCH}],
    )

    # Give Odoo a beat to flush, then navigate away so any idle bus
    # notifications settle before the run harness snapshots state.
    page.wait_for_timeout(1000)
    page.goto(full_url("/odoo"))
    page.wait_for_load_state("load")
    _wait_no_loading(page)


run_oracle(oracle)
