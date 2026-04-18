"""Postcondition checks for maintenance.fill_description_schedule_window_move_to_repaired."""


REQUEST_NAME = "Replace Conveyor Drive Belt"
EXPECTED_DESC_FRAGMENT = "Belt cracked at the splice"
EXPECTED_DURATION = 2.0


def check(env):
    failures = []

    requests = env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", REQUEST_NAME),
    ])
    if not requests:
        return [f"Maintenance request '{REQUEST_NAME}' not found"]
    if len(requests) != 1:
        return [
            f"Expected exactly 1 maintenance request '{REQUEST_NAME}', "
            f"found {len(requests)}"
        ]

    request = requests[0]

    if not request.stage_id or not request.stage_id.done:
        failures.append(
            f"Stage is '{request.stage_id.name if request.stage_id else None}' "
            f"(done={bool(request.stage_id and request.stage_id.done)}); "
            f"expected a 'done' stage like 'Repaired'"
        )
    elif request.stage_id.name != "Repaired":
        failures.append(
            f"Stage is '{request.stage_id.name}', expected 'Repaired'"
        )

    desc = request.description or ""
    if EXPECTED_DESC_FRAGMENT not in desc:
        failures.append(
            f"Description does not contain expected text "
            f"'{EXPECTED_DESC_FRAGMENT}'; got: {desc[:120]!r}"
        )

    if not request.schedule_date or not request.schedule_end:
        failures.append(
            "Either Scheduled Date or End Date is empty — agent did not log "
            "the schedule window"
        )
    else:
        if abs(request.duration - EXPECTED_DURATION) > 0.05:
            failures.append(
                f"Duration is {request.duration} hours, expected "
                f"~{EXPECTED_DURATION} hours (start to end)"
            )

    if request.archive:
        failures.append("Request was archived; expected to remain active")

    return failures
