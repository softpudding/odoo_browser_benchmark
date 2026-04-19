"""Postcondition checks for account.import_opening_balance_set_initial_equity.

Validates:
1. Exactly one account.move with move_type='entry', ref='OPEN-BAL-001',
   state='posted', date=2026-01-01.
2. Entry has exactly two journal lines (ignoring section/note).
3. Total debit = 10000, total credit = 10000, balanced (amount_total_signed=0).
4. One line debits an asset-like `Stock Valuation` (code 140000) account for
   10000.
5. Other line credits an equity-type `Opening Balance` account for 10000.
"""

from datetime import date


REF = "OPEN-BAL-001"


def check(env):
    failures = []

    moves = env["account.move"].search([
        ("move_type", "=", "entry"),
        ("ref", "=", REF),
    ])
    if len(moves) != 1:
        return [f"Expected exactly 1 journal entry with ref '{REF}', found {len(moves)}"]

    mv = moves[0]

    if mv.state != "posted":
        failures.append(f"Entry state is '{mv.state}', expected 'posted'")

    expected_date = date(2026, 1, 1)
    if mv.date != expected_date:
        failures.append(f"Entry date is '{mv.date}', expected '{expected_date}'")

    if (mv.journal_id.type or "") != "general":
        failures.append(
            f"Entry journal type is '{mv.journal_id.type}' (journal="
            f"'{mv.journal_id.name}'), expected a 'general' journal"
        )

    lines = mv.line_ids.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
    )
    if len(lines) != 2:
        failures.append(f"Expected exactly 2 journal lines, found {len(lines)}")

    total_debit = sum(line.debit for line in lines)
    total_credit = sum(line.credit for line in lines)
    if abs(total_debit - 10000.0) > 0.01:
        failures.append(f"Total debit is {total_debit}, expected 10000.00")
    if abs(total_credit - 10000.0) > 0.01:
        failures.append(f"Total credit is {total_credit}, expected 10000.00")
    if abs(total_debit - total_credit) > 0.01:
        failures.append(
            f"Entry unbalanced: debit={total_debit}, credit={total_credit}"
        )

    # Overall balanced invariant on the move. For move_type='entry',
    # `amount_total_signed` on Odoo 19 reflects the total on one side
    # (=10000 here) rather than net 0 — balance is enforced via the
    # debit==credit invariant checked above.

    def _seen_diag():
        return ", ".join(
            f"{l.account_id.name}({l.account_id.code}/{l.account_id.account_type})"
            f" d={l.debit} c={l.credit}"
            for l in lines
        )

    # Debit 10000 on Stock Valuation (140000) / asset_current account
    asset_types = {"asset_current", "asset_fixed", "asset_non_current", "asset_cash"}
    stock_ok = any(
        (
            line.account_id.code == "140000"
            or (line.account_id.name or "").lower() == "stock valuation"
            or (
                line.account_id.account_type in asset_types
                and "stock" in (line.account_id.name or "").lower()
            )
        )
        and abs(line.debit - 10000.0) < 0.01
        and abs(line.credit) < 0.01
        for line in lines
    )
    if not stock_ok:
        failures.append(
            f"No debit line of 10000.00 on a Stock Valuation/asset account found. "
            f"Seen lines: {_seen_diag()}"
        )

    # Credit 10000 on Opening Balance / equity account
    equity_ok = any(
        (
            line.account_id.account_type == "equity"
            or "opening" in (line.account_id.name or "").lower()
        )
        and abs(line.credit - 10000.0) < 0.01
        and abs(line.debit) < 0.01
        for line in lines
    )
    if not equity_ok:
        failures.append(
            f"No credit line of 10000.00 on an Opening Balance/equity account found. "
            f"Seen lines: {_seen_diag()}"
        )

    return failures
