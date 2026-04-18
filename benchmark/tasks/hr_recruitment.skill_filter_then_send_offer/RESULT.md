ROW: 335
TASK_ID: hr_recruitment.skill_filter_then_send_offer
DIFFICULTY: hard
SUMMARY: Filter the Applications list by Skill=Python, identify Alice Senior among 4 Python-skilled candidates (the only QA Lead applicant tagged Senior), select her row checkbox, cog Actions > Send Email, fill subject "Job Offer - QA Lead" and body containing 2026-06-01, send.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## hr_recruitment.skill_filter_then_send_offer

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment (hr_recruitment), Skills (hr_recruitment_skills), Mail |
| **Workflow** | Seed installs `hr_skills` + `hr_recruitment_skills` on demand and creates 5 applicants: Alice Senior (QA Lead + Senior tag + Python Expert, CORRECT), Bob Junior (QA Lead + Junior), Dana Pirate (Senior Backend Developer + Senior), Eve Contractor (QA Lead + Contractor), Charlie Jones (QA Lead, JavaScript — no Python). Task: open `/odoo/recruitment-applications` in list view, search-facet on **Skills: Python** (autocomplete), check Alice's row, open cog **Actions → Send Email**, fill subject "Job Offer - QA Lead" and body containing "2026-06-01", click Send. |
| **Capability tested** | Custom m2m search-filter selection from autocomplete ("Skills" facet, not Applicant/Tag/Job), cross-condition disambiguation among 4 filter matches (need both Senior tag AND QA Lead job), cog Actions bulk-binding Send Email wizard (binding_view_types='list,kanban' — NOT on form), applicant.send.mail wizard with required subject + body overrides. |
| **Notes** | Calibration FAILED (too easy): BU passed on first run in ~98s with F1=1.0, picking Alice correctly and filling subject+body. The two designed traps (Skills-facet and pick-senior-not-junior) did not resist Claude-Opus-driven BU, which read the prompt's explicit three-condition description and derived Alice. To re-harden, either (a) remove the explicit "Senior tag + QA Lead + Python" breakdown from the prompt and force inference from chatter/priority signals, or (b) add a wizard-modal policy trap such as toggling an uncommon `attachment_ids` upload. Oracle took ~25s and 37 API calls; includes `applicant.send.mail.action_send` which appears in trace_spec.required_ops. Module installs: `hr_skills` and `hr_recruitment_skills` are both `auto_install: True` and already present in the base snapshot built from per-task DBs, so `_ensure_module` is a no-op in practice but defends against minimal snapshots. |
