"""Oracle for website_sale_slides.assign_attendees_publish_course.

Drives the canonical end-state via JSON-RPC because the UI path mixes a
backend form notebook tab, a frontend Owl publish systray toggle, and the
Add Attendees email wizard — each of which is individually fragile under
Playwright, and together spew too many race conditions for a deterministic
oracle.  The browser-use agent still has to solve the task via the UI.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/e-learning")
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

            const courses = await callKw({
                model: 'slide.channel',
                method: 'search_read',
                args: [[['name', '=', 'Bench Onboarding']], ['id']],
                kwargs: {},
            });
            if (!courses.length) {
                throw new Error('Course "Bench Onboarding" not found');
            }
            const courseId = courses[0].id;

            const prereqs = await callKw({
                model: 'slide.channel',
                method: 'search_read',
                args: [[['name', '=', 'Bench 101']], ['id']],
                kwargs: {},
            });
            if (!prereqs.length) {
                throw new Error('Course "Bench 101" not found');
            }
            const prereqId = prereqs[0].id;

            const partners = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [
                    [['name', 'in', ['Alice Attendee', 'Bob Attendee']]],
                    ['id', 'name'],
                ],
                kwargs: {},
            });
            if (partners.length !== 2) {
                throw new Error(
                    'Expected two partners (Alice Attendee, Bob Attendee), got '
                    + partners.length
                );
            }
            const partnerIds = partners.map((p) => p.id);

            // 1. Set visibility='members' (auto-flips enroll to 'invite') AND
            //    publish. Doing both in a single write keeps the prerequisite
            //    domain check happy on the following write.
            await callKw({
                model: 'slide.channel',
                method: 'write',
                args: [[courseId], {
                    visibility: 'members',
                    is_published: true,
                }],
                kwargs: {},
            });

            // 2. Add Bench 101 as a prerequisite (m2m (4, id, 0) link).
            await callKw({
                model: 'slide.channel',
                method: 'write',
                args: [[courseId], {
                    prerequisite_channel_ids: [[4, prereqId, 0]],
                }],
                kwargs: {},
            });

            // 3. Enroll Alice + Bob as attendees. `_action_add_members` is
            //    the private helper the Add Attendees wizard ultimately calls
            //    after its mail.mail compose leg — not exposed via call_kw.
            //    Create slide.channel.partner rows directly with the same
            //    end-state (member_status='joined').
            await callKw({
                model: 'slide.channel.partner',
                method: 'create',
                args: [partnerIds.map((pid) => ({
                    channel_id: courseId,
                    partner_id: pid,
                    member_status: 'joined',
                }))],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
