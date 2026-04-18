# Odoo 19 quirks discovered in hr_expense.create_with_currency_eur_to_usd

## hr.expense.sheet REMOVED in Odoo 19

The legacy `hr.expense.sheet` model (Expense Report wrapper that grouped
multiple `hr.expense` lines for submission and approval) is GONE in Odoo 19.
Tasks ported from older versions that say "create an expense report and attach
this expense to it" must be redesigned around the single `hr.expense` record:
submission/approval/posting now happens directly on the expense.

A vestige remains: `hr.expense.former_sheet_id` (Integer) preserves the legacy
sheet id for migrated data — do NOT use it as a real foreign key.

## hr.expense Currency dropdown is gated by base.group_multi_currency

The `currency_id` Many2one next to `total_amount_currency` on the expense form
has `groups="base.group_multi_currency"`. Without that group on the user, the
dropdown is invisible and the agent cannot pick a foreign currency — the
expense silently uses the company currency.

Seed pattern when the task tests multi-currency:
```python
admin.group_ids |= env.ref("base.group_multi_currency")
```

## Currencies start active=False in fresh DB

`res.currency` records like `base.EUR` and `base.USD` ship with
`active=False` in the data file. Only the company's own currency gets
auto-activated via `_check_company_currency_stays_active` constraint. If a
task needs another currency, seed must explicitly write `active=True` (use
`sudo()` since the field is restricted).

## res.currency.rate semantics

`res.currency.rate.rate` is "currency-per-company-currency". With
company=USD and `EUR.rate=0.925` it means 1 USD = 0.925 EUR; therefore an
expense entered as 185 EUR converts to `185 / 0.925 = 200.00 USD` via the
internal `inverse_rate` returned by `_get_conversion_rate(EUR, USD)`. Pick
clean ratios when you want stable check.py tolerances.

## hr.expense.search default scope hides admin's own expenses by employee filter

When the agent (admin) creates an expense via UI, it appears in
`/odoo/expenses` only under "My Expenses". Default `start_url=/odoo/expenses`
opens the admin's own list, which is fine for a single-expense task.
