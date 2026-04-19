Go to the **Sales** app and open **Quotations**.

Find the draft quotation with name / customer reference **BENCH-DISC** for
customer **Bench Disc Co** and open it.

The quotation already has two order lines on the **Order Lines** tab:

| Line | Product | Qty |
|---|---|---|
| 1 | Bench Product A | 2 |
| 2 | Bench Product B | 3 |

You must apply a **10% discount** to the **first order line only**
(`Bench Product A`).

Steps:

1. On the opened quotation, stay on the **Order Lines** tab (it is the
   default tab).
2. Locate the **Disc.%** column in the order-lines list (it is the
   per-line discount column, usually toward the right side of the
   row — it sits between "Taxes" and "Amount"). In Odoo 19, this
   column is visible because the per-line-discount setting has been
   enabled for the admin user.
3. Click into the **Disc.%** cell on the **first** line
   (the Bench Product A row). The cell turns into an editable input.
4. Type exactly:
   ```
   10.0
   ```
5. Press **Tab** (or click elsewhere) to commit the value.
6. Click **Save** (the cloud / save icon in the breadcrumb area, or
   the form's Save button). Do **NOT** click **Confirm** — the
   quotation must remain in the Quotation (draft) state.

**Rules:**

- Apply the 10% discount ONLY to the first line (Bench Product A).
  The second line (Bench Product B) must keep its discount at 0.
- Do NOT change any quantity, product, unit price, or any other field.
- Do NOT add new lines or delete any existing lines.
- Do NOT click **Confirm** — leave the quotation in the draft /
  Quotation state.
- The value to enter is the per-line **Disc.%** column (percentage
  discount on one order line), NOT any header-level discount or a
  new section/note line.
