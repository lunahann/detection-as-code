# Test record: PowerShell Execution With Encoded Command

| Field | Value |
|---|---|
| Rule | `rules/windows/process_creation/proc_creation_win_powershell_encoded_command.yml` |
| ATT&CK | T1059.001 PowerShell, T1027 Obfuscated Files or Information |
| Atomic test | T1059.001, pick a test that uses `-EncodedCommand` / `-e` |
| Telemetry | Sysmon Event ID 1 / Elastic Defend process events |
| Tested on | _Windows build, date_ |
| Result | _Pending_ |

## Run it
```powershell
Invoke-AtomicTest T1059.001 -ShowDetailsBrief
Invoke-AtomicTest T1059.001 -TestNumbers <N>
```
Manual check:
```powershell
$c = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes('whoami'))
powershell.exe -NoProfile -EncodedCommand $c
```

## Evidence
- Alert screenshot:
- Raw event:

## Tuning notes
- Expect noise from management agents. Record the parent processes you saw, then exclude by `ParentImage` rather than dropping the rule.

## Gaps / bypasses
- Caret or quote insertion inside the flag (e.g. `-e^nc`) may evade `contains`. Pair with Script Block Logging (EID 4104) detections.
