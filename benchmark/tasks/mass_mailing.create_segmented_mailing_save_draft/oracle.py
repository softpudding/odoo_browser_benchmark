"""Oracle for mass_mailing.create_segmented_mailing_save_draft.

The mailing.mailing form ships with a finicky domain widget (tree editor
with field-path autocomplete) and a WYSIWYG editor that Playwright cannot
always drive deterministically. To keep the oracle reliable we navigate
to /odoo/email-marketing (proving the workflow exists in the UI for the
admin user) and then commit the canonical mailing record via JSON-RPC.

The browser-use agent must perform the same workflow through the UI; the
postcondition checks (check.py) will validate that whatever route was
taken left the database in the correct end state.
"""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    login,
    navigate,
    run_oracle,
)


SUBJECT = "Berlin April Bulletin"


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

            const modelRes = await callKw({
                model: 'ir.model',
                method: 'search_read',
                args: [[['model', '=', 'res.partner']], ['id']],
                kwargs: { limit: 1 },
            });
            const partnerModelId = modelRes.result?.[0]?.id;
            if (!partnerModelId) return 'no res.partner ir.model';

            const existing = await callKw({
                model: 'mailing.mailing',
                method: 'search_read',
                args: [[['subject', '=', 'Berlin April Bulletin']], ['id']],
                kwargs: {},
            });
            const existingIds = (existing.result || []).map(r => r.id);
            if (existingIds.length) {
                await callKw({
                    model: 'mailing.mailing',
                    method: 'unlink',
                    args: [existingIds],
                    kwargs: {},
                });
            }

            // Get current user's email_from for the mailing.
            const userRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['email', 'partner_id']],
                kwargs: { limit: 1 },
            });
            const userEmail = userRes.result?.[0]?.email
                || (userRes.result?.[0]?.partner_id && userRes.result[0].partner_id[1])
                || 'admin@example.com';

            const created = await callKw({
                model: 'mailing.mailing',
                method: 'create',
                args: [[{
                    subject: 'Berlin April Bulletin',
                    email_from: userEmail,
                    mailing_model_id: partnerModelId,
                    contact_list_ids: [[5, 0, 0]],
                    mailing_domain: "[('city', '=', 'Berlin')]",
                    body_html: '<p>Hello Berlin team — here is our April bulletin.</p>',
                    body_arch: '<p>Hello Berlin team — here is our April bulletin.</p>',
                }]],
                kwargs: {},
            });
            let mailingId = created.result;
            if (!mailingId) {
                return 'DEBUG create error: ' + JSON.stringify(created.error);
            }
            if (Array.isArray(mailingId)) {
                mailingId = mailingId[0];
            }

            const after = await callKw({
                model: 'mailing.mailing',
                method: 'read',
                args: [[mailingId], ['state', 'mailing_model_name', 'mailing_domain', 'subject', 'mailing_model_id']],
                kwargs: {},
            });
            return after.result?.[0] || ('no read result for id=' + mailingId + ' err=' + JSON.stringify(after.error));
        }""",
    )
    if isinstance(response, str):
        raise RuntimeError(f"Oracle JSON-RPC failed: {response}")
    if response.get("state") != "draft":
        raise RuntimeError(f"Mailing state is {response.get('state')!r}, expected 'draft'")
    if response.get("mailing_model_name") != "res.partner":
        raise RuntimeError(
            f"mailing_model_name is {response.get('mailing_model_name')!r}, expected 'res.partner'"
        )


run_oracle(oracle)
