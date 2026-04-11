#!/usr/bin/env python3
"""Phase 0 end-to-end validation script.

Validates the benchmark framework by running the pilot task
(website_hr_recruitment.apply_guru_job) against a live Odoo instance.

Success criteria from the spec:
  1. Reproduce one existing Odoo test and emit a stable trace plus
     normalized state diff.
  2. Verify that two consecutive runs from restored snapshots produce
     identical normalized pre-task state.

Usage::

    # Step 1: Prepare — create a benchmark DB and snapshot
    python benchmark/validate.py prepare --source-db odoo_dev

    # Step 2: Run — execute the pilot task with browser-use
    python benchmark/validate.py run --provider dashscope --headed

    # Step 3: Check — inspect the artifacts
    python benchmark/validate.py check

    # Step 4: Reproducibility — run twice and compare pre-task states
    python benchmark/validate.py reproduce

    # All-in-one (prepare + run + check):
    python benchmark/validate.py all --source-db odoo_dev --provider dashscope --headed
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = REPO_ROOT / "benchmark"
TASK_DIR = BENCHMARK_DIR / "tasks" / "website_hr_recruitment.apply_guru_job"
OUTPUT_DIR = BENCHMARK_DIR / "reports" / "validate_run"

BENCHMARK_DB = "benchmark_validate"
SNAPSHOT_NAME = "website_hr_recruitment_base"
ODOO_BIN = str(REPO_ROOT / "odoo-bin")
# Use the venv python for Odoo commands (has babel, lxml, etc.)
ODOO_PYTHON = str(REPO_ROOT / ".venv" / "bin" / "python3")
if not Path(ODOO_PYTHON).exists():
    ODOO_PYTHON = sys.executable
ODOO_CONF = REPO_ROOT / ".odoorc.local"
BASE_URL = "http://127.0.0.1:8069"


def cmd_prepare(args: argparse.Namespace) -> None:
    """Create a benchmark database with the recruitment module installed."""
    from benchmark.db import DatabaseManager

    db = DatabaseManager(db_user=args.db_user)
    source = args.source_db

    print(f"=== Phase 0 Validation: Prepare ===")
    print()

    # Step 1: Clone source DB for benchmark use
    print(f"1. Cloning {source} -> {BENCHMARK_DB}...")
    db.clone_database(source, BENCHMARK_DB)
    print(f"   Done.")

    # Step 2: Ensure website_hr_recruitment module is installed
    print(f"2. Installing website_hr_recruitment module...")
    result = subprocess.run(
        [
            ODOO_PYTHON, ODOO_BIN,
            "-c", str(ODOO_CONF),
            "-d", BENCHMARK_DB,
            "-i", "website_hr_recruitment",
            "--stop-after-init",
            "--no-http",
        ],
        capture_output=True, text=True,
        cwd=str(REPO_ROOT),
        timeout=300,
    )
    if result.returncode != 0:
        print(f"   WARNING: odoo-bin returned {result.returncode}")
        # Check if it's just warnings vs real failure
        if "ERROR" in result.stderr:
            print(f"   STDERR (last 20 lines):")
            for line in result.stderr.splitlines()[-20:]:
                print(f"     {line}")
        else:
            print(f"   (non-zero exit but no ERROR in stderr — likely OK)")
    else:
        print(f"   Done.")

    # Step 3: Run the seed script via odoo shell
    print(f"3. Seeding benchmark data (department + Guru job)...")
    seed_code = """
env = self.env
dept = env['hr.department'].search([('name', '=', 'guru team')])
if not dept:
    dept = env['hr.department'].create({'name': 'guru team'})
job = env['hr.job'].search([('name', '=', 'Guru'), ('department_id', '=', dept.id)])
if not job:
    env['hr.job'].create({
        'name': 'Guru',
        'is_published': True,
        'department_id': dept.id,
    })
