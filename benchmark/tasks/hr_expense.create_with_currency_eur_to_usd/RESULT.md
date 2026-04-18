ROW: 316
TASK_ID: hr_expense.create_with_currency_eur_to_usd
DIFFICULTY: medium
SUMMARY: Create EUR-currency hotel expense (€185); company is USD; multi-currency dropdown + computed conversion to ~$200.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## hr_expense.create_with_currency_eur_to_usd

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Expenses |
| **Workflow** | Open Expenses, click New, fill description NYC Hotel, category Hotel, total 185.00 with the currency dropdown switched from USD to EUR, date 04/01/2026, Paid By Employee, then save in draft. The form auto-computes the company-currency total (~$200 USD via the seeded 0.925 rate). |
| **Capability tested** | Selecting a non-default value in a multi-currency many2one dropdown that is gated behind base.group_multi_currency, verifying the computed converted total. |
| **Notes** | Odoo 19 has removed hr.expense.sheet, so the original "expense report" wrapper is dropped — the test is on the expense itself. The Currency field on the form requires base.group_multi_currency (granted in seed). EUR is inactive by default and was activated in seed; res.currency.rate seeded with rate=0.925 dated 2026-01-01 so 185 EUR → 200.00 USD deterministically. Browser-use ran the full flow but created the expense twice (2 instead of 1), failing the duplicate-count postcondition; F1=0 because the duplicate adds 6 extra edits. |
