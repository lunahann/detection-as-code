# Detection-as-Code Portfolio

Vendor-neutral detections written in [Sigma](https://sigmahq.io), automatically validated and
converted to **Elastic (Lucene, EQL, ES|QL)** and **Microsoft Defender XDR (KQL)**, and tested
against real adversary behavior using **Atomic Red Team** in a home lab.

## Coverage

| Rule | ATT&CK | Level | Tested |
|---|---|---|---|
| LSASS Memory Dump via comsvcs.dll | T1003.001 | high | ☐ |
| PowerShell Encoded Command | T1059.001, T1027 | medium | ☐ |
| Run Key Persistence via reg.exe | T1547.001 | medium | ☐ |

## Pipeline

```
Sigma rule (rules/) ──► sigma check ──► metadata gate ──► convert ──► build/ artifact
                                                            ├─ Elastic Lucene / EQL / ES|QL
                                                            ├─ Kibana import bundle (.ndjson)
                                                            └─ Defender XDR KQL
```
Every push and PR runs `.github/workflows/detections.yml`. A rule can't merge unless it passes
Sigma validation, has an ATT&CK tag and false-positive notes, and has a test record in `tests/`.

## Detection lifecycle

1. **Hypothesis:** pick an ATT&CK technique and the telemetry that would show it.
2. **Write:** add a Sigma rule under `rules/` and a test record under `tests/` with the same filename.
3. **Validate:** open a PR. CI checks syntax and metadata, then converts.
4. **Test:** run the matching Atomic Red Team test in the lab and confirm the alert fires.
5. **Tune:** baseline for false positives, document exclusions, then promote `status` from `experimental` to `test` to `stable`.
6. **Document gaps:** note the bypasses the rule doesn't cover, and the follow-up rule that would.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
sigma check rules/
python scripts/validate_metadata.py
bash scripts/convert.sh
```

## Lab

- **SIEM:** Elastic Stack in Docker, with Fleet + Elastic Defend set to *detect only*
- **Endpoint:** Windows 10/11 VM with Sysmon (SwiftOnSecurity or Olaf Hartong config) and Elastic Agent
- **Emulation:** Invoke-AtomicRedTeam on the Windows VM. Snapshot before every test.

All data in this repo comes from my own lab. No production or employer data.