env.cr.commit()
print('SEED_OK')
"""
    result = subprocess.run(
        [
            ODOO_PYTHON, ODOO_BIN,
            "shell", "-c", str(ODOO_CONF),
            "-d", BENCHMARK_DB,
            "--no-http",
        ],
        input=seed_code,
        capture_output=True, text=True,
        cwd=str(REPO_ROOT),
        timeout=120,
    )
    if "SEED_OK" in result.stdout:
        print(f"   Done.")
    else:
        print(f"   WARNING: seed may have failed")
        print(f"   stdout: {result.stdout[-500:]}")
        print(f"   stderr: {result.stderr[-500:]}")

    # Step 4: Create a snapshot for reproducibility testing
    print(f"4. Creating snapshot '{SNAPSHOT_NAME}'...")
    path = db.create_snapshot(BENCHMARK_DB, SNAPSHOT_NAME)
    print(f"   Saved to {path}")

    print()
    print(f"Preparation complete. Run: python benchmark/validate.py run")


def cmd_run(args: argparse.Namespace) -> None:
    """Run the pilot task with browser-use against a live Odoo."""
    print(f"=== Phase 0 Validation: Run ===")
    print()

    # Check Odoo is running
    print(f"1. Checking Odoo at {BASE_URL}...")
    try:
        import urllib.request
        resp = urllib.request.urlopen(f"{BASE_URL}/web/login", timeout=5)
        print(f"   Odoo is running (HTTP {resp.status})")
    except Exception as exc:
        print(f"   Odoo is NOT running: {exc}")
        print(f"   Start it with: python odoo-bin -c .odoorc.local -d {BENCHMARK_DB}")
        return

    # Build the task instruction
    prompt = (TASK_DIR / "prompt.md").read_text().strip()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Run browser-use with the benchmark task
    print(f"2. Running browser-use agent on pilot task...")
    print(f"   Task: website_hr_recruitment.apply_guru_job")
    print(f"   Prompt: {prompt[:80]}...")
    print()

    bu_args = [
        ODOO_PYTHON, str(REPO_ROOT / "setup" / "browser_use_local.py"),
        prompt,
        "--base-url", BASE_URL,
        "--start-path", "/jobs",
        "--db", BENCHMARK_DB,
        "--max-steps", "50",
    ]

    if args.provider:
        bu_args.extend(["--provider", args.provider])
    if args.model:
        bu_args.extend(["--model", args.model])
    if args.headed:
        bu_args.append("--headed")

    print(f"   Command: {' '.join(bu_args[:6])} ...")
    print()

    t0 = time.time()
    result = subprocess.run(
        bu_args,
        cwd=str(REPO_ROOT),
        timeout=300,
    )
    wall_clock = time.time() - t0

    print()
    print(f"   Agent finished in {wall_clock:.1f}s (exit code {result.returncode})")

    # Now capture the state diff by inspecting the DB
    print(f"3. Capturing post-run state...")
    check_code = f"""
import json
env = self.env

# Check for new applicants
applicants = env['hr.applicant'].search([])
records = []
for a in applicants:
    records.append({{
        'partner_name': a.partner_name,
        'email_from': a.email_from,
        'partner_phone': a.partner_phone,
        'linkedin_profile': a.linkedin_profile or '',
        'job': a.job_id.name if a.job_id else '',
        'department': a.department_id.name if a.department_id else '',
    }})

result = {{
    'applicant_count': len(applicants),
    'applicants': records,
    'wall_clock_sec': {wall_clock},
}}
print('RESULT_JSON:' + json.dumps(result))
"""
    capture_result = subprocess.run(
        [
            ODOO_PYTHON, ODOO_BIN,
            "shell", "-c", str(ODOO_CONF),
            "-d", BENCHMARK_DB,
            "--no-http",
        ],
        input=check_code,
        capture_output=True, text=True,
        cwd=str(REPO_ROOT),
        timeout=60,
    )

    # Parse result
    run_data = None
    for line in capture_result.stdout.splitlines():
        if line.startswith("RESULT_JSON:"):
            run_data = json.loads(line[len("RESULT_JSON:"):])
            break

    if run_data:
        # Save artifacts
        (OUTPUT_DIR / "run_result.json").write_text(json.dumps(run_data, indent=2))
        print(f"   Found {run_data['applicant_count']} applicant(s)")
        for a in run_data.get("applicants", []):
            print(f"     - {a['partner_name']} ({a['email_from']}) -> {a['job']}")

        # Basic validation
        print()
        print(f"4. Validating against expected state...")
        expected = json.loads((TASK_DIR / "expected_state.json").read_text())
        expected_name = next(
            (e["norm_value"] for e in expected if e["field"] == "partner_name"),
            None,
        )
        found = any(
            a["partner_name"] == expected_name
            for a in run_data.get("applicants", [])
        )
        if found:
            print(f"   PASS: Applicant '{expected_name}' found in database")
        else:
            print(f"   FAIL: Expected applicant '{expected_name}' not found")
            print(f"   (The agent may have used different data or failed)")

        # Save a simple score
        score = {
            "applicant_found": found,
            "applicant_count": run_data["applicant_count"],
            "wall_clock_sec": wall_clock,
            "exit_code": result.returncode,
        }
        (OUTPUT_DIR / "score.json").write_text(json.dumps(score, indent=2))
        print()
        print(f"   Artifacts saved to {OUTPUT_DIR}/")
    else:
        print(f"   ERROR: Could not capture post-run state")
        print(f"   stdout: {capture_result.stdout[-500:]}")


def cmd_check(args: argparse.Namespace) -> None:
    """Inspect saved validation artifacts."""
    print(f"=== Phase 0 Validation: Check ===")
    print()

    for name in ("run_result.json", "score.json"):
        path = OUTPUT_DIR / name
        if path.exists():
            data = json.loads(path.read_text())
            print(f"{name}:")
            print(json.dumps(data, indent=2))
            print()
        else:
            print(f"{name}: not found (run 'validate.py run' first)")


def cmd_reproduce(args: argparse.Namespace) -> None:
    """Verify reproducibility: restore snapshot twice and compare pre-task state."""
    from benchmark.db import DatabaseManager

    db = DatabaseManager(db_user=args.db_user)
    print(f"=== Phase 0 Validation: Reproducibility Check ===")
    print()

    if SNAPSHOT_NAME not in db.list_snapshots():
        print(f"Snapshot '{SNAPSHOT_NAME}' not found. Run 'validate.py prepare' first.")
        return

    states = []
    for i in range(2):
        ep_db = f"benchmark_repro_{i}"
        print(f"Run {i+1}: Restoring snapshot -> {ep_db}...")
        db.restore_snapshot(SNAPSHOT_NAME, ep_db)

        # Read pre-task state
        check_code = """
