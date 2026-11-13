# Test record: Run Key Persistence Added via reg.exe

| Field | Value |
|---|---|
| Rule | `rules/windows/process_creation/proc_creation_win_reg_add_run_key.yml` |
| ATT&CK | T1547.001 Registry Run Keys / Startup Folder |
| Atomic test | T1547.001 "Reg Key Run" |
| Telemetry | Sysmon Event ID 1 / Elastic Defend process events |
| Tested on | _Windows build, date_ |
| Result | _Pending_ |

## Run it
```powershell
Invoke-AtomicTest T1547.001 -ShowDetailsBrief
Invoke-AtomicTest T1547.001 -TestNumbers <N>
Invoke-AtomicTest T1547.001 -TestNumbers <N> -Cleanup
```

## Evidence
- Alert screenshot:
- Raw event:

## Tuning notes
- Installers create Run values constantly. Baseline the value names, then exclude known-good ones.

## Gaps / bypasses
- Run keys set via PowerShell `Set-ItemProperty`, the .NET API, or `regedit /s` don't spawn reg.exe. Follow-up: a `registry_set` rule (Sysmon EID 13) covers every writer.
