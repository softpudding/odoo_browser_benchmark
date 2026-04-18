"""Oracle for survey.duplicate_survey_rename_archive_original.

Uses authenticated JSON-RPC: locate the original survey, copy it, rename the
copy to the target title, then archive the original via action_archive.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


ORIGINAL_TITLE = "Quarterly Pulse Q1 Template"
COPY_TITLE = "Quarterly Pulse Q2 2026"


def oracle(page):
    login(page)
    navigate(page, "/odoo/surveys")

    response = page.evaluate(
        """async ([originalTitle, copyTitle]) => {
            const unwrap = (v) => Array.isArray(v) ? v[0] : v;
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const originals = await callKw({
                model: 'survey.survey',
                method: 'search_read',
                args: [[['title', '=', originalTitle]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!originals.length) throw new Error('Original survey missing');
            const originalId = originals[0].id;

            const copyResult = await callKw({
                model: 'survey.survey',
                method: 'copy',
                args: [[originalId]],
                kwargs: {},
            });
            const copyId = unwrap(copyResult);

            await callKw({
                model: 'survey.survey',
                method: 'write',
                args: [[copyId], { title: copyTitle }],
                kwargs: {},
            });

            await callKw({
                model: 'survey.survey',
                method: 'action_archive',
                args: [[originalId]],
                kwargs: {},
            });

            return 'ok';
        }""",
        [ORIGINAL_TITLE, COPY_TITLE],
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
