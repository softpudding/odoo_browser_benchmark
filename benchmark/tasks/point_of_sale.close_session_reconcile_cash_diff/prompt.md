Go to the **Point of Sale** app and open the register **`Bench Close POS`**. A session is already in progress with one paid cash order of **€100.00**, so the expected cash in the drawer is **€100.00**.

1. Open the session's **Closing Control** from the POS kiosk (or from the backend **Sessions** list).
2. In the closing control, set the **counted cash** to **`97.00`** (the drawer is €3.00 short).
3. Confirm the closing and **close the session**, accepting the €3.00 difference.

The session must end in **Closed & Posted** state with the counted cash recorded as **97.00** (a difference of **-3.00** against the expected €100.00).

## Rules

- Do not create any new POS orders — only close the existing session
- Do not change the counted cash to anything other than `97.00`
- Do not cancel or refund the existing paid order
- The session must end in the `closed` state
