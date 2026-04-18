"""Oracle for website_hr_recruitment.apply_public_then_schedule_interview."""

from benchmark.oracle_helpers import (
    full_url,
    run_oracle,
    DB,
    login,
    navigate,
)


def oracle(page):
    login(page)

    url = "/jobs"
    if DB:
        url = f"/jobs?db={DB}"
    page.goto(full_url(url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # If we hit a database selector page, select the DB
    db_select = page.locator("select[name='db']")
    if db_select.count() > 0 and db_select.is_visible():
        if DB:
            db_select.select_option(DB)
            page.wait_for_timeout(1000)
        page.goto(full_url(url))
        page.wait_for_load_state("load")
        page.wait_for_timeout(3000)

    job_link = page.locator("a:has-text('Platform Support Analyst')").first
    job_link.wait_for(timeout=10000)
    job_link.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    apply_btn = page.locator(
        "a:has-text('Apply'), "
        "button:has-text('Apply')"
    ).first
    apply_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    page.locator("input[name='partner_name']").first.fill("Casey Portal")
    page.locator("input[name='email_from']").first.fill("casey.portal@example.com")
    page.locator("input[name='partner_phone']").first.fill("+1 555 0128")
    page.locator("input[name='linkedin_profile']").first.fill(
        "linkedin.com/in/casey-portal"
    )
    page.locator("textarea[name='short_introduction']").first.fill(
        "Public applicant ready for interview scheduling."
    )
    page.locator(".s_website_form_send").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    page.wait_for_selector(
        ".s_website_form_end_message:visible, "
        "span:has-text('Thank'):visible, "
        "div:has-text('submitted'):visible, "
        "div:has-text('Congratulations'):visible",
        timeout=15000,
    )

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

            const applicant = await callKw({
                model: 'hr.applicant',
                method: 'search_read',
                args: [[['partner_name', '=', 'Casey Portal'], ['email_from', '=', 'casey.portal@example.com']], ['id']],
                kwargs: { limit: 1 },
            });
            const user = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'marc.demo']], ['id']],
                kwargs: { limit: 1 },
            });
            const activityType = await callKw({
                model: 'mail.activity.type',
                method: 'search_read',
                args: [[['name', 'ilike', 'Call']], ['id']],
                kwargs: { limit: 1 },
            });
            const modelRes = await callKw({
                model: 'ir.model',
                method: 'search_read',
                args: [[['model', '=', 'hr.applicant']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!applicant.length || !user.length || !activityType.length || !modelRes.length) {
                return 'missing applicant or activity metadata';
            }
            await callKw({
                model: 'mail.activity',
                method: 'create',
                args: [[{
                    res_model_id: modelRes[0].id,
                    res_id: applicant[0].id,
                    activity_type_id: activityType[0].id,
                    user_id: user[0].id,
                    date_deadline: '2026-05-28',
                    summary: 'Schedule initial interview',
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
