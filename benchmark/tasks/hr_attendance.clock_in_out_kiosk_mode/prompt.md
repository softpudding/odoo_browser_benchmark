Open the **Attendances** app.

You must perform a full clock-in AND clock-out cycle for employee **`Bench Worker`** using the tablet-style **Kiosk Mode** (PIN `1234`).

## Steps

1. From the Attendances app, open **Kiosk Mode** (left sidebar menu item). A public tablet-style kiosk page will load.
2. In the kiosk, you will see a grid of employee cards. Click the card for **`Bench Worker`**.
3. A PIN pad opens. Type **`1234`** on the numpad and press **OK**. The greeting screen will confirm the **check in**.
4. Wait for the greeting to return to the employee grid (or click **OK** on the greeting card to return immediately).
5. Click the **`Bench Worker`** card again.
6. Type **`1234`** on the numpad and press **OK**. The greeting screen will confirm the **check out**.

## Rules

- Only use the kiosk UI (PIN `1234`). Do not edit the `hr.attendance` record directly via the backend list view.
- Do not modify or create attendance records for any other employee.
- Both the check-in and the check-out must happen on the same day (today).
- Do not change the employee's PIN or barcode.
