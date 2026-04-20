"""Oracle for website_hr_recruitment.publish_job_set_interview_form_and_archive_old_posting."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    response = page.evaluate(
        """async () => {
            const unwrapId = (value) => Array.isArray(value) ? value[0] : value;
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

            const deptRes = await callKw({
                model: 'hr.department',
                method: 'search_read',
                args: [[['name', '=', 'Administration']], ['id']],
                kwargs: { limit: 1 },
            });
            const surveyRes = await callKw({
                model: 'survey.survey',
                method: 'search_read',
                args: [[['title', '=', 'Bench Interview Form']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!deptRes.length || !surveyRes.length) {
                throw new Error('missing department or survey seed');
            }

            const newId = unwrapId(await callKw({
                model: 'hr.job',
                method: 'create',
                args: [[{
                    name: 'Warehouse Interview Specialist',
                    department_id: deptRes[0].id,
                    no_of_recruitment: 1,
                    description: '<p>Run warehouse candidate interviews and calibration sessions.</p>',
                    survey_id: surveyRes[0].id,
                    is_published: true,
                    website_published: true,
                    active: true,
                }]],
                kwargs: {},
            }));

            const legacyRes = await callKw({
                model: 'hr.job',
                method: 'search_read',
                args: [[['name', '=', 'Legacy Support Agent']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!legacyRes.length) {
                throw new Error('legacy job missing');
            }
            await callKw({
                model: 'hr.job',
                method: 'write',
                args: [[legacyRes[0].id], {
                    active: false,
                    is_published: false,
                    website_published: false,
                }],
                kwargs: {},
            });

            const finalState = await callKw({
                model: 'hr.job',
                method: 'read',
                args: [[newId], ['name', 'is_published', 'website_published', 'active']],
                kwargs: {},
            });
            return finalState[0];
        }""",
    )
    if response.get("name") != "Warehouse Interview Specialist":
        raise RuntimeError(f"job create failed: {response!r}")


run_oracle(oracle)
