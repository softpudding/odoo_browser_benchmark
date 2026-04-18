# Cookbook notes — website_sale.set_product_seo_title_meta

New / reinforced Odoo 19 quirks picked up while building this easy task:

## SEO fields live on a mixin, not on the product form

- `product.template` inherits `website.seo.metadata` → adds `website_meta_title` (Char), `website_meta_description` (Text), `website_meta_keywords` (Char), plus the computed `is_seo_optimized`.
- **None** of those fields are rendered in `product_template_form_view` or any of its website_sale inherits. The only canonical UI path is the frontend **Site ▸ This Page ▸ Optimize SEO** dialog (Owl component `OptimizeSEODialog`, registered under `website.menu_optimize_seo`).
- The dialog is visible only when `website.currentWebsite.metadata.canOptimizeSeo` is truthy, which requires the current URL to map to a `website.seo.metadata` record (product shop page, blog post, landing page, …).

## Two ways BU can reach the dialog for a product

1. Kanban card click on `/odoo/ecommerce-products` → opens the front-end shop page inside the website preview action (because `product_pages_tree_view.action = open_website_url`, but the default `product_template_action_website` still routes to the backend form).
2. Backend product form → click the **`is_published`** header widget (labeled "Go to Website") → lands on the shop page. BU used this path in the calibration run.

Both paths end on `/shop/<product-slug>` inside the `website.website_preview` client action, where the Site menu is available.

## Expected-state-diff surprises

- `is_seo_optimized` is computed+stored, so flipping either of the two meta fields to truthy auto-bumps it from False → True. Either list it in `expected_state.json` or add it to `ignore_fields` (we chose ignore since it's derivative).
- `website_meta_title` and `website_meta_description` normalize to the plain string (`translate=True` has no effect on the diff payload for single-language DBs).
- `is_published` does not appear in the diff when it starts True and stays True — no extra noise.

## Oracle pattern

JSON-RPC `write` on `product.template` is the cleanest oracle. The frontend SEO dialog is Owl + iframe; scripting it via Playwright is possible but pointless for an oracle. `call_kw` writes bypass the dialog and leave the exact two-field diff the browser-use run would produce.

## Seed tip

Create the product with `is_published=True` directly. The `product_template_action_website` view applies `search_default_published=1`, so an unpublished product would be hidden and force BU to clear filters before finding it (harder than intended for an easy task).
