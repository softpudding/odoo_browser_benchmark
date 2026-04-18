"""Oracle for website_slides.duplicate_lesson_to_new_section.

Uses JSON-RPC because the slide.slide section assignment is computed from
the relative sequence of category vs non-category slides on the channel.
We add the new "Advanced" section, copy the original "Welcome Video", then
position the duplicate after the new section (and rename it).
"""

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

            const channels = await callKw({
                model: 'slide.channel',
                method: 'search_read',
                args: [[['name', '=', 'Bench Onboarding Course']], ['id']],
                kwargs: {},
            });
            if (!channels.length) {
                throw new Error('Course "Bench Onboarding Course" not found');
            }
            const channelId = channels[0].id;

            const welcomeRecs = await callKw({
                model: 'slide.slide',
                method: 'search_read',
                args: [
                    [['name', '=', 'Welcome Video'], ['channel_id', '=', channelId]],
                    ['id', 'sequence'],
                ],
                kwargs: {},
            });
            if (!welcomeRecs.length) {
                throw new Error('Lesson "Welcome Video" not found on course');
            }
            const welcomeId = welcomeRecs[0].id;

            // 1. Create the new "Advanced" section after Welcome Video.
            const advancedSectionId = unwrap(await callKw({
                model: 'slide.slide',
                method: 'create',
                args: [[{
                    name: 'Advanced',
                    channel_id: channelId,
                    is_category: true,
                    sequence: 30,
                }]],
                kwargs: {},
            }));

            // 2. Duplicate the Welcome Video lesson via copy().
            const dupId = unwrap(await callKw({
                model: 'slide.slide',
                method: 'copy',
                args: [[welcomeId]],
                kwargs: { default: {} },
            }));

            // 3. Move the duplicate after the Advanced section AND rename it.
            //    The category_id is computed from sequence ordering: the slide
            //    falls under the most recent prior is_category slide.
            await callKw({
                model: 'slide.slide',
                method: 'write',
                args: [[dupId], {
                    name: 'Advanced Welcome',
                    sequence: 40,
                }],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
