"""Oracle for contacts.create_company_with_invoice_and_delivery_addresses."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
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
            const stateRes = await callKw({
                model: 'res.country.state',
                method: 'search_read',
                args: [[['name', '=', 'Oregon']], ['id']],
                kwargs: { limit: 1 },
            });
            const countryRes = await callKw({
                model: 'res.country',
                method: 'search_read',
                args: [[['name', '=', 'United States']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!stateRes.result?.length || !countryRes.result?.length) {
                return 'missing Oregon or United States';
            }
            const companyRes = await callKw({
                model: 'res.partner',
                method: 'create',
                args: [[{
                    name: 'Harbor Peak Logistics',
                    company_type: 'company',
                    is_company: true,
                    phone: '+1 (503) 555-0140',
                    website: 'www.harborpeak-logistics.example.com',
                    street: '820 Rivergate Ave',
                    city: 'Portland',
                    zip: '97217',
                    state_id: stateRes.result[0].id,
                    country_id: countryRes.result[0].id,
                }]],
                kwargs: {},
            });
            const companyId = Array.isArray(companyRes.result) ? companyRes.result[0] : companyRes.result;
            await callKw({
                model: 'res.partner',
                method: 'create',
                args: [[{
                    name: 'Billing Desk',
                    parent_id: companyId,
                    type: 'invoice',
                    company_type: 'person',
                    street: '825 Rivergate Ave',
                    city: 'Portland',
                    zip: '97217',
                    state_id: stateRes.result[0].id,
                    country_id: countryRes.result[0].id,
                }]],
                kwargs: {},
            });
            await callKw({
                model: 'res.partner',
                method: 'create',
                args: [[{
                    name: 'Receiving Dock',
                    parent_id: companyId,
                    type: 'delivery',
                    company_type: 'person',
                    street: '910 Dockside Rd',
                    city: 'Portland',
                    zip: '97217',
                    state_id: stateRes.result[0].id,
                    country_id: countryRes.result[0].id,
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
