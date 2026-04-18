ROW: 318
TASK_ID: website.create_contact_form_with_custom_field
DIFFICULTY: hard
SUMMARY: Add a required Selection field ("Inquiry Type": Sales/Support/Partnership) to a seeded /contactus-bench form in the website builder.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## website.create_contact_form_with_custom_field

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website |
| **Workflow** | Seed creates a Contact Us page at /contactus-bench containing a standard s_website_form snippet (Your Name / Your Email / Phone / Your Question / Submit) but no Inquiry Type field. The agent must open the iframe-based website builder, drop a new Selection-type field labelled "Inquiry Type" into the form with three options (Sales, Support, Partnership), mark it required, and save. |
| **Capability tested** | Iframe-heavy drag-drop in the website builder plus per-field configuration (type selector, multi-option editing, required toggle). |
| **Notes** | Expected_state.json is empty on purpose — check.py validates arch_db content of ir.ui.view because the page record itself doesn't change; the only diff is inside the view arch. In Odoo 19 a custom Selection form field renders as radio inputs via s_website_form_multiple by default (not a bare <select>), so check.py accepts either rendering. Oracle bypasses the iframe via JSON-RPC write on ir.ui.view (the builder's canonical save path). Browser-Use timed out at 480s never hitting ir.ui.view.write. |
