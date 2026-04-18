"""Oracle for website.add_image_snippet_swap_source.

The canonical success shape is the seeded page `/bench-image-page` with an
Image snippet dropped into the page body and its `<img>` src swapped to
`/web/image/website.library_image_10`.  The Odoo 19 website builder's
snippet drag-and-drop + media dialog flow is notoriously hard to script
reliably from Playwright (iframe drop-zones jitter, media dialogs load
the library tab asynchronously).  This oracle therefore takes the
JSON-RPC shortcut: log in, open the editor once so the asset pipeline is
warm, then overwrite the underlying `ir.ui.view` arch via
`/web/dataset/call_kw` with the expected persisted shape.  The browser
agent must still solve the task via UI drag + media swap.
"""

import json

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
    _wait_no_loading,
)


# The arch for the seeded page WITH an Image snippet inserted after the
# heading section.  The inserted <img> has the target src so the check
# passes.  We use the `s_image` snippet wrapper class the Odoo 19 Image
# block renders to.
TARGET_ARCH = """
<t t-call="website.layout">
    <div id="wrap" class="oe_structure oe_empty">
        <section class="pt48 pb24">
            <div class="container">
                <h1 class="text-center mb-3">Our Image Showcase</h1>
                <p class="lead text-center">Add an Image block below and swap its source to the requested library image.</p>
            </div>
        </section>
        <section class="s_image_block pt24 pb24">
            <div class="container text-center">
                <img class="img img-fluid mx-auto s_image" src="/web/image/website.library_image_10" alt="" data-name="Image"/>
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
        "?path=%2Fbench-image-page&enable_editor=1"
    )
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Find the target view id for /bench-image-page via JSON-RPC.
    pages = _call_kw(
        page,
        "website.page",
        "search_read",
        [[("url", "=", "/bench-image-page")], ["id", "view_id"]],
        {"limit": 1},
    )
    if not pages:
        raise RuntimeError("Seeded page /bench-image-page not found")
    view_id = pages[0]["view_id"][0]

    # Write the new arch directly — this is the canonical persisted form
    # of "Image snippet added + src swapped via builder + Save".
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
