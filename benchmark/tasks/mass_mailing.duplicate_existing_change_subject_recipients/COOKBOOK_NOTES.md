# Cookbook notes — mass_mailing.duplicate_existing_change_subject_recipients

## Browser-use failure mode: cog->Duplicate spam loop

When asked to "Duplicate via the Actions menu, then edit the copy", browser-use
on `mailing.mailing` form clicked the cog -> Duplicate item **repeatedly** (15
total mailings created, hitting the step limit). The likely cause: after the
first Duplicate, the form navigates to the new copy with subject still equal
to the source ("Q1 Bulletin Template"); BU's policy of "find original, click
Duplicate" reads the heading as still-not-yet-duplicated and tries again.

Implication for similar tasks: when the *only* visible signal that Duplicate
succeeded is a URL/id change (not a subject/title change), BU may loop. Tasks
that want to test "duplicate then edit" should phrase the prompt in a way
that makes the post-duplicate state visually distinguishable, or accept this
as the canonical FAIL mode.

check.py guards against this by asserting **exactly 2** mailings across the
{source-subject, dup-subject} set; the spam loop creates 14 extra copies of
the source and trips the count check.

## Oracle pattern: copy() + write() via JSON-RPC

The mailing.mailing domain widget (tree editor with field-path autocomplete)
and Recipients dropdown autocompletion are notoriously hard to drive from
Playwright. Reuse the JSON-RPC bypass already in
`mass_mailing.create_segmented_mailing_save_draft/oracle.py`: call
`mailing.mailing.copy([source_id])` to mimic the UI Duplicate, then `write()`
the new id with the target subject, `mailing_model_id=ir.model('res.partner')`,
`contact_list_ids=[(5,0,0)]`, and `mailing_domain="[('country_id.code','=','DE')]"`.

## check.py country-domain matching

Browser-use / humans may write the country filter in any of these textual
forms — accept all of them in check.py:
- `[('country_id', '=', <germany_id>)]`
- `[('country_id', '=', 'Germany')]`
- `[('country_id.name', '=', 'Germany')]`
- `[('country_id.code', '=', 'DE')]`

Resolve `res.country` by `code='DE'` once, then compare integer ids and
case-insensitive 'germany'/'de'/germany.name on string leaves.
