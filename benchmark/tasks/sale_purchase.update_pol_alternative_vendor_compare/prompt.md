Open the **Purchase** app.

There is a draft Request for Quotation with source document `R-BENCH-ALT-001`
sent to vendor **Atlas Industrial** for **10 × Industrial Compressor** at a
unit price of **120.00**.

You need to call for tender with two more vendors and pick the cheapest one.

1. Open the RFQ `R-BENCH-ALT-001`.
2. On the **Alternatives** tab click **Create Alternative**. In the dialog:
   - Vendor: **Beacon Mechanical**
   - Leave **Copy Products** checked
   - Click **Create Alternative**
3. The new RFQ for Beacon Mechanical opens. Set its line **Unit Price** to
   **100.00** for the Industrial Compressor (keep quantity = 10). Save.
4. Go back to the original RFQ `R-BENCH-ALT-001` (use the Alternatives tab
   on the new RFQ to navigate, or browse from the list). On the
   **Alternatives** tab click **Create Alternative** again. In the dialog:
   - Vendor: **Crestline Equipment**
   - Leave **Copy Products** checked
   - Click **Create Alternative**
5. On the Crestline Equipment RFQ that opens, set the Industrial Compressor
   **Unit Price** to **130.00** (keep quantity = 10). Save.
6. From any of the three linked RFQs, go to the **Alternatives** tab and
   click **Compare Product Lines**.
7. In the comparison list, find the Industrial Compressor row for vendor
   **Beacon Mechanical** (the 100.00 price line) and click its **Choose**
   button (the bullseye icon at the end of the row). This will clear the
   quantities on the Atlas Industrial and Crestline Equipment lines.
8. Open the Beacon Mechanical RFQ (you can click it from the Reference
   column in the comparison list, or open it from the Purchase list).
9. Click **Confirm Order**. A dialog titled "What about the alternative
   Requests for Quotations?" appears. Click **Cancel Alternatives** so the
   Atlas Industrial and Crestline Equipment RFQs are cancelled.

**Final state:**
- Beacon Mechanical RFQ is **confirmed** (Purchase Order) with 10 ×
  Industrial Compressor at unit price 100.00.
- Atlas Industrial RFQ is **cancelled**.
- Crestline Equipment RFQ is **cancelled**.

**Rules:**
- Do not change the product or quantity on any line — only the unit price on
  the alternatives.
- Do not delete any RFQ.
- Do not confirm the Atlas Industrial or Crestline Equipment RFQ.
- The "Cancel Alternatives" choice in the warning dialog is mandatory; do
  not pick "Keep Alternatives".
