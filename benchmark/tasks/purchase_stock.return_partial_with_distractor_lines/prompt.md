Open the **Purchase** app.

There is one received purchase order from vendor **Bayside Components Co.**:

- target: origin `P-BENCH-RET-001` — already confirmed and fully received

The receipt has 3 product lines:
- `Bayside WidgetA` (received qty: 10)
- `Bayside WidgetB` (received qty: 5)
- `Bayside WidgetC` (received qty: 8)

Only **2 units** of `Bayside WidgetB` need to be returned. The other two products
(WidgetA and WidgetC) must **NOT** be returned.

1. Open purchase order `P-BENCH-RET-001`.
2. Open its **Receipt** (the done transfer).
3. Click the **Return** button on the receipt.
4. In the return wizard, set the return quantities **exactly** as follows:
   - `Bayside WidgetA`: `0`
   - `Bayside WidgetB`: `2`
   - `Bayside WidgetC`: `0`
5. Click **Return** in the wizard to create the return picking.
6. On the new return transfer, click **Validate**.

**Rules:**
- Only `Bayside WidgetB` should appear on the validated return picking with quantity 2
- `Bayside WidgetA` and `Bayside WidgetC` must NOT be returned (set them to 0 in the wizard)
- Do not use **Return All**
- Do not cancel, delete, or edit the purchase order itself
- Do not modify the original receipt's done state
