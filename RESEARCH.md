# Candidate brief and fair comparison — 11 October 2026

**User:** Linux service authors reviewing an explicit startup transaction offline. **Painful task:** Requires/Wants pull in units but do not order them; After/Before order units but do not pull them in.

**Current alternatives:** systemd-analyze verify/dot, systemd-graph and SystemdGenie. **Smallest useful capability:** Expand explicit pull-ins from roots, separately construct ordering edges and return one concrete cycle or deterministic topological order.

**Demand evidence:** inferred from the documented protocol/workflow and established comparable projects, not a verified request for this new product. Current comparable READMEs, representative implementation/docs and recent issue/PR lists were reviewed. Those issues do not prove demand for our feature, and no competitor absence is asserted. See [portfolio research evidence](https://github.com/nripankadas07/nripankadas07/blob/main/docs/RESEARCH_2026-10-11.json) for exact observations and code/doc URLs.

**Acceptance:** the 16 core contract tests must pass, the demo must check its known output and malformed input, and a clean installed command outside source must reproduce both success and error behavior. Scope limits remain visible in README/output. LIVE additionally requires final default-branch CI and verified docs/install path.

**Discovery:** descriptive GitHub topics, the profile chronological index, and a reproducible linked demo. No promised growth, invented users or unsolicited third-party issue promotion.

**Distinctness:** compared with all 158 existing owned repository names and today's other four briefs. Cookie routing is separate from CSP/cache/robots checks; SOA rollout arithmetic is separate from mail DNS topology and DNS blocking; expression alternatives are separate from SBOM inventory/dependency audits; startup pull-in versus ordering is separate from general migration plans; captured packet accounting is separate from live LAN delivery/network discovery. These are five independent capabilities, not subdivisions of one product.

## Live GitHub research

Queries: `systemd dependencies sort:stars`, `systemd sort:stars`, `systemd graph sort:stars`. Observation date 2026-10-11 UTC. GitHub query results were relevance-screened; some broad queries include unrelated repositories. Highest-star relevant comparable **found** in this research: [systemd/systemd](https://github.com/systemd/systemd) (16815 stars). Coverage is limited; this is not an exhaustive global ranking. Additional established tools were inspected directly. Stars are discovery evidence, not performance.

| Comparable | Stars | Latest push observed (UTC) | Documented workflow |
| --- | ---: | --- | --- |
| [systemd/systemd](https://github.com/systemd/systemd) | 16815 | 2026-10-11T05:44:23Z | The systemd System and Service Manager  |
| [icholy/systemd-graph](https://github.com/icholy/systemd-graph) | 11 | 2026-09-10T23:59:14Z | A web ui for a live view the SystemD unit dependency graph |
| [KDE/systemdgenie](https://github.com/KDE/systemdgenie) | 84 | 2026-10-11T02:33:22Z | Systemd managment utility |

## Workflow tradeoffs

Established alternatives have broader capabilities, documentation, examples and ecosystems; installability varies by language and platform. Ours offers a narrow one-command synthetic example and a zero-runtime-dependency Python source install. No competitor installation was timed or independently stress-tested in this run. No measured time-to-first-result, reliability, support responsiveness, performance or superiority claim. Current comparable licenses are recorded in linked research metadata; none of their implementation or prose was reused. Our license is MIT. Support is best-effort GitHub reports with no SLA.

**Limits and negative result:** Normalized JSON snapshot, not a unit-file parser or replacement for systemd-analyze verify. No default/implicit dependencies, drop-ins, generators, aliases, conditions, failure propagation, stop ordering or live system operations. Missing pull-ins make complete false; inactive ordering targets are explicit. Blocked includes descendants of cycles, not just cycle members. Broader production needs should use the established tools. Runnable local success demonstrates our behavior only.
