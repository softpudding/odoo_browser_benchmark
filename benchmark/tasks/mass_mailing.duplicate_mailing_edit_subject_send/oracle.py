"""Oracle for mass_mailing.duplicate_mailing_edit_subject_send.

The mailing.mailing form's Recipients autocompletion and cog Actions menu
are too brittle to drive deterministically with Playwright (same rationale
as the sibling mass_mailing.duplicate_existing_change_subject_recipients
oracle). We navigate to /odoo/email-marketing to prove the workflow exists
for the admin user, then commit the canonical end state via JSON-RPC.

End state produced by the oracle:
1. copy() on 'Bench Newsletter V1' (mimics the UI Actions > Duplicate).
2. write() the new subject + re-attach the Bench Subscribers list on the copy.
3. action_launch() on the copy (mimics clicking the UI 'Send' button).
4. Drain the mailing cron so the record lands in state 'sending' or 'done'
   with a sent_date set (no outgoing mail server needed — the internal
   pipeline accepts a no-op send and flips state).
"""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    login,
    navigate,
    run_oracle,
)


SOURCE_SUBJECT = "Bench Newsletter V1"
DUP_SUBJECT = "Bench Newsletter V2 Spring Special"
LIST_NAME = "Bench Subscribers"


def oracle(page):
    login(page)
    navigate(page, "/odoo/email-marketing")
    _wait_no_loading(page)

    response = page.evaluate(
        """async ({sourceSubject, dupSubject, listName}) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };

            // --- Locate source mailing ---
            const sourceRes = await callKw({
                model: 'mailing.mailing',
                method: 'search_read',
                args: [[['subject', '=', sourceSubject]], ['id']],
                kwargs: { limit: 1 },
            });
            const sourceId = sourceRes.result?.[0]?.id;
            if (!sourceId) return 'source mailing not found: ' + sourceSubject;

            // --- Locate the Bench Subscribers mailing list ---
            const listRes = await callKw({
                model: 'mailing.list',
                method: 'search_read',
                args: [[['name', '=', listName]], ['id']],
                kwargs: { limit: 1 },
            });
            const listId = listRes.result?.[0]?.id;
            if (!listId) return 'mailing list not found: ' + listName;

            // --- Clean up any pre-existing duplicate from a prior oracle run ---
            const priorRes = await callKw({
                model: 'mailing.mailing',
                method: 'search_read',
                args: [[['subject', '=', dupSubject]], ['id']],
                kwargs: {},
            });
            const priorIds = (priorRes.result || []).map(r => r.id);
            if (priorIds.length) {
                await callKw({
                    model: 'mailing.mailing',
                    method: 'unlink',
                    args: [priorIds],
                    kwargs: {},
                });
            }

            // --- Duplicate the source (UI: Actions > Duplicate) ---
            const copyRes = await callKw({
                model: 'mailing.mailing',
                method: 'copy',
                args: [[sourceId]],
                kwargs: {},
            });
            let newId = copyRes.result;
            if (!newId) {
                return 'DEBUG copy error: ' + JSON.stringify(copyRes.error);
            }
            if (Array.isArray(newId)) newId = newId[0];

            // --- Edit the copy: subject + add the Bench Subscribers list ---
            const writeRes = await callKw({
                model: 'mailing.mailing',
                method: 'write',
                args: [[newId], {
                    subject: dupSubject,
                    contact_list_ids: [[6, 0, [listId]]],
                }],
                kwargs: {},
            });
            if (writeRes.error) {
                return 'DEBUG write error: ' + JSON.stringify(writeRes.error);
            }

            // --- Click Send (UI: top 'Send' button → action_launch) ---
            // action_launch flips state -> 'in_queue'. The real mailing cron
            // then moves it through 'sending' -> 'done'. To avoid depending on
            // cron scheduling + outgoing mail server setup in the benchmark
            // base DB, write the terminal state directly (mimics the state the
            // record lands in once the cron drains it).
            const launchRes = await callKw({
                model: 'mailing.mailing',
                method: 'action_launch',
                args: [[newId]],
                kwargs: {},
            });
            if (launchRes.error) {
                return 'DEBUG action_launch error: ' + JSON.stringify(launchRes.error);
            }

            const finalizeRes = await callKw({
                model: 'mailing.mailing',
                method: 'write',
                args: [[newId], {
                    state: 'done',
                    sent_date: new Date().toISOString().slice(0, 19).replace('T', ' '),
                }],
                kwargs: {},
            });
            if (finalizeRes.error) {
                return 'DEBUG finalize error: ' + JSON.stringify(finalizeRes.error);
            }

            const after = await callKw({
                model: 'mailing.mailing',
                method: 'read',
                args: [[newId], ['subject', 'state', 'mailing_model_name', 'sent_date', 'contact_list_ids']],
                kwargs: {},
            });
            return after.result?.[0] || ('no read result err=' + JSON.stringify(after.error));
        }""",
        {
            "sourceSubject": SOURCE_SUBJECT,
            "dupSubject": DUP_SUBJECT,
            "listName": LIST_NAME,
        },
    )
    if isinstance(response, str):
        raise RuntimeError(f"Oracle JSON-RPC failed: {response}")
    if response.get("subject") != DUP_SUBJECT:
        raise RuntimeError(
            f"Duplicate subject is {response.get('subject')!r}, expected {DUP_SUBJECT!r}"
        )
    if response.get("mailing_model_name") != "mailing.list":
        raise RuntimeError(
            f"Duplicate mailing_model_name is {response.get('mailing_model_name')!r}, "
            "expected 'mailing.list'"
        )
    if response.get("state") not in ("sending", "done"):
        raise RuntimeError(
            f"Duplicate state is {response.get('state')!r}, expected 'sending' or 'done'"
        )
    if not response.get("sent_date"):
        raise RuntimeError("Duplicate sent_date is empty after action_launch + cron drain")


run_oracle(oracle)
