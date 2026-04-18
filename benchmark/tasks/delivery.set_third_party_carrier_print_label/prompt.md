Go to the **Delivery Methods** configuration page (Inventory → Configuration → Shipping Methods).

Create a new delivery method with these exact values:

- **Delivery Method**: `Bench Express`
- **Provider**: `Fixed Price`
- **Delivery Product**: create (or use the create-and-edit shortcut for) a service product named `Bench Express Shipping`.
- **Fixed Price**: `12.00`

Save the delivery method.

Then go to the **Inventory** app and open the **outgoing delivery** picking whose Source Document is **`S-BENCH-DLV-002`** (it is in the **Ready** state with one move line of `Bench Express Crate` x 3 already reserved).

On the picking form:

1. In the **Additional Info** / Shipping Information section, set **Shipping Method** to `Bench Express`.
2. In the **Tracking Reference** field on the same section, enter exactly `BX-TRACK-002`.
3. Click **Validate** to mark the picking done. (If a quantity confirmation dialog appears, accept the default and proceed — the reserved quantities are already correct.)
4. Once the picking is in the **Done** state, click the **Print** button in the form header to trigger the delivery slip printout. (You don't need to download or save the PDF — clicking the button is enough.)

## Rules

- Do not change the customer or the move line product/quantity on the picking.
- Do not edit any other delivery method.
- Do not create more than one delivery method.
- Do not cancel the picking; it must end up in the **Done** state.
- The tracking reference text must be exactly `BX-TRACK-002` (case-sensitive, no extra spaces).
