"""Pure JSON-RPC oracle for website_hr_recruitment.apply_public_then_schedule_interview.

This oracle does NOT use a browser. It proves the task is solvable by hitting
Odoo's JSON-RPC endpoint directly:
  1. Create an `hr.applicant` for the seeded "Senior Backend Engineer" job
     with the expected partner_name / email_from / description (cover letter).
  2. Create a `mail.activity` linked to that applicant with:
       - activity_type_id  -> the "Meeting" type
       - summary           -> "Interview"
       - date_deadline     -> 2026-05-04
       - user_id           -> admin

Environment variables (set by eval.py --agent oracle):
  BENCHMARK_BASE_URL   -- e.g. http://127.0.0.1:8069
  BENCHMARK_DB         -- target database
  BENCHMARK_LOGIN      -- login (default "admin")
  BENCHMARK_PASSWORD   -- password (default "admin")
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

BASE_URL = os.environ.get("BENCHMARK_BASE_URL", "http://127.0.0.1:8069").rstrip("/")
DB = os.environ.get("BENCHMARK_DB", "")
LOGIN = os.environ.get("BENCHMARK_LOGIN") or "admin"
PASSWORD = os.environ.get("BENCHMARK_PASSWORD") or "admin"

JOB_NAME = "Senior Backend Engineer"
APPLICANT_NAME = "Bench Candidate"
APPLICANT_EMAIL = "bench.candidate@example.com"
APPLICANT_PHONE = "+1 555 0143"
APPLICANT_LINKEDIN = "linkedin.com/in/bench-candidate"
APPLICANT_INTRO = (
    "Excited to interview for the Senior Backend Engineer role."
)
ACTIVITY_SUMMARY = "Interview"
ACTIVITY_DATE = "2026-05-04"


def jsonrpc_call(url: str, service: str, method: str, args: list):
    """Low-level JSON-RPC call to Odoo."""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args,
        },
        "id": 1,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{url}/jsonrpc",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if "error" in body:
        raise RuntimeError(f"JSON-RPC error: {body['error']}")
    return body.get("result")


def authenticate(base_url: str, db: str, login: str, password: str) -> int:
    uid = jsonrpc_call(base_url, "common", "authenticate", [db, login, password, {}])
    if not uid:
        raise RuntimeError(f"JSON-RPC auth failed for {login}@{db}")
    return uid


def execute_kw(base_url, db, uid, password, model, method, args, kwargs=None):
    return jsonrpc_call(
        base_url, "object", "execute_kw",
        [db, uid, password, model, method, args, kwargs or {}],
    )


def main():
    if not DB:
        print("ERROR: BENCHMARK_DB is not set", file=sys.stderr)
        sys.exit(1)

    uid = authenticate(BASE_URL, DB, LOGIN, PASSWORD)

    # -----------------------------------------------------------------
    # 1. Locate the seeded job.
    # -----------------------------------------------------------------
    jobs = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "hr.job", "search_read",
        [[("name", "=", JOB_NAME)]],
        {"fields": ["id", "name", "department_id"], "limit": 1},
    )
    if not jobs:
        raise RuntimeError(f"hr.job '{JOB_NAME}' not found (seed may have failed)")
    job = jobs[0]
    job_id = job["id"]
    department_id = job["department_id"][0] if job.get("department_id") else False

    # Ensure no stray applicant exists from a previous aborted oracle run.
    existing = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "hr.applicant", "search",
        [[
            "|",
            ("partner_name", "=", APPLICANT_NAME),
            ("email_from", "=", APPLICANT_EMAIL),
        ]],
        {},
    )
    if existing:
        # Cancel linked activities first.
        act_ids = execute_kw(
            BASE_URL, DB, uid, PASSWORD,
            "mail.activity", "search",
            [[("res_model", "=", "hr.applicant"), ("res_id", "in", existing)]],
            {},
        )
        if act_ids:
            execute_kw(BASE_URL, DB, uid, PASSWORD, "mail.activity", "unlink", [act_ids])
        execute_kw(BASE_URL, DB, uid, PASSWORD, "hr.applicant", "unlink", [existing])

    # -----------------------------------------------------------------
    # 2. Create the applicant (mirrors what /website/form/hr.applicant does).
    # -----------------------------------------------------------------
    applicant_vals = {
        "partner_name": APPLICANT_NAME,
        "email_from": APPLICANT_EMAIL,
        "partner_phone": APPLICANT_PHONE,
        "linkedin_profile": APPLICANT_LINKEDIN,
        "job_id": job_id,
    }
    if department_id:
        applicant_vals["department_id"] = department_id

    applicant_id = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "hr.applicant", "create",
        [applicant_vals],
    )
    print(f"Created hr.applicant id={applicant_id}")

    # Post the cover letter to the chatter so downstream checks that look at
    # message_ids also pass (mirrors the public form's short_introduction).
    execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "hr.applicant", "message_post",
        [[applicant_id]],
        {"body": APPLICANT_INTRO},
    )

    # -----------------------------------------------------------------
    # 3. Schedule the "Meeting" activity named "Interview" on 2026-05-04.
    # -----------------------------------------------------------------
    meeting_type = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "mail.activity.type", "search_read",
        [[("name", "=", "Meeting")]],
        {"fields": ["id", "name"], "limit": 1},
    )
    if not meeting_type:
        # Fallback: some DBs localise to e.g. category "meeting"
        meeting_type = execute_kw(
            BASE_URL, DB, uid, PASSWORD,
            "mail.activity.type", "search_read",
            [[("category", "=", "meeting")]],
            {"fields": ["id", "name"], "limit": 1},
        )
    if not meeting_type:
        raise RuntimeError("mail.activity.type 'Meeting' not found")

    applicant_model = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "ir.model", "search_read",
        [[("model", "=", "hr.applicant")]],
        {"fields": ["id"], "limit": 1},
    )
    if not applicant_model:
        raise RuntimeError("ir.model for hr.applicant not found")

    activity_vals = {
        "res_model": "hr.applicant",
        "res_model_id": applicant_model[0]["id"],
        "res_id": applicant_id,
        "activity_type_id": meeting_type[0]["id"],
        "summary": ACTIVITY_SUMMARY,
        "date_deadline": ACTIVITY_DATE,
        "user_id": uid,
    }
    activity_id = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "mail.activity", "create",
        [activity_vals],
    )
    print(f"Created mail.activity id={activity_id} on hr.applicant id={applicant_id}")
    print("Oracle: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"Oracle: FAIL - {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
