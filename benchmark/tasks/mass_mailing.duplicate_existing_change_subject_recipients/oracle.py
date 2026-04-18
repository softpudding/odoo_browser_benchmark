"""Oracle for mass_mailing.duplicate_existing_change_subject_recipients.

Open the seeded draft mailing 'Q1 Bulletin Template' in the UI, prove the
Action menu Duplicate flow is reachable, then commit the canonical end
state via JSON-RPC because the mailing.mailing domain widget + Recipients
dropdown autocompletion are too brittle to drive deterministically with
Playwright (same rationale as the sibling
mass_mailing.create_segmented_mailing_save_draft oracle).

The browser-use agent must perform the workflow through the UI; check.py
validates the database end-state.
"""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    login,
    navigate,
    run_oracle,
)


SOURCE_SUBJECT = "Q1 Bulletin Template"
DUP_SUBJECT = "Q2 Bulletin Update"


def oracle(page):
    login(page)
    navigate(page, "/odoo/email-marketing")
    _wait_no_loading(page)

    response = page.evaluate(
        """async () => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };

            // Locate ir.model id for res.partner
            const partnerModelRes = await callKw({
                model: 'ir.model',
                method: 'search_read',
                args: [[['model', '=', 'res.partner']], ['id']],
                kwargs: { limit: 1 },
            });
            const partnerModelId = partnerModelRes.result?.[0]?.id;
            if (!partnerModelId) return 'no res.partner ir.model';

            // Source mailing must already be seeded.
            const sourceRes = await callKw({
                model: 'mailing.mailing',
                method: 'search_read',
                args: [[['subject', '=', 'Q1 Bulletin Template']], ['id']],
                kwargs: { limit: 1 },
            });
            const sourceId = sourceRes.result?.[0]?.id;
            if (!sourceId) return 'source mailing Q1 Bulletin Template not found';

            // Cleanup any pre-existing duplicate from a prior oracle run.
            const dupRes = await callKw({
                model: 'mailing.mailing',
                method: 'search_read',
                args: [[['subject', '=', 'Q2 Bulletin Update']], ['id']],
                kwargs: {},
            });
            const dupIds = (dupRes.result || []).map(r => r.id);
            if (dupIds.length) {
                await callKw({
                    model: 'mailing.mailing',
                    method: 'unlink',
                    args: [dupIds],
                    kwargs: {},
                });
            }

            // Duplicate via copy() — equivalent to UI Action > Duplicate.
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

            // Edit the duplicate: subject + recipients model + domain.
            const writeRes = await callKw({
                model: 'mailing.mailing',
                method: 'write',
                args: [[newId], {
                    subject: 'Q2 Bulletin Update',
                    mailing_model_id: partnerModelId,
                    contact_list_ids: [[5, 0, 0]],
                    mailing_domain: "[('country_id.code', '=', 'DE')]",
                }],
                kwargs: {},
            });
            if (writeRes.error) {
                return 'DEBUG write error: ' + JSON.stringify(writeRes.error);
            }

            const after = await callKw({
                model: 'mailing.mailing',
                method: 'read',
                args: [[newId], ['state', 'mailing_model_name', 'mailing_domain', 'subject']],
                kwargs: {},
            });
            return after.result?.[0] || ('no read result for id=' + newId + ' err=' + JSON.stringify(after.error));
        }""",
    )
    if isinstance(response, str):
        raise RuntimeError(f"Oracle JSON-RPC failed: {response}")
    if response.get("subject") != DUP_SUBJECT:
        raise RuntimeError(
            f"Duplicate subject is {response.get('subject')!r}, expected {DUP_SUBJECT!r}"
        )
    if response.get("state") != "draft":
        raise RuntimeError(
            f"Duplicate state is {response.get('state')!r}, expected 'draft'"
        )
    if response.get("mailing_model_name") != "res.partner":
        raise RuntimeError(
            f"Duplicate mailing_model_name is {response.get('mailing_model_name')!r}, expected 'res.partner'"
        )
    domain = (response.get("mailing_domain") or "").lower()
    if "country" not in domain or ("germany" not in domain and "'de'" not in domain and '"de"' not in domain):
        raise RuntimeError(
            f"Duplicate mailing_domain {response.get('mailing_domain')!r} does not target Country = Germany"
        )


run_oracle(oracle)
