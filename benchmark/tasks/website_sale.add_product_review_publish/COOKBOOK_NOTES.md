# Cookbook notes - website_sale.add_product_review_publish

New / reinforced Odoo 19 quirks picked up while building this medium task.

## The `website_sale.product_comment` view ships with `active=False`

- The `Customer Reviews` + star composer section on `/shop/<product>` is
  rendered by the `website_sale.product_comment` ir.ui.view (defined in
  `addons/website_sale/views/templates.xml:2566`), which is declared with
  `active="False"`. Without explicit activation, the accordion is
  completely absent from the product page, no `is_view_active` gate
  fires, and the task is unsolvable.
- Seed **must** activate it:

  ```python
  env["ir.ui.view"].with_context(active_test=False).search(
      [("key", "=", "website_sale.product_comment")]
  ).write({"active": True})
  ```

- Search with `active_test=False` because a failed prior run may have
  left a disabled copy. Writing `active=True` is idempotent.

## `product.template` already inherits `rating.mixin`

- `addons/website_sale/models/product_template.py:36` extends
  `product.template` with `_inherit = ['rating.mixin', ...]`, which
  adds `rating_ids`, `rating_count`, `rating_avg`, and the
  `message_post(rating_value=...)` override from
  `rating/models/mail_thread.py`.
- `portal_rating` is `auto_install=True` when `portal` + `rating` are
  both present — and `rating` is pulled in transitively by
  `website_sale`. So `portal_rating` is always installed in the
  benchmark base snapshot (which includes `website_sale`); no on-demand
  install needed.

## How the UI submit becomes a `rating.rating` row

- Logged-in user clicks **Send** in the inline review composer on the
  product page.
- Frontend: the patched `@mail/core/common/composer` (see
  `addons/portal_rating/static/src/chatter/frontend/composer_patch.js`)
  reads `portalState.ratingValue` (default 4), attaches it as
  `post_data.rating_value`, and POSTs to `/mail/message/post`.
- Controller (`addons/mail/controllers/thread.py:200`) calls
  `thread._prepare_message_data(post_data, ...)` which filters
  `post_data` by `thread._get_allowed_message_params()`. The
  `rating.mail_thread` override (`addons/rating/models/mail_thread.py:194`)
  adds `rating_value` to the allowed params, so it survives into
  `message_post`.
- `rating.mail_thread.message_post` pops `rating_value` off kwargs, creates
  `rating.rating({rating: float(rating_value), res_model_id, res_id,
  consumed=True, partner_id=env.user.partner_id})`, then delegates to
  `super().message_post(rating_id=rating.id, ...)`. Finally
  `_message_post_after_hook` writes the bidirectional link:
  `rating.message_id = message.id` + `message.rating_id = rating.id`.

## Default star value is load-bearing for BU

- The composer opens with `DEFAULT_STAR_RATING = 4` (see `composer_patch.js:9`).
  Because the task requires exactly 4 stars, BU can succeed without
  clicking any star icon — just type the body + hit Send.
- To harden: pick a non-default rating (1, 2, 3, or 5) so the agent must
  actually interact with the `.o-mail-Composer-stars i` icons.

## Oracle short-circuit

- `rating.rating` is created server-side inside `message_post`; there is
  no REST endpoint specifically for ratings. The cleanest oracle is a
  JSON-RPC `call_kw` on `product.template.message_post` with
  `rating_value=4` + `body='<p>Great product</p>'` +
  `subtype_xmlid='mail.mt_comment'` + `message_type='comment'`.
- This produces the identical 5-edit diff as the browser path because
  the browser path also flows through `message_post`. No UI interaction
  needed.

## Expected state entity_key is `(res_model, res_name, partner_id)`

- `res_id` is an unstable `Many2oneReference` int that cannot be
  resolved at diff time — keep it in `ignore_fields`.
- `res_name` is a stored compute that resolves to the product's display
  name ("Bench Review Item"), which IS stable — use it in `match_key`.
- `res_model` is a stored related to `res_model_id.model`, resolves to
  `"product.template"` — also stable.
- `partner_id` normalizes to the display name — `"Mitchell Admin"` for
  admin login.
- Result: entity_key = `("product.template", "Bench Review Item", "Mitchell Admin")`.

## Ignored-field noise on rating.rating

- `access_token` (uuid generated per row, always unique).
- `parent_res_*` (False for product.template rating without parent).
- `rating_image` / `rating_image_url` / `rating_text` (compute).
- `resource_ref` / `parent_ref` (compute).
- `rated_on` (Datetime, XML-RPC-fragile).
- `publisher_*` fields from `portal_rating` (all None for a first review).
- `is_internal` / `feedback` / `message_id` (derivative, capture via check.py instead).

## check.py gates

- Exactly 1 rating.rating row on the product.
- `rating=4.0` with `consumed=True` and `message_id` set.
- Linked mail.message has body containing `"Great product"`,
  `message_type='comment'`, `subtype_id=mail.mt_comment`,
  `model='product.template'`, `res_id=product.id`.
- Product still published + active + price unchanged.

## Cleanup ordering

- Unlink rating.rating rows (res_model+res_id) BEFORE unlinking
  product.template; otherwise FK cascade is fine but the rating row may
  linger with a dangling `res_name` compute.
- Unlink mail.message rows (model+res_id) BEFORE product.template for
  the same reason.
