# Receive a subcontracted serial-tracked product

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

The vendor **Bench Subcontractor Inc** finished assembling 2 units of the
serial-tracked product **Bench Sub Assembly** for us under a
subcontracting Bill of Materials. A confirmed purchase order
`P-BENCH-SUB-001` for 2 units of **Bench Sub Assembly** is already in
the system and has auto-generated an incoming transfer (receipt) from
the subcontractor. The raw components (`Bench Sub Part-A` and
`Bench Sub Part-B`) are already located at the subcontractor's
subcontracting location (the vendor has them).

Each finished unit must be tagged with its own serial number. Your job
is to receive the 2 units through the receipt, enter the two serial
numbers, and validate — so the linked subcontract MO closes and
back-flushes the raw components.

## What to do

1. From the Inventory overview, go to **Receipts** (the Receipts kanban
   tile or Operations > Transfers filtered to Receipts).
2. Open the receipt whose **Source Document** is `P-BENCH-SUB-001` (it
   is in state **Ready**, vendor is `Bench Subcontractor Inc`, and the
   single line is `Bench Sub Assembly` with demand `2`).
3. On the `Bench Sub Assembly` move line, click the **Details** button
   (the list-icon `⋮`/`≡` button at the end of the row) to open the
   **Detailed Operations** popup — a modal with a list of
   `stock.move.line` rows.
4. Make sure the popup ends up with **exactly two rows**, one per
   serial. If the popup starts with fewer than two rows, use the
   **Add a line** button in the popup's list.
5. Enter the serial numbers, one per row, each with **Quantity = 1**:
   - Row 1: Lot/Serial Number = `BSA-2026-01`, Quantity = `1`
   - Row 2: Lot/Serial Number = `BSA-2026-02`, Quantity = `1`

   When the autocomplete suggests `Create "BSA-2026-01"` /
   `Create "BSA-2026-02"`, pick the **Create** option so the serial is
   created on the fly.
6. Save / close the popup.
7. Back on the receipt form header, click **Validate**.
8. The receipt state should become **Done**. As a side effect, the
   auto-generated subcontracting manufacturing order becomes **Done**
   and the 4 components (2 of Part-A + 2 of Part-B) are consumed at
   the subcontractor's location.

## Rules

- The receipt **must end in state Done**. Do not cancel it, do not
  create a backorder.
- You MUST enter **two distinct serial numbers** `BSA-2026-01` and
  `BSA-2026-02` exactly (no extra whitespace, no alternate spelling).
- Each serial row MUST carry Quantity **1.0** (not 2.0 on a single
  row).
- Do NOT change the demand quantity on the line (leave it at `2`).
- Do NOT open the Manufacturing app and try to close the subcontract MO
  manually — the MO closes automatically when the receipt is validated.
- Do NOT add or remove Bench Sub Assembly lines on the receipt — only
  edit the move-line rows inside the Detailed Operations popup.
- Do NOT modify the Bill of Materials or the subcontractor partner.
- Leave the origin `P-BENCH-SUB-001` as the Source Document.
