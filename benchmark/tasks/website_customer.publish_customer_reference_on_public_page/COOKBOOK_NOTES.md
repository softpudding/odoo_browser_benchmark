# Cookbook notes — website_customer.publish_customer_reference_on_public_page

## /customers domain + module activation

- `website_customer` is NOT in the base snapshot. Seed must
  `button_immediate_install()` — it pulls in
  `website_crm_partner_assign` and `website_partner` as dependencies.
- Public `/customers` controller domain is
  `[('website_published', '=', True), ('assigned_partner_id', '!=', False)]`
  (see `website_customer/controllers/main.py`). The partner must
  (a) be published AND (b) have an "Implemented by" partner set.
  Seeds MUST populate `assigned_partner_id` or the partner will be
  invisible on /customers even after publishing.
- `/partners/<slug>` (from `website_partner.partners_detail`) renders
  for unpublished partners IFF the visiting user has
  `website.group_website_restricted_editor` (admin does). This is
  what makes the "preview while unpublished" flow possible: admin
  clicks Go to Website -> lands on /partners/<slug> -> flips the
  systray toggle.

## `res.partner.is_published` is `website_redirect_button` in the form

- `addons/website_partner/views/res_partner_views.xml` places the
  field in the `button_box` with `widget="website_redirect_button"`.
  The button's visible text is always "Go to Website" (from
  `addons/website/static/src/components/fields/redirect_field.xml`),
  with the aria-label / title reflecting the current state
  ("Unpublished" or "Published"). The globe icon is colored red
  when unpublished, green when published.
- Clicking invokes `open_website_url()` (defined on the
  `WebsitePublishedMixin`), which navigates to the record's
  `website_url`. It does NOT toggle is_published.
- The canonical backend publish path is the Owl
  `PublishSystrayItem` on the frontend preview, which RPCs
  `model.website_publish_button()` (same method the Job/Event
  forms would use).

## Selector that works under Playwright

Matching the button by visible text "Go to Website" is reliable;
matching by aria-label "Unpublished" / "Published" also works. The
best semantic selector is by widget class:

```python
page.locator(
    ".o_field_website_redirect_button button, "
    ".o_field_widget[name='is_published'] button"
).first
```

Confirmed working on `res.partner` and expected to work on any
model using the same widget.

## Seed ordering gotcha — assigned_partner_id cleanup

Re-run cleanup must null out `assigned_partner_id` on partners that
reference seeded records BEFORE unlinking them; otherwise FK
constraints from `website_crm_partner_assign` / other modules can
block the unlink. Pattern:

```python
referring = env["res.partner"].with_context(active_test=False).search([
    ("assigned_partner_id", "in", old_partners.ids),
])
if referring:
    referring.sudo().write({"assigned_partner_id": False})
old_partners.sudo().unlink()
```

## Calibration signal (BU single-shot pass)

Browser-use solved this task in 61.4s single-shot with F1=1.0. The
task exercises: click stat button to navigate frontend preview +
click Owl systray toggle + navigate URL `/customers`. No wizard and
no non-default widgets; BU handles all three steps cleanly. Medium
tier is correct and matches the sibling
`website_hr_recruitment.edit_job_form_publish_preview` (which also
uses a publish-and-preview-page round-trip and which BU also
passes).
