# systemd-order-audit

Expand explicit pull-ins from roots, separately construct ordering edges and return one concrete cycle or deterministic topological order.

For linux service authors reviewing an explicit startup transaction offline. Requires/Wants pull in units but do not order them; After/Before order units but do not pull them in.

## Quickstart

Python 3.10 or newer. No runtime dependencies or service account. Build tooling downloads require access to PyPI; this repository is not published on PyPI.

```bash
git clone https://github.com/nripankadas07/systemd-order-audit.git
cd systemd-order-audit
python -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/systemd-order-audit example.json
```

Windows: use `.venv\Scripts\python.exe` and `.venv\Scripts\systemd-order-audit.exe` instead. Windows is not part of the tested CI matrix.

The supplied example is synthetic. JSON success exits 0, including valid findings such as unmet quorum, ineligible cookie or an ordering cycle; malformed or unsupported input exits 2 with an `error` field. Argument usage errors use argparse's stderr. No input files or live services are modified.

## Scope and limits

Normalized JSON snapshot, not a unit-file parser or replacement for systemd-analyze verify. No default/implicit dependencies, drop-ins, generators, aliases, conditions, failure propagation, stop ordering or live system operations. Missing pull-ins make complete false; inactive ordering targets are explicit. Blocked includes descendants of cycles, not just cycle members.

Input limits: 1 MiB JSON; 1..500 unit records, each relation list at most 500 names.

## Inspectable evidence

- [Demo and input schema](DEMO.md)
- [Candidate brief and comparisons](RESEARCH.md)
- [Validation and untested behavior](VALIDATION.md)
- [Build instructions](BUILDING.md)
- [Security reporting](SECURITY.md) and [support/contribution guidance](SUPPORT.md)

MIT; original implementation. No competitor code or branding copied. No speed, adoption or superiority claim. CI executes core regressions, the demo, a fresh wheel installation outside source and the documented source installation on Python 3.10, 3.12 and 3.14.
