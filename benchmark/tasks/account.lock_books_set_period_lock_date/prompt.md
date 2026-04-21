# Lock the Books: Set the Global Lock Date

You must set the company's **Global Lock Date** (a.k.a. Non-Advisors Lock Date / Fiscal-Year Lock Date — the field stored as `fiscalyear_lock_date` on `res.company`) to **March 31, 2026**.

This prevents users without accountant rights from posting or modifying any journal entry dated on or before that date.

## Steps

1. Open the **Accounting** app (top menu: `Accounting`), then go to the **Configuration → Settings** page (or use the top-bar `Settings` app and click the **Accounting** tab).
2. Scroll to the **Fiscal Periods** section.
3. Find the **Global Lock Date** (a.k.a. Non-Advisors Lock Date / Fiscal Year Lock Date) field for the current company (`My Company` / the only company in the database).
4. Set it to **03/31/2026** (March 31, 2026).
5. Click **Save** at the top of the Settings page so the change is persisted on `res.company`.

## Rules

- Set **only** the Global / Non-Advisors Lock Date (`fiscalyear_lock_date`). Do **not** change `tax_lock_date`, `sale_lock_date`, `purchase_lock_date`, or `hard_lock_date`.
- The date must be exactly **2026-03-31** (March 31, 2026).
- Apply the change to the main company only; do not create a new company.
- After saving, the value must persist on the company record (`res.company.fiscalyear_lock_date == 2026-03-31`).
