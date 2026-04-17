"""Oracle for hr_recruitment.schedule_second_interview_with_feedback."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    response = page.evaluate(
        """async () => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const applicantRes = await callKw({
                model: 'hr.applicant',
                method: 'search_read',
                args: [[['partner_name', '=', 'Mina Chen']], ['id']],
                kwargs: { limit: 1 },
            });
            const stageRes = await callKw({
                model: 'hr.recruitment.stage',
                method: 'search_read',
                args: [[['name', '=', 'Second Interview']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!applicantRes.length || !stageRes.length) {
                throw new Error('missing applicant or second interview stage');
            }
            const applicantId = applicantRes[0].id;
            await callKw({
                model: 'hr.applicant',
                method: 'write',
                args: [[applicantId], {
                    stage_id: stageRes[0].id,
                    applicant_notes: '<p>Strong process knowledge and clear stakeholder communication.</p>',
                }],
                kwargs: {},
            });
            await callKw({
                model: 'calendar.event',
                method: 'create',
                args: [[{
                    name: 'Second Interview - Mina Chen',
                    start: '2026-06-25 14:00:00',
                    stop: '2026-06-25 14:30:00',
                    applicant_id: applicantId,
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
