"""Oracle for purchase_stock.receive_partial_scrap_damaged_units."""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    click_stat_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def _set_done_qty(page, row_index, value):
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row, "
        ".o_list_view .o_data_row"
    ).nth(row_index)
    cell = row.locator("td[name='quantity'], .o_field_widget[name='quantity']").first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "SCRAP-PO-07")
    page.wait_for_timeout(1000)

    receive_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Receive'), "
        "button[name='action_view_picking']:visible"
    ).first
    receive_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    _set_done_qty(page, 0, "4")
    _set_done_qty(page, 1, "7")

    click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Create Backorder')").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
        _wait_for_ready(page)

    # Create the scrap deterministically via RPC from the first completed receipt.
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
            const [po] = await callKw({
                model: 'purchase.order',
                method: 'search_read',
                args: [[['origin', '=', 'SCRAP-PO-07']], ['id', 'picking_ids']],
                kwargs: { order: 'id desc', limit: 1 },
            });
            if (!po) {
                throw new Error('purchase order missing');
            }
            const [firstPicking] = await callKw({
                model: 'stock.picking',
                method: 'search_read',
                args: [[['id', 'in', po.picking_ids], ['backorder_id', '=', false]], ['id', 'location_dest_id']],
                kwargs: { limit: 1 },
            });
            if (!firstPicking) {
                throw new Error('first receipt missing');
            }
            const [product] = await callKw({
                model: 'product.product',
                method: 'search_read',
                args: [[['name', '=', 'Bench Filter Cartridge']], ['id', 'uom_id']],
                kwargs: { limit: 1 },
            });
            if (!product) {
                throw new Error('filter product missing');
            }
            const scrapId = await callKw({
                model: 'stock.scrap',
                method: 'create',
                args: [[{
                    product_id: product.id,
                    product_uom_id: Array.isArray(product.uom_id) ? product.uom_id[0] : product.uom_id,
                    scrap_qty: 1,
                    picking_id: firstPicking.id,
                    location_id: firstPicking.location_dest_id[0],
                    origin: 'SCRAP-PO-07',
                }]],
                kwargs: {},
            });
            await callKw({
                model: 'stock.scrap',
                method: 'action_validate',
                args: [[Array.isArray(scrapId) ? scrapId[0] : scrapId]],
                kwargs: {},
            });
            return 'ok';
        }"""
    )
    if response != "ok":
        raise RuntimeError(response)

    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    click_list_row(page, "SCRAP-PO-07")
    page.wait_for_timeout(1000)
    click_stat_button(page, "Receipt")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    ready_row = page.locator(
        ".o_list_view .o_data_row:has-text('Ready'), "
        ".o_list_view .o_data_row:has-text('Assigned')"
    )
    if ready_row.count() > 0:
        ready_row.first.click()
    else:
        rows = page.locator(".o_list_view .o_data_row")
        rows.nth(1).click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    _set_done_qty(page, 0, "2")
    _set_done_qty(page, 1, "3")

    click_button(page, "Validate")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Ok'), button.btn-primary").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
