# Cookbook notes — website_hr_recruitment.edit_job_form_publish_preview

## hr.job backend Publish toggle

- Canonical selector for the Published boolean_toggle on the job form:
  `.o_field_boolean_toggle[name='website_published'] input` (Odoo 19,
  from `website_hr_recruitment/views/hr_recruitment_views.xml`). The
  widget onchange mirrors the toggle to `is_published`, so the diff
  engine reports BOTH `website_published` and `is_published` flipping
  to True in a single user action.
- The Details/Recruitment notebook tab is the default visible one;
  the Published toggle renders next to the "Target / new employees"
  row inside group `job_posting`.
- The `is_published` field in the button box is rendered with
  `widget="website_redirect_button"` — it navigates to the public
  `/jobs/<slug>` preview, it does NOT toggle the published state
  (consistent with the `event.event` / `event.track` pattern
  documented in ODOO19_PATTERNS.md).

## website_description is frontend-editor-only

- `website_description` is NOT exposed in the backend hr.job form view;
  it only appears as `<div t-field="job.website_description"/>` in the
  public `/jobs/detail/<slug>` template and is editable via the website
  WYSIWYG overlay (fragile iframe editor).
- Tasks that need `website_description` content to be asserted should
  **pre-seed** the desired HTML in `seed.py` and tell the agent NOT
  to touch that field. The agent then only touches the backend
  `description` (Summary tab) which is a regular in-page HTML editor.

## Diff engine on hr.job HTML fields

- `description` and `website_description` are `fields.Html(sanitize_overridable=True, sanitize_attributes=False, sanitize_form=False)`.
  Any whitespace/newline change shows as a diff row. Put both in
  `ignore_fields` in state_spec.yaml and validate via `html2plaintext`
  substring checks in `check.py`.
- `website_published` boolean_toggle's onchange flips `is_published` in
  the same user action — expect both fields to appear in the diff,
  even though the user clicked only one widget.
