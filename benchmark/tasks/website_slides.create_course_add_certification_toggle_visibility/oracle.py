"""Oracle for website_slides.create_course_add_certification_toggle_visibility."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/e-learning")
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

            const channelId = unwrapId(await callKw({
                model: 'slide.channel',
                method: 'create',
                args: [[{
                    name: 'Compliance Badge Basics',
                    description_short: '<p>Core rules for badge-ready warehouse operations.</p>',
                    channel_type: 'training',
                    visibility: 'members',
                    enroll: 'invite',
                    website_published: true,
                    is_published: true,
                }]],
                kwargs: {},
            }));

            const slideId = unwrapId(await callKw({
                model: 'slide.slide',
                method: 'create',
                args: [[{
                    name: 'Badge Criteria',
                    channel_id: channelId,
                    slide_category: 'article',
                    html_content: '<p>This article covers the safety checklist for badge-ready operations.</p>',
                    website_published: true,
                    is_published: true,
                    completion_time: 1.0,
                }]],
                kwargs: {},
            }));

            const summary = await callKw({
                model: 'slide.slide',
                method: 'read',
                args: [[slideId], ['name', 'website_published']],
                kwargs: {},
            });
            return summary[0];
        }""",
    )
    if response.get("name") != "Badge Criteria":
        raise RuntimeError(f"slide create failed: {response!r}")


run_oracle(oracle)
