# Ledger

**Ledger: A Path-Validated, Database-Grounded Benchmark for Enterprise Web Agents**
NeurIPS 2026, Evaluations and Datasets Track

Xiao Yang, Mo Sha, Yiran Li, Chengjin Tian, Sheng Wang, Fangyuan Zhou, Feifei Li

[Paper on OpenReview](https://openreview.net/forum?id=LUGEM2rYcv) ·
[NeurIPS paper page](https://neurips.cc/virtual/2026/loc/paris/poster/139511) ·
[Dataset: 10.7910/DVN/0YVNZM](https://doi.org/10.7910/DVN/0YVNZM)

Ledger evaluates browser agents on **424 fixed tasks across 54 functional
modules** of Odoo Community 19.0. Each episode restores a PostgreSQL snapshot,
seeds a synthetic enterprise workflow, and evaluates database changes and
server-side operation traces against task-specific oracles.

This repository contains the evaluation harness, task bundles, agent wrappers,
`benchmark_trace` addon, and the Odoo source needed to run them. The archived
dataset contains the task manifest, task archive, base snapshot, checksums,
Croissant metadata, and provenance documentation.

## Installation

Use Python 3.11–3.13, `uv`, Git, and a running local PostgreSQL 14+ installation
with `psql`, `createdb`, `dropdb`, `pg_dump`, and `pg_restore` on `PATH`.
The archived snapshot was produced with PostgreSQL 14.19. Some Odoo Python
packages require platform-specific build dependencies; see the
[Odoo source-install guide](https://www.odoo.com/documentation/19.0/administration/on_premise/source.html).
Node.js and additional agent dependencies are only needed for the relevant
wrappers.

```bash
git clone https://github.com/softpudding/odoo_browser_benchmark.git
cd odoo_browser_benchmark
git checkout v1.0
uv sync --frozen
uv pip install --python .venv/bin/python -r requirements.txt
uv run playwright install chromium
```

Create `.odoorc.local` in the repository root, replacing the two placeholders:

```ini
[options]
addons_path = /absolute/path/to/odoo_browser_benchmark/addons,/absolute/path/to/odoo_browser_benchmark/odoo/addons
db_user = your_postgres_role
http_interface = 127.0.0.1
http_port = 8069
data_dir = /absolute/path/to/odoo_browser_benchmark/.odoo-data
without_demo = True
```

Use a local PostgreSQL role that can create databases. Set `PGUSER` to the same
role as `db_user`; the harness's PostgreSQL command-line tools use `PGUSER`.
If required, configure `PGHOST`/`PGPORT` and the matching Odoo settings as well.
The benchmark's default synthetic Odoo login is `admin` / `admin`.

## Prepare the base snapshot

To use the archived dataset, download `snapshots/benchmark_base.dump` and
`snapshots/benchmark_base.sha256` from
[Dataverse](https://doi.org/10.7910/DVN/0YVNZM). In the download's `snapshots/`
directory, verify the checksum with `sha256sum -c benchmark_base.sha256`
(or `shasum -a 256 -c benchmark_base.sha256` on macOS). From the repository root,
point the harness at that directory:

```bash
export PGUSER=your_postgres_role
export BENCHMARK_SNAPSHOT_DIR=/absolute/path/to/download/snapshots
```

Alternatively, after installation and PostgreSQL configuration, build a new
base database from the repository's pinned module list:

```bash
uv run benchmark-eval bootstrap-base
```

The default snapshot directory is `/tmp/benchmark_snapshots`. Bootstrap refuses
to overwrite an existing base database unless `--rebuild` is supplied. Rebuilt
PostgreSQL dumps need not be byte-identical to the archived snapshot; use the
archived dump for its exact starting state.

## Run and score tasks

```bash
# Discover tasks and command options
uv run benchmark-eval list
uv run benchmark-eval run --help

# Run the packaged Playwright oracle without an LLM API key
uv run benchmark-eval run sale.change_validity_date --agent oracle \
  --output-dir /tmp/ledger-oracle

# Perform an author-style manual walkthrough
uv run benchmark-eval run sale.change_validity_date --agent human

# Re-score saved artifacts
uv run benchmark-eval score /tmp/ledger-oracle \
  --task-dir benchmark/tasks/sale.change_validity_date
```

For browser-use, install its optional dependency into the Odoo environment,
provide a model API key through the environment, and run:

```bash
uv pip install --python .venv/bin/python browser-use
export DASHSCOPE_API_KEY=your_api_key
uv run benchmark-eval run sale.change_validity_date \
  --agent browser-use --provider dashscope --model qwen3.6-plus \
  --max-steps 60 --output-dir /tmp/ledger-browser-use
```

The runner creates an isolated database and Odoo server for each episode by
default. Outputs include `score.json`, state differences, and operation traces.
An agent's own completion message is not the benchmark verdict.

See [benchmark setup](benchmark/AGENTS.md) for further commands,
[agent wrappers](benchmark/agents/README.md) for third-party agent installation
and provider configuration, and [evaluation records](benchmark/reports/README.md)
for the scope of the archived runs. `human_eval/` holds limited author QA
records, not a human-performance baseline. Historical queues include retries
and should not be treated as one-row-per-task result tables.

## Citation

```bibtex
@inproceedings{yang2026ledger,
 author = {Yang, Xiao and Sha, Mo and Li, Yiran and Tian, Chengjin and Wang, Sheng and Zhou, Fangyuan and Li, Feifei},
 booktitle = {Advances in Neural Information Processing Systems},
 title = {Ledger: A Path-Validated, Database-Grounded Benchmark for Enterprise Web Agents},
 year = {2026}
}
```

Please also cite the dataset DOI
[10.7910/DVN/0YVNZM](https://doi.org/10.7910/DVN/0YVNZM), using Dataverse's
**Cite Dataset** action for the version you used.

## Licenses and upstream Odoo

The code in this repository remains under the existing
[LGPL-3.0 license](LICENSE), including the evaluation harness and
`addons/benchmark_trace`. No separate MIT license is added to `benchmark/`.
Third-party dependencies retain their own licenses.

The Dataverse dataset has asset-specific terms: synthetic task bundles and
dataset metadata/documentation are distributed under MIT; the Odoo-derived
PostgreSQL snapshot is distributed under LGPL-3.0. See the dataset's
`LICENSES.md` and terms for the authoritative asset list.

Odoo copyright and license notices are preserved. The original upstream
project introduction is available in [README.odoo.md](README.odoo.md).
