# website_hr_recruitment.edit_job_form_publish_preview — RESULT

- Difficulty: medium (tier 2)
- Time limit: 360s, step limit: 200

## Oracle

- Agent: `oracle`
- Result: **PASS**, StateDiffF1=1.0, RequiredOpRecall=1.0
- Wall clock: 45.3s
- Writes: 24 (0 forbidden)
- State diff: 2 edits observed / 2 expected.

## Browser-Use (single-shot)

- Agent: `browser-use`
- Result: **PASS**, StateDiffF1=1.0
- Wall clock: 111.1s, steps=14
- Postcondition failures: 0
- HarmfulWriteRate=0, WritePrecision=1.0
- Run dir: `benchmark/reports/runs/website_hr_recruitment.edit_job_form_publish_preview__browser-use__1776528839/`

BU successfully: found and configured the Bench QA Engineer job,
opened the Summary tab, typed the exact description, toggled the
Published boolean, saved, and clicked "Job Page" (website_redirect_button)
to preview `/jobs/bench-qa-engineer-1`. The seeded Requirements section
(Python / Playwright / 2+ yrs) remained untouched, so `check.py`
passed on all four validations.

## Notes

- Check verifies:
  - exactly one `hr.job` named "Bench QA Engineer"
  - `is_published=True` and `website_published=True`
  - `description` HTML → plaintext contains the exact phrase
  - `website_description` plaintext still has seeded tokens
    (Requirements, Python, Playwright, 2+ yrs)
  - no applicants created, department/no_of_recruitment untouched
- `description` and `website_description` are in `state_spec.yaml`
  `ignore_fields` because the diff engine is noisy on HTML bodies;
  `check.py` is the source of truth.
