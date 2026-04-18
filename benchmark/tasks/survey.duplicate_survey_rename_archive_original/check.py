"""Postcondition checks for survey.duplicate_survey_rename_archive_original."""


ORIGINAL_TITLE = "Quarterly Pulse Q1 Template"
COPY_TITLE = "Quarterly Pulse Q2 2026"


def check(env):
    failures = []
    Survey = env["survey.survey"].with_context(active_test=False)

    originals = Survey.search([("title", "=", ORIGINAL_TITLE)])
    copies = Survey.search([("title", "=", COPY_TITLE)])

    if len(originals) != 1:
        failures.append(
            f"Expected exactly 1 survey titled '{ORIGINAL_TITLE}', found "
            f"{len(originals)}"
        )
    else:
        original = originals[0]
        if original.active:
            failures.append(
                f"Original survey '{ORIGINAL_TITLE}' is still active — "
                f"agent did not archive it"
            )

    if len(copies) != 1:
        failures.append(
            f"Expected exactly 1 survey titled '{COPY_TITLE}', found {len(copies)}"
        )
    else:
        copy = copies[0]
        if not copy.active:
            failures.append(
                f"Renamed copy '{COPY_TITLE}' is archived — only the "
                f"original should be archived"
            )
        if originals and copy.id == originals[0].id:
            failures.append(
                "Original and copy resolve to the same record — duplicate did not happen"
            )
        # Copy should retain the original's question structure (cog Duplicate copies questions).
        if not copy.question_and_page_ids:
            failures.append(
                f"Renamed copy '{COPY_TITLE}' has no questions — likely created "
                f"from scratch instead of via Duplicate action"
            )

    # Make sure no leftover "(copy)" suffix survey exists.
    leftovers = Survey.search([("title", "=", f"{ORIGINAL_TITLE} (copy)")])
    if leftovers:
        failures.append(
            f"Found {len(leftovers)} survey(s) still titled "
            f"'{ORIGINAL_TITLE} (copy)' — agent did not finish renaming the copy"
        )

    return failures
