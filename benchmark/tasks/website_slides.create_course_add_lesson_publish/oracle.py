"""Oracle for website_slides.create_course_add_lesson_publish."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/e-learning")
    response = page.evaluate(
        """async () => {
            const unwrap = (value) => Array.isArray(value) ? value[0] : value;
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
            const channelId = unwrap(await callKw({
                model: 'slide.channel',
                method: 'create',
                args: [[{
                    name: 'Dock Safety Express',
                    description_short: '<p>A quick refresher for loading-bay launch crews.</p>',
                    channel_type: 'training',
                    visibility: 'public',
                    is_published: true,
                }]],
                kwargs: {},
            }));
            await callKw({
                model: 'slide.slide',
                method: 'create',
                args: [[{
                    name: 'Emergency Exit Drill',
                    channel_id: channelId,
                    slide_category: 'article',
                    html_content: '<p>Review the alarm path and the assembly point before departure.</p>',
                    is_published: true,
                    completion_time: 1.0,
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
