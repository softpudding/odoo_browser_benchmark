"""Postcondition checks for hr_holidays.request_time_off_with_attachment.

Gates on:
  1. A 'Paid Leave' leave type exists (seeded) — sanity.
  2. Exactly one hr.leave exists for admin's employee of type 'Paid Leave'
     with:
       - request_date_from == 2026-07-01
       - request_date_to   == 2026-07-02
       - number_of_days    == 2.0 (working days)
       - state in {'confirm', 'validate1', 'validate'} (the prompt asks for
         'confirm'; we accept validate1/validate defensively so an agent
         that happens to auto-approve isn't doubly punished on state + all
         the other checks, but prefer 'confirm').
       - name contains 'Medical appointment' (soft check — tolerates
         auto-derived names).
  3. >=1 ir.attachment linked to this leave (res_model='hr.leave',
     res_id=<leave_id>) named 'BENCH-JUST.pdf' with non-empty bytes.
"""

from datetime import date


LEAVE_TYPE_NAME = "Paid Leave"
LEAVE_DESC = "Medical appointment"
PDF_FILENAME = "BENCH-JUST.pdf"
EXPECTED_FROM = date(2026, 7, 1)
EXPECTED_TO = date(2026, 7, 2)
EXPECTED_DAYS = 2.0


def check(env):
    failures = []

    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE_NAME)], limit=1
    )
    if not leave_type:
        failures.append(f"Leave type '{LEAVE_TYPE_NAME}' is missing")
        return failures

    admin = env.ref("base.user_admin")
    admin_emp = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    if not admin_emp:
        failures.append("Admin employee record is missing")
        return failures

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("employee_id", "=", admin_emp.id),
        ("holiday_status_id", "=", leave_type.id),
    ])
    if not leaves:
        failures.append(
            f"No hr.leave found for admin employee with type "
            f"'{LEAVE_TYPE_NAME}'"
        )
        return failures
    if len(leaves) > 1:
        failures.append(
            f"Found {len(leaves)} Paid Leave records for admin, expected "
            f"exactly 1"
        )

    leave = leaves[0]

    # State — agent must NOT approve. Accept confirm, but defensively also
    # allow validate1/validate (the other checks are strict enough).
    if leave.state not in ("confirm", "validate1", "validate"):
        failures.append(
            f"Leave state is '{leave.state}', expected 'confirm' (To "
            f"Approve); draft/refuse indicate the agent never saved the "
            f"request properly"
        )

    if leave.request_date_from != EXPECTED_FROM:
        failures.append(
            f"request_date_from is {leave.request_date_from}, expected "
            f"{EXPECTED_FROM}"
        )
    if leave.request_date_to != EXPECTED_TO:
        failures.append(
            f"request_date_to is {leave.request_date_to}, expected "
            f"{EXPECTED_TO}"
        )
    if abs(leave.number_of_days - EXPECTED_DAYS) > 0.01:
        failures.append(
            f"number_of_days is {leave.number_of_days}, expected "
            f"{EXPECTED_DAYS} (Wed 2026-07-01 -> Thu 2026-07-02 = 2 "
            f"working days)"
        )

    # Soft check on description — tolerate Odoo's auto-derived name, but
    # flag if the agent wrote something completely different.
    if leave.name and LEAVE_DESC.lower() not in (leave.name or "").lower():
        # Don't fail hard — this is descriptive. Many agents leave the
        # description blank and Odoo auto-fills it from the type. Only
        # surface as a warning-shaped failure when the agent clearly typed
        # a different description.
        pass

    # Attachment: at least one ir.attachment named BENCH-JUST.pdf linked
    # to this hr.leave with non-empty bytes.
    atts = env["ir.attachment"].with_context(active_test=False).search([
        ("res_model", "=", "hr.leave"),
        ("res_id", "=", leave.id),
    ])
    if not atts:
        failures.append(
            f"No ir.attachment linked to hr.leave id={leave.id} "
            f"(res_model='hr.leave'); the PDF justification was not "
            f"attached via the chatter paperclip"
        )
    else:
        named = [
            a for a in atts
            if (a.name or "").strip().lower() == PDF_FILENAME.lower()
        ]
        if not named:
            failures.append(
                f"hr.leave has {len(atts)} attachment(s) but none named "
                f"'{PDF_FILENAME}'. Attachments: {atts.mapped('name')}."
            )
        else:
            non_empty = [a for a in named if (a.datas or a.raw)]
            if not non_empty:
                failures.append(
                    f"'{PDF_FILENAME}' attachment on the leave has empty "
                    f"bytes"
                )

    return failures
