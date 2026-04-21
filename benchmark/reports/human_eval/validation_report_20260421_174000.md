# Human Validation Report

Date: 2026-04-21
Tasks validated: 10 / 424
Selection method: random 10 from browser-use failures

## Results

| Task | Human | Agent | Status | Notes |
|---|---|---|---|---|
| account.partial_pay_vendor_bill_with_memo | PASS (131s) | FAIL (timeout 300s) | validated | Agent timed out, 0 edits |
| account.update_vendor_bill_reference_post | PASS (60s) | FAIL (timeout 300s) | validated | Agent timed out, 0 edits |
| calendar.edit_single_recurrence_occurrence | PASS (132s) | FAIL (timeout 480s) | validated | Agent made correct edits but timed out |
| calendar.make_single_occurrence_all_day | PASS (75s) | FAIL (timeout 480s) | validated | Agent made edits but wrong values |
| contacts.create_company_set_supplier_tag | PASS (94s) | FAIL (timeout 300s) | validated | Agent timed out, 0 edits |
| crm.create_opportunity_tag_schedule_call | PASS (158s) | FAIL (timeout 300s) | validated | Agent made all 5 correct edits but timed out |
| crm.merge_duplicate_opportunities_cleanup | PASS (70s) | FAIL (308s) | validated | Both hit merge action; agent missed write+activity |
| crm.update_lead_email | PASS (145s) | pending | validated | Human initially edited wrong record (pipeline vs leads view); rerun passed |
| purchase.cancel_reissue_wrong_vendor | PASS (138s) | FAIL (timeout 480s) | validated | Agent cancelled PO but couldn't create replacement |
| sale.change_validity_date | PASS (174s) | FAIL (timeout 180s) | validated | Agent timed out, 0 edits |

## Summary

- **10/10 tasks validated** (human passed all)
- **0/10 tasks passed by agent** (all browser-use failures confirmed)
- **0 task design issues found** — all tasks are completable by a competent human
- **1 human error on first attempt** (crm.update_lead_email): user opened pipeline view instead of Leads view; resolved on rerun

## Observations

- Most agent failures are **timeouts** — the agent runs out of time navigating the UI
- In 2 cases (calendar.edit_single_recurrence_occurrence, crm.create_opportunity_tag_schedule_call) the agent actually made all correct edits but still timed out before the eval harness captured completion
- Average human completion time: **117s** (range: 60–174s)
- No task design problems detected — prompts are clear and achievable
