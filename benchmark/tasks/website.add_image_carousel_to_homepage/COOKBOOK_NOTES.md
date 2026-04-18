# Cookbook notes — website.add_image_carousel_to_homepage

New Odoo 19 quirks and reusable patterns surfaced while building row 328.

## 1. `oe_structure oe_empty` marker on the `#wrap` div

Seeded pages must include both classes on the wrapping `<div id="wrap">` for the website builder to treat the body as a valid drop target. Without `oe_structure`, the dropzone arrows never render. Without `oe_empty`, the builder still drops but the sidebar won't show the "This page is empty — add a block" placeholder. Canonical seed arch:

```xml
<t t-call="website.layout">
    <div id="wrap" class="oe_structure oe_empty">
        ... content ...
    </div>
</t>
```

## 2. Image Gallery snippet labels are split

`addons/website/views/snippets/snippets.xml`:

```xml
<t t-snippet="website.s_image_gallery" string="Image Gallery" group="images" label="Carousel">
```

The sidebar category heading says **Image Gallery** (the `string=`), but the tile/variant in the "Insert a block" preview dialog has `aria-label="Carousel"` (the `label=`). For snippet-insertion tasks, put both strings in the prompt so whichever path the agent searches via, it finds a match.

## 3. JSON-RPC oracle shortcut for snippet insertion

Instead of scripting the drag from Playwright (known-fragile), write the new arch directly:

```python
page.evaluate("""async (payload) => {
  const resp = await fetch('/web/dataset/call_kw', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });
  return resp.json();
}""", {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "ir.ui.view",
        "method": "write",
        "args": [[view_id], {"arch": NEW_ARCH_WITH_SNIPPET}],
        "kwargs": {},
    },
})
```

The `arch` field accepts the full QWeb body including freshly-inserted snippet markup. `website.page.view_id` resolves to the single `ir.ui.view` that backs the page — no need to hop via `website.controller_page` or similar. This pattern applies to any "add a snippet / edit a structural block" task where the iframe editor would otherwise be the only path.

## 4. Calibration quirk: click-to-insert beats drag

BU-1.0 skipped the drag affordance entirely and used the snippet preview dialog's click-based insertion. If a task was sized assuming only drag works, expect it to be easier than advertised. For true hard-tier difficulty with the builder, force a path that requires interaction inside the iframe after insertion (rename a block, change a snippet option in the right panel, etc.) — bare "insert and save" is now demonstrably within BU's reach.

## 5. State-diff pattern for "content-only" edits

When a task only modifies `ir.ui.view.arch` but not any `website.page` scalar field (name / url / is_published unchanged), `state_spec.yaml` can still track `website.page` so the diff engine has something to reason about, but `expected_state.json` is an empty list. Verification lives entirely in `check.py` via `page.view_id.arch_db`. Keeps F1 = 1.0 stable without phantom edits.
