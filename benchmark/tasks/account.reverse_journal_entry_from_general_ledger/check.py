"""Postcondition checks for account.reverse_journal_entry_from_general_ledger."""


def check(env):
    failures = []

    source = env["account.move"].search([("ref", "=", "BENCH-GL-REV")], limit=1)
    if not source:
        return ["Source entry BENCH-GL-REV not found"]

    if source.move_type != "entry":
        failures.append(
            f"BENCH-GL-REV move_type is {source.move_type!r}, expected 'entry'"
        )
    if source.state != "posted":
        failures.append(
            f"BENCH-GL-REV state is {source.state!r}, expected 'posted' "
            f"(source entry must remain posted — do NOT reset to draft or cancel it)"
        )

    # Source entry untouched: two balanced lines, Rent debit 100, Bank credit 100.
    src_lines = source.line_ids.filtered(
        lambda l: l.display_type not in ("line_section", "line_subsection", "line_note")
    )
    if len(src_lines) != 2:
        failures.append(
            f"Source entry has {len(src_lines)} non-section lines, expected 2"
        )
    src_total_debit = sum(l.debit for l in src_lines)
    src_total_credit = sum(l.credit for l in src_lines)
    if abs(src_total_debit - 100.0) > 0.01:
        failures.append(
            f"Source entry total debit is {src_total_debit}, expected 100.00"
        )
    if abs(src_total_credit - 100.0) > 0.01:
        failures.append(
            f"Source entry total credit is {src_total_credit}, expected 100.00"
        )

    reversals = env["account.move"].search([
        ("reversed_entry_id", "=", source.id),
    ])
    if not reversals:
        failures.append(
            "No account.move with reversed_entry_id=BENCH-GL-REV.id found "
            "(reversal entry was not created)"
        )
        return failures
    if len(reversals) != 1:
        failures.append(
            f"Expected exactly 1 reversal entry linked to BENCH-GL-REV, "
            f"found {len(reversals)}"
        )

    rev = reversals[0]
    if rev.move_type != "entry":
        failures.append(
            f"Reversal move_type is {rev.move_type!r}, expected 'entry'"
        )
    if rev.state != "posted":
        failures.append(
            f"Reversal state is {rev.state!r}, expected 'posted' "
            f"(the reversal wizard auto-posts the new entry)"
        )
    # Journal should match the source journal (Misc).
    if rev.journal_id.id != source.journal_id.id:
        failures.append(
            f"Reversal journal is {rev.journal_id.name!r}, expected "
            f"{source.journal_id.name!r} (leave Journal at its default)"
        )

    # Reversal lines: two lines with debit/credit swapped.
    rev_lines = rev.line_ids.filtered(
        lambda l: l.display_type not in ("line_section", "line_subsection", "line_note")
    )
    if len(rev_lines) != 2:
        failures.append(
            f"Reversal entry has {len(rev_lines)} non-section lines, expected 2"
        )
    total_debit = sum(l.debit for l in rev_lines)
    total_credit = sum(l.credit for l in rev_lines)
    if abs(total_debit - 100.0) > 0.01:
        failures.append(
            f"Reversal total debit is {total_debit}, expected 100.00"
        )
    if abs(total_credit - 100.0) > 0.01:
        failures.append(
            f"Reversal total credit is {total_credit}, expected 100.00"
        )

    # The reversal must swap debit/credit per account relative to the source.
    def line_map(lines):
        return {
            (l.account_id.id, round(l.debit, 2), round(l.credit, 2))
            for l in lines
        }

    src_sig = {(l.account_id.id, round(l.debit, 2), round(l.credit, 2)) for l in src_lines}
    rev_sig = {(l.account_id.id, round(l.debit, 2), round(l.credit, 2)) for l in rev_lines}
    expected_rev_sig = {
        (acc_id, credit, debit) for (acc_id, debit, credit) in src_sig
    }
    if rev_sig != expected_rev_sig:
        failures.append(
            f"Reversal lines do not mirror source. Source lines "
            f"(account_id, debit, credit)={sorted(src_sig)}; reversal lines "
            f"{sorted(rev_sig)}; expected reversal "
            f"{sorted(expected_rev_sig)}"
        )

    return failures
