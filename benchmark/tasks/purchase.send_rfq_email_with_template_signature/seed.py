"""Seed for purchase.send_rfq_email_with_template_signature (HARD).

Category 2: Policy trap (wizard) + side-effect trap.

Workflow:
  - Agent opens a seeded draft RFQ (R-BENCH-EMAIL-001) for vendor
    'Beacon Electrical Ltd.'.
  - Clicks the 'Send RFQ' header button → mail.compose.message wizard
    opens with 'Purchase: Request For Quotation' template pre-loaded.
  - Must APPEND 'Please confirm by Friday.' to the existing body without
    replacing the template text, then click Send.

Hard failure patterns:
  - BU frequently hits the primary Send button without touching the body
    (default success path).
  - When BU does interact with the body, it tends to Ctrl+A + Backspace
    then type only its sentence — replacing the template content entirely.
    Our check.py enforces BOTH the template greeting AND the appended
    sentence remain in the sent mail.message body.

Calibration (SMTP sink):
  Purchase 'Send RFQ' ultimately fires mail.mail.send() which requires a
  working outgoing mail server. Without it, SMTP fails, the transaction
  rolls back, and the mail.message / 'sent' state never persist. Seed
  spawns a detached aiosmtpd Sink on 127.0.0.1:2525 (same pattern as
  mail.invite_external_email_to_existing_channel / cookbook row 323) and
  registers an ir.mail_server pointing at it.
"""

import os
import socket
import subprocess
import time


VENDOR_NAME = "Beacon Electrical Ltd."
VENDOR_EMAIL = "orders@beacon-electrical.example.com"
TARGET_REF = "R-BENCH-EMAIL-001"
DISTRACTOR_REF = "R-BENCH-EMAIL-002"

PRODUCT_CABLE = "Industrial Cable 10m"
PRODUCT_RELAY = "Relay Module"

SMTP_HOST = "127.0.0.1"
SMTP_PORT = 2525


def _port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def _find_repo_root():
    import sys
    for p in sys.path + [os.getcwd()]:
        if not p:
            continue
        cur = os.path.abspath(p)
        for _ in range(8):
            candidate = os.path.join(cur, ".venv", "bin", "python")
            if os.path.exists(candidate):
                return cur
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    return os.getcwd()


def _start_fake_smtp():
    """Idempotently start a detached aiosmtpd Sink for the Send RFQ flow."""
    if _port_open(SMTP_HOST, SMTP_PORT):
        return
    repo_root = _find_repo_root()
    python = os.path.join(repo_root, ".venv", "bin", "python")
    if not os.path.exists(python):
        python = "python3"
    script = (
        "from aiosmtpd.controller import Controller\n"
        "from aiosmtpd.handlers import Sink\n"
        f"c = Controller(Sink(), hostname={SMTP_HOST!r}, port={SMTP_PORT})\n"
        "c.start()\n"
        "import time\n"
        "while True:\n"
        "    time.sleep(60)\n"
    )
    try:
        subprocess.Popen(
            [python, "-c", script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError:
        return
    for _ in range(50):
        if _port_open(SMTP_HOST, SMTP_PORT):
            return
        time.sleep(0.1)


def _cleanup(env):
    """Cleanup prior runs — must handle all PO states + stray mail data."""
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_ref", "in", [TARGET_REF, DISTRACTOR_REF]),
    ])
    for po in pos:
        env["mail.message"].search([
            ("model", "=", "purchase.order"),
            ("res_id", "=", po.id),
        ]).unlink()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "list_price": price,
            "standard_price": price,
        })
        return product
    tmpl = env["product.template"].create({
        "name": name,
        "type": "consu",
        "list_price": price,
        "standard_price": price,
    })
    return tmpl.product_variant_id


def _make_po(env, vendor, ref, products_prices):
    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "partner_ref": ref,
        "origin": ref,
    })
    for prod, qty, price in products_prices:
        env["purchase.order.line"].create({
            "order_id": po.id,
            "product_id": prod.id,
            "product_qty": qty,
            "price_unit": price,
            "tax_ids": [(5, 0, 0)],
        })
    return po


def setup(env):
    _cleanup(env)

    # --- Fake outgoing SMTP sink so Send RFQ doesn't roll back ---
    _start_fake_smtp()
    env["ir.mail_server"].with_context(active_test=False).search(
        [("name", "=", "benchmark_fake_smtp")]
    ).unlink()
    env["ir.mail_server"].create({
        "name": "benchmark_fake_smtp",
        "smtp_host": SMTP_HOST,
        "smtp_port": SMTP_PORT,
        "smtp_encryption": "none",
        "smtp_authentication": "login",
        "from_filter": False,
        "sequence": 1,
    })

    # Admin needs an email_formatted for mail_from on the outbound.
    admin = env.ref("base.user_admin")
    if not admin.partner_id.email:
        admin.partner_id.write({"email": "admin@bench.test"})

    env["ir.config_parameter"].sudo().set_param(
        "mail.catchall.domain", "bench.test"
    )
    env["ir.config_parameter"].sudo().set_param(
        "mail.default.from", "no-reply"
    )

    # The 'Purchase: Request For Quotation' mail template attaches a PDF
    # report (purchase.report_purchase_quotation) by default. Rendering
    # the PDF requires wkhtmltopdf which is NOT installed on the benchmark
    # runners — it pops an "Unable to find Wkhtmltopdf" error dialog
    # instead of opening the compose wizard. Detach the report from both
    # the RFQ and PO templates so Send RFQ reliably opens the compose.
    for xml_id in (
        "purchase.email_template_edi_purchase",
        "purchase.email_template_edi_purchase_done",
    ):
        tpl = env.ref(xml_id, raise_if_not_found=False)
        if tpl and tpl.report_template_ids:
            tpl.write({"report_template_ids": [(5, 0, 0)]})

    # --- Vendor with an email (required so template.use_default_to resolves
    # to a partner_to recipient whose email marks partner_ids_all_have_email
    # True → the primary 'Send' button stays enabled). ---
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": VENDOR_EMAIL,
            "supplier_rank": 1,
        })
    else:
        vendor.write({
            "email": VENDOR_EMAIL,
            "supplier_rank": max(vendor.supplier_rank, 1),
        })

    # --- Products ---
    cable = _ensure_product(env, PRODUCT_CABLE, 32.0)
    relay = _ensure_product(env, PRODUCT_RELAY, 18.5)

    # --- Target draft RFQ ---
    _make_po(env, vendor, TARGET_REF, [
        (cable, 5, 32.0),
        (relay, 10, 18.5),
    ])
    # --- Distractor draft RFQ (same vendor, must NOT be modified) ---
    _make_po(env, vendor, DISTRACTOR_REF, [
        (cable, 2, 32.0),
    ])
