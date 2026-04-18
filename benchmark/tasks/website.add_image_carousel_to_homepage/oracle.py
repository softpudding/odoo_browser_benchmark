"""Oracle for website.add_image_carousel_to_homepage.

The canonical "success" shape is an Image Gallery snippet on
`/bench-gallery-test` with at least three `<img>` children.  The Odoo 19
website builder's snippet drag-and-drop flow is notoriously hard to
script reliably from Playwright (iframe drop-zones jitter, the snippet
preview dialog can open as a variant picker, and the dropzone target
varies by viewport).  This oracle therefore takes the JSON-RPC shortcut
permitted for oracle scripts by ODOO19_PATTERNS.md: log in, open the
editor once so the view is loaded, then overwrite the underlying
`ir.ui.view` arch via `/web/dataset/call_kw`.  The benchmark agent
(browser-use) must still solve the task via UI drag.
"""

import json

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
    _wait_no_loading,
)


# The arch for the seeded page WITH the Image Gallery snippet inserted
# after the heading section.  Three carousel-item <img> children keep the
# `arch_db.count('<img') >= 3` check satisfied.
TARGET_ARCH = """
<t t-call="website.layout">
    <div id="wrap" class="oe_structure oe_empty">
        <section class="pt48 pb24">
            <div class="container">
                <h1 class="text-center mb-3">Our Portfolio</h1>
                <p class="lead text-center">Add an image gallery below to showcase recent work.</p>
            </div>
        </section>
        <section class="s_image_gallery o_slideshow pt24 pb24 s_image_gallery_controllers_outside s_image_gallery_indicators_dots s_image_gallery_arrows_default" data-vcss="002" data-columns="3">
            <div class="o_container_small overflow-hidden">
                <div id="slideshow_bench_sample" class="carousel carousel-dark slide" data-bs-ride="carousel" data-bs-interval="0">
                    <div class="carousel-inner">
                        <div class="carousel-item active">
                            <img class="img img-fluid d-block mh-100 mw-100 mx-auto rounded object-fit-cover" src="/web/image/website.library_image_08" data-name="Image" data-index="0" alt=""/>
                        </div>
                        <div class="carousel-item">
                            <img class="img img-fluid d-block mh-100 mw-100 mx-auto rounded object-fit-cover" src="/web/image/website.library_image_03" data-name="Image" data-index="1" alt=""/>
                        </div>
                        <div class="carousel-item">
                            <img class="img img-fluid d-block mh-100 mw-100 mx-auto rounded object-fit-cover" src="/web/image/website.library_image_02" data-name="Image" data-index="2" alt=""/>
                        </div>
                    </div>
                </div>
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
        raise RuntimeError(f"call_kw {model}.{method} error: {json.dumps(result['error'])[:500]}")
    return result.get("result") if isinstance(result, dict) else result


def oracle(page):
    login(page)

    # Open the builder briefly — this also exercises the editor asset
    # pipeline and reveals save_button so that the post-task state
    # capture sees a sane arch layout.
    editor_url = (
        "/odoo/action-website.website_preview"
        "?path=%2Fbench-gallery-test&enable_editor=1"
    )
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Find the target view id for /bench-gallery-test via JSON-RPC.
    pages = _call_kw(
        page,
        "website.page",
        "search_read",
        [[("url", "=", "/bench-gallery-test")], ["id", "view_id"]],
        {"limit": 1},
    )
    if not pages:
        raise RuntimeError("Seeded page /bench-gallery-test not found")
    view_id = pages[0]["view_id"][0]

    # Write the new arch directly — this is the canonical persisted form
    # of "snippet added via builder + Save".
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
