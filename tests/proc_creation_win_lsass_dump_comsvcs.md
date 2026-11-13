# Test record: LSASS Memory Dump via comsvcs.dll MiniDump

| Field | Value |
|---|---|
| Rule | `rules/windows/process_creation/proc_creation_win_lsass_dump_comsvcs.yml` |
| ATT&CK | T1003.001 OS Credential Dumping: LSASS Memory |
| Atomic test | T1003.001 "Dump LSASS.exe Memory using comsvcs.dll" |
| Telemetry | Sysmon Event ID 1 / Elastic Defend process events |
| Tested on | _Windows 10/11 build, date_ |
| Result | _Pending: Detected / Missed / Partial_ |

## Run it
```powershell
Invoke-AtomicTest T1003.001 -ShowDetailsBrief        # find the comsvcs test number
Invoke-AtomicTest T1003.001 -TestNumbers <N> -GetPrereqs
Invoke-AtomicTest T1003.001 -TestNumbers <N>
Invoke-AtomicTest T1003.001 -TestNumbers <N> -Cleanup
```
Defender/Elastic Defend will likely block this. Use a detect-only policy in the lab, or log the block as a separate finding.

## Evidence
- Screenshot of the alert in Kibana: `docs/img/lsass_comsvcs_alert.png`
- Matching raw event (sanitized command line):

## Tuning notes
- False positives seen during a 7-day baseline:
- Exclusions added (and why):

## Gaps / bypasses
- Renamed rundll32 is covered by `OriginalFileName`. Renamed comsvcs.dll copied elsewhere is not. Consider an image-load (Sysmon EID 7) rule as a follow-up.
