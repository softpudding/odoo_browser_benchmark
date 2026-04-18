ROW: 304
TASK_ID: project_todo.create_three_personal_with_specific_priorities
DIFFICULTY: easy
SUMMARY: Create 3 personal to-do notes; only Plan Sprint gets the first priority star (Medium = '1'), others stay default ('0').
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## project_todo.create_three_personal_with_specific_priorities

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (1 run, headless) — postcondition failure: 7 duplicate Plan Sprint records created |
| **F1** | 0.0 |
| **Odoo modules** | To-Do (project_todo) |
| **Workflow** | Open the To-do app, create three personal notes (Plan Sprint, Write Docs, Refactor CSS). Only Plan Sprint should get one priority star clicked (Medium = priority '1'); the other two stay at the default priority. Save each. |
| **Capability tested** | Multi-record creation in the to-do quick-create / form combined with the priority star widget interaction. |
| **Notes** | Priority widget renders only N-1 stars (skips value_first). For Selection [(0,Low),(1,Medium),(2,High)] this means 2 stars: star 1 → '1' (Medium), star 2 → '2' (High). Initial prompt that said "High - star" was ambiguous — BU clicked star 2 (priority='2') because "High" reads as the highest level. Tightened the prompt to say "click only the FIRST star (Medium)" and explicitly forbid the second star. After tightening, BU set the right priority value but failed via a different mode: it duplicated Plan Sprint 7 times instead of moving on to Write Docs / Refactor CSS. Oracle uses JSON-RPC create directly. See COOKBOOK_NOTES.md for the priority-widget star indexing quirk. |
