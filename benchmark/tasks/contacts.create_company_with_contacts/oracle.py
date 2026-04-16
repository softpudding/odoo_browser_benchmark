"""Oracle for contacts.create_company_with_contacts.

Create company "Vantage Industrial Group" with address details, then create
two individual contacts (Patricia Drum and Steven Okafor) linked to it.
"""

from benchmark.oracle_helpers import (
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def _create_company(page):
    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Ensure "Company" type is selected (not Individual)
    # In Odoo 19 contacts, the company toggle is a radio/checkbox at top
    company_radio = page.locator(
        "div.o_field_radio[name='company_type'] .o_radio_item:has-text('Company') input, "
        "input[value='company'], "
        ".o_field_widget[name='is_company'] input[type='checkbox']"
    ).first
    if company_radio.count() > 0:
        if not company_radio.is_checked():
            company_radio.click()
        page.wait_for_timeout(300)
    else:
        # Try clicking the Company label/button
        page.locator(
            "label:has-text('Company'), .o_radio_item:has-text('Company')"
        ).first.click()
        page.wait_for_timeout(300)

    fill_field(page, "name", "Vantage Industrial Group")
    page.wait_for_timeout(300)

    fill_field(page, "phone", "+1 (312) 555-0190")
    page.wait_for_timeout(300)

    fill_field(page, "website", "www.vantage-industrial.example.com")
    page.wait_for_timeout(300)

    fill_field(page, "street", "4400 Commerce Drive")
    page.wait_for_timeout(300)

    fill_field(page, "city", "Chicago")
    page.wait_for_timeout(300)

    # State: Illinois
    set_many2one(page, "state_id", "Illinois")
    page.wait_for_timeout(500)

    # Country: United States
    set_many2one(page, "country_id", "United States")
    page.wait_for_timeout(500)

    fill_field(page, "zip", "60609")
    page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


def _create_contact(page, name, job_title, email, phone, company_name):
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # In Odoo 19, contacts are "Person" or "Company" (not "Individual")
    # Default is "Person" but ensure it's selected explicitly
    person_radio = page.locator("input[data-value='person']").first
    if not person_radio.is_checked():
        person_radio.click()
        page.wait_for_timeout(500)

    fill_field(page, "name", name)
    page.wait_for_timeout(300)

    # Link to company — parent_id appears after Person type is selected
    set_many2one(page, "parent_id", company_name)
    page.wait_for_timeout(500)

    fill_field(page, "function", job_title)
    page.wait_for_timeout(300)

    fill_field(page, "email", email)
    page.wait_for_timeout(300)

    fill_field(page, "phone", phone)
    page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    # Step 1: Create the company
    _create_company(page)

    # Step 2: Create Patricia Drum
    _create_contact(
        page,
        name="Patricia Drum",
        job_title="Procurement Manager",
        email="p.drum@vantage-industrial.example.com",
        phone="+1 (312) 555-0191",
        company_name="Vantage Industrial Group",
    )

    # Step 3: Create Steven Okafor
    _create_contact(
        page,
        name="Steven Okafor",
        job_title="Logistics Coordinator",
        email="s.okafor@vantage-industrial.example.com",
        phone="+1 (312) 555-0192",
        company_name="Vantage Industrial Group",
    )


run_oracle(oracle)
