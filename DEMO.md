# Runnable demo

```bash
python demo.py
python systemd_order_audit.py example.json
```

`demo.py` checks a synthetic success and malformed-input rejection. The installed command uses the same arguments.

## Input contract

```text
{
  "roots": [
    "app.service"
  ],
  "units": {
    "app.service": {
      "after": [
        "db.service"
      ],
      "before": [],
      "requires": [
        "db.service"
      ],
      "wants": []
    },
    "db.service": {
      "after": [],
      "before": [],
      "requires": [],
      "wants": []
    }
  }
}
```

Inspect `test_contract.py` for independently specified expected outcomes, including boundary failures. Normalized JSON snapshot, not a unit-file parser or replacement for systemd-analyze verify. No default/implicit dependencies, drop-ins, generators, aliases, conditions, failure propagation, stop ordering or live system operations. Missing pull-ins make complete false; inactive ordering targets are explicit. Blocked includes descendants of cycles, not just cycle members.
