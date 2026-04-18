# Cookbook notes — project_todo.create_three_personal_with_specific_priorities

## Priority widget (`web.PriorityField`) — star indexing

`project.task.priority` is a Selection `[('0','Low priority'), ('1','Medium priority'), ('2','High priority')]`.

The `priority` (and `priority_switch`) widget renders **N-1 stars**, skipping the
first option (`value_first` is the default zero state):

- Star 1 (index 0 in `.o_priority_star`) → priority `'1'` (Medium / one filled star)
- Star 2 (index 1 in `.o_priority_star`) → priority `'2'` (High / both filled stars)

Default (no star filled) is priority `'0'` (Low).

### Implications for prompts

Saying just "set the priority to High by clicking the star" is ambiguous —
browser-use will often click the right-most star (index 1) because "High" reads
as the highest level, producing priority `'2'`. If your check expects priority
`'1'`, the prompt MUST say:

- "click only the FIRST star" / "exactly one star filled" / "Medium priority"

and explicitly forbid clicking the second star.

### Oracle pattern

Just write priority via JSON-RPC `create` / `write`; no need to simulate the
star clicks. The kanban / form views both accept `priority` as a regular
selection field.

## Browser-use failure mode observed

When asked to create three named to-dos and only set priority on one, the agent
went into a loop creating **7 duplicates of the first to-do** (`Plan Sprint`),
each with priority `'1'`, instead of moving on to the next to-do. Plausibly
the agent re-clicks "New" believing the save didn't take. Note for easy-tier
"create N records" tasks: even simple multi-create flows can fail this way.
