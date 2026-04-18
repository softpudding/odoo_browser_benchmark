# website_customer.publish_customer_reference_on_public_page — RESULT

- Difficulty: medium (tier 2)
- Time limit: 360s, step limit: 200

## Oracle

- Agent: `oracle`
- Result: **PASS**, StateDiffF1=1.0, RequiredOpRecall=1.0
- Wall clock: 23.8s
- Writes: 19 (0 forbidden)
- State diff: 2 edits observed / 2 expected.

## Browser-Use (single-shot)

- Agent: `browser-use`
- Result: **PASS**, StateDiffF1=1.0
- Wall clock: 61.4s
- Postcondition failures: 0
- HarmfulWriteRate=0, WritePrecision=1.0
- Run dir: `benchmark/reports/runs/website_customer.publish_customer_reference_on_public_page__browser-use__1776531590/`

BU successfully: navigated /odoo/contacts, opened 'Bench Happy Client',
clicked the button-box **Go to Website** redirect button (widget
`website_redirect_button`) to land on `/partners/<slug>`, clicked the
Owl **Unpublished** systray toggle to flip to **Published** (invokes
`res.partner.website_publish_button()`), then verified the partner
is listed at `/customers`. All three postcondition checks satisfied:
`website_published=True`, `is_published=True`, and the name appears
in /customers HTML.

## Notes

- Seed installs `website_customer` on demand via
  `button_immediate_install()` (not in base snapshot — pulls in
  `website_crm_partner_assign` and `website_partner`).
- /customers domain is
  `[('website_published', '=', True), ('assigned_partner_id', '!=', False)]`.
  Seed populates `assigned_partner_id` by creating a second company
  ("Bench Delivery Partner") and linking it as the implementer.
- `res.partner.is_published` on the backend form uses
  `widget="website_redirect_button"` (navigation-only; same pattern
  as `event.event` / `hr.job`). The canonical publish path is via
  the Owl systray on the frontend preview, which calls
  `website_publish_button()`.
- Check verifies:
  - exactly one `res.partner` named "Bench Happy Client"
  - `is_published=True` and `website_published=True` (related pair)
  - `assigned_partner_id` still points at "Bench Delivery Partner"
    (not blanked by the agent)
  - `country_id` preserved (seeded US)
  - partner name visible in /customers page HTML (best-effort HTTP
    fetch; gracefully skipped if HTTP unreachable from the check
    harness, since the domain attributes above guarantee rendering)

## Calibration

Medium tier is correct. BU passed single-shot in 61.4s with F1=1.0,
consistent with the sibling reference task
`website_hr_recruitment.edit_job_form_publish_preview` (which also
uses `website_published` boolean_toggle + backend-to-frontend
round-trip and which BU also passes). The task exercises the
cross-module navigation pattern (backend form -> frontend preview ->
systray toggle -> frontend listing) without wizards or non-default
choices, so it calibrates as medium rather than hard.
