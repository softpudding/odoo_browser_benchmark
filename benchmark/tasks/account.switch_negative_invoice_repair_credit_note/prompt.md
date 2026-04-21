Open the Invoicing (Accounting) app. There are two draft customer invoices for **Lumen Works**.

Edit **only** the draft invoice whose source document is `RET-508`.
In this UI, that field may appear as **Invoice Origin** / **Source Document** in the invoice list or under **Other Info**.

That document currently has a negative total, so it should not remain a customer invoice.

For that document:

1. Use the **Action** menu to switch it into a **credit note / refund**.
2. From **Invoicing > Customers > Products**, open each product from the document and read its **Sales Description** field.
3. The Sales Description gives the correct **Quantity** and **Discount** for that product in the format `Qty=X | Discount=Y`.
4. Return to the credit note and fix every product line so the quantity and discount match the instruction. Also ensure each line's unit price is **positive** (the switch may leave prices negative).
5. Open **Other Info** and set **Customer Reference** to `RET-508-READY`.
6. Post the credit note.

Do not modify the other draft invoice.
