Go to the **Sales** app and open **Quotations**.

Find the draft quotation **SO-BENCH-STRUCT** for customer **Bench Struct Co**
and open it. It already has two product lines (`Bench Struct Item A` qty=1,
`Bench Struct Item B` qty=2). Leave those lines as they are.

You will add **two new non-product lines** at the bottom of the **Order Lines**
tab:

1. In the Order Lines tab, look at the footer of the lines list. Next to
   the usual **Add a product** link you will see **Add a section** and
   **Add a note** links (they share the same footer row; you may have to
   look carefully because "Add a product" is the default/left-most
   option).
2. Click **Add a section**. A new line opens with a single wide input for
   the section name. Type exactly:
   ```
   Phase 1
   ```
   Press Tab (or click elsewhere) to commit the value.
3. Click **Add a note**. A new line opens with a single wide input for
   the note text. Type exactly:
   ```
   Delivery by end of month
   ```
   Press Tab (or click elsewhere) to commit.
4. **Save** the quotation (cloud/save icon in the breadcrumb area, or
   the form's Save button). Do NOT click Confirm.

**Rules:**

- Do NOT use **Add a product** for these — the section and note lines must
  use the dedicated **Add a section** / **Add a note** buttons so that
  their `display_type` is set to `line_section` / `line_note`. A regular
  product line with the name "Phase 1" is NOT the same thing.
- Do NOT delete or edit the existing two product lines. They must remain
  with their original products and quantities.
- Do NOT click **Confirm** — the quotation must stay in the Quotation
  (draft) state.
- The section line must come before the note line is fine; the exact
  ordering between them vs the two product lines is not checked, only
  that the two new rows exist alongside the two product rows.
