"""Oracle for website_slides.duplicate_course_edit_add_slide.

Uses JSON-RPC because eLearning's kanban + course form iframe transitions
are fragile under Playwright, and `slide.channel.copy` followed by a rename
via the form is much flakier than a direct RPC call. Browser-use still has
to solve this through the UI.
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

            const originals = await callKw({
                model: 'slide.channel',
                method: 'search_read',
                args: [[['name', '=', 'Bench Course Original']], ['id']],
                kwargs: {},
            });
            if (!originals.length) {
                throw new Error('Course "Bench Course Original" not found');
            }
            const originalId = originals[0].id;

            // 1. Duplicate the slide.channel (cog -> Duplicate equivalent).
            const copyId = unwrap(await callKw({
                model: 'slide.channel',
                method: 'copy',
                args: [[originalId]],
                kwargs: { default: {} },
            }));

            // 2. Rename the copy to "Bench Course Spring".
            await callKw({
                model: 'slide.channel',
                method: 'write',
                args: [[copyId], { name: 'Bench Course Spring' }],
                kwargs: {},
            });

            // slide.channel.copy() duplicates the seeded "Bench Intro Video"
            // slide onto the new channel (via copy_data). Remove it so the
            // Spring copy ends up with exactly the one new slide the task
            // requires.
            const copiedSlides = await callKw({
                model: 'slide.slide',
                method: 'search_read',
                args: [[['channel_id', '=', copyId]], ['id']],
                kwargs: {},
            });
            if (copiedSlides.length) {
                await callKw({
                    model: 'slide.slide',
                    method: 'unlink',
                    args: [copiedSlides.map((s) => s.id)],
                    kwargs: {},
                });
            }

            // 3. Add a new article slide titled "Welcome slide" on the copy.
            await callKw({
                model: 'slide.slide',
                method: 'create',
                args: [[{
                    name: 'Welcome slide',
                    channel_id: copyId,
                    slide_category: 'article',
                    html_content: '<p>Welcome to the spring session of the Bench course.</p>',
                    is_published: true,
                    completion_time: 0.05,
                }]],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