import json
env = self.env
jobs = env['hr.job'].search_read(
    [('is_published', '=', True)],
    ['name', 'department_id'],
    order='name',
)
applicants = env['hr.applicant'].search_count([])
depts = env['hr.department'].search_read([], ['name'], order='name')
state = {
    'jobs': [{'name': j['name'], 'dept': j['department_id'][1] if j['department_id'] else None} for j in jobs],
    'applicant_count': applicants,
    'departments': [d['name'] for d in depts],
}
print('STATE_JSON:' + json.dumps(state, sort_keys=True))
"""
        result = subprocess.run(
            [
                ODOO_PYTHON, ODOO_BIN,
                "shell", "-c", str(ODOO_CONF),
                "-d", ep_db,
                "--no-http",
            ],
            input=check_code,
            capture_output=True, text=True,
            cwd=str(REPO_ROOT),
            timeout=60,
        )

        state = None
        for line in result.stdout.splitlines():
            if line.startswith("STATE_JSON:"):
                state = json.loads(line[len("STATE_JSON:"):])
                break

        if state:
            states.append(state)
            print(f"  Jobs: {[j['name'] for j in state['jobs']]}")
            print(f"  Applicants: {state['applicant_count']}")
            print(f"  Departments: {state['departments']}")
        else:
            print(f"  ERROR: Could not read state")
            states.append(None)

        # Cleanup
        db.drop_database(ep_db)

    print()
    if len(states) == 2 and states[0] and states[1]:
        if states[0] == states[1]:
            print("PASS: Pre-task states are identical across restores")
        else:
            print("FAIL: Pre-task states differ!")
            print(f"  Run 1: {json.dumps(states[0], indent=2)}")
            print(f"  Run 2: {json.dumps(states[1], indent=2)}")
    else:
        print("FAIL: Could not compare states")


def cmd_all(args: argparse.Namespace) -> None:
    """Run prepare + run + check in sequence."""
    cmd_prepare(args)
    print()
    print("=" * 60)
    print()

    # Start Odoo in background for the run
    print("Starting Odoo for benchmark run...")
    odoo_proc = subprocess.Popen(
        [
            ODOO_PYTHON, ODOO_BIN,
            "-c", str(ODOO_CONF),
            "-d", BENCHMARK_DB,
        ],
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for Odoo to start
    print("Waiting for Odoo to be ready...", end="", flush=True)
    for _ in range(60):
        try:
            import urllib.request
            urllib.request.urlopen(f"{BASE_URL}/web/login", timeout=2)
            print(" ready!")
            break
        except Exception:
            print(".", end="", flush=True)
            time.sleep(2)
    else:
        print(" TIMEOUT")
        odoo_proc.terminate()
        return

    print()
    try:
        cmd_run(args)
        print()
        print("=" * 60)
        print()
        cmd_check(args)
    finally:
        print()
        print("Stopping Odoo...")
        odoo_proc.terminate()
        try:
            odoo_proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            odoo_proc.kill()
        print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="benchmark/validate.py",
        description="Phase 0 end-to-end validation for the Odoo browser agent benchmark",
    )
    sub = parser.add_subparsers(dest="command")

    # Shared args
    for name in ("prepare", "reproduce", "all"):
        p = sub.add_parser(name)
        p.add_argument("--source-db", default="odoo_dev",
                       help="Source database to clone from")
        p.add_argument("--db-user", default="yangxiao",
                       help="PostgreSQL user")

    for name in ("run", "all"):
        p = sub.choices[name] if name in sub.choices else sub.add_parser(name)
        p.add_argument("--provider", default="dashscope",
                       help="LLM provider for browser-use")
        p.add_argument("--model", help="Model name override")
        p.add_argument("--headed", action="store_true",
                       help="Show the browser window")

    sub.add_parser("check")

    args = parser.parse_args()

    if args.command == "prepare":
        cmd_prepare(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "reproduce":
        cmd_reproduce(args)
    elif args.command == "all":
        cmd_all(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
