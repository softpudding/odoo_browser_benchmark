# website_sale.set_product_seo_title_meta — calibration result

- **Difficulty target:** easy (~80% BU pass)
- **Tier:** 1, `time_limit_sec: 240`, `step_limit: 120`
- **Oracle run:** PASS — StateDiffF1 1.0, 2/2 edits matched, wall clock 17.6s
- **Browser-use run:** PASS — StateDiffF1 1.0, 2/2 edits matched, 11 BU steps, wall clock 81.9s
  - BU path: `/odoo/ecommerce-products` → click product card → click form header "Go to Website" → Site menu → Optimize SEO → fill Title + Description → Save.
- **Calibration verdict:** PASS — easy target satisfied on first shot.

## Agent behavior notes

- BU reached the Optimize SEO dialog through the **form-header "Go to Website"** button rather than clicking the kanban card directly (our prompt allowed either path). It then opened the Site dropdown and clicked "Optimize SEO" without confusion.
- The SEO dialog exposes two plain `<input>` / `<textarea>` fields (Title + Description) and a primary "Save" button; BU had no trouble with the dialog itself.
- No forbidden ops triggered; HarmfulWriteRate 0.0.

## Design choices

- **Seed** creates a published product with empty `website_meta_title` / `website_meta_description` so the expected state diff is exactly two atomic `set` edits.
- **Oracle** uses a JSON-RPC bypass (`product.template.write`) — robust against the frontend iframe/Owl dialog, no Playwright flakiness.
- **expected_state.json** only asserts the two SEO fields. `is_published` is unchanged (true → true), so it does NOT appear in the diff (the engine emits only changed values). `is_seo_optimized` is a computed field that flips when either of the meta fields becomes truthy; it's in `ignore_fields` to avoid noise.
