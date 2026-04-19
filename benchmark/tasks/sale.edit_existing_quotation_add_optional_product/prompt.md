Go to the **Sales** app and open **Quotations**.

Find the draft quotation with name / customer reference **BENCH-ADD-LINE** for
customer **Bench Add Co** and open it.

The quotation already has **one** order line on the **Order Lines** tab:

| Line | Product | Qty | Unit Price |
|---|---|---|---|
| 1 | Bench Existing Item | 2 | 30.00 |

You must **add a second product line** for `Bench Extra Item` with quantity
`4`. The existing first line must be left untouched.

Steps:

1. On the opened quotation, stay on the **Order Lines** tab (it is the
   default tab).
2. In the list footer, click **Add a product** (the default, leftmost
   link next to "Add a section" / "Add a note"). A new empty editable
   row appears under the existing `Bench Existing Item` row.
3. In the new row's **Product** cell, type `Bench Extra Item` and pick
   it from the autocomplete dropdown.
4. In the same new row's **Quantity** cell, change the default (`1.00`)
   to exactly:
   ```
   4
   ```
   Press **Tab** (or click elsewhere) to commit the qty value.
5. Click **Save** (the cloud / save icon in the breadcrumb area, or the
   form's Save button). Do **NOT** click **Confirm** — the quotation
   must remain in the Quotation (draft) state.

**Rules:**

- Do NOT modify the existing first line in any way — `Bench Existing Item`
  must still have qty=2 and price=30.00 afterwards.
- Do NOT add more than one new line. After saving, the Order Lines
  list must have exactly two product rows.
- Do NOT use **Add a section** or **Add a note** — the new row is a
  regular PRODUCT line (display_type unset).
- Do NOT override the unit price on the new line; it should remain
  `15.00` (the `list_price` of `Bench Extra Item`, no pricelist is
  applied).
- Do NOT click **Confirm** — leave the quotation in the draft /
  Quotation state.
