#!/usr/bin/env python3
"""Portfolio quality gate: every rule must meet house standards beyond basic Sigma syntax.

Checks per rule:
  - required fields present (title, id, description, author, date, tags, falsepositives, level)
  - at least one ATT&CK technique tag (attack.tNNNN)
  - unique rule id across the repo
  - a matching test record in tests/<rule_filename>.md
Exit code 1 on any failure so CI blocks the merge.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "rules"
TESTS = ROOT / "tests"
REQUIRED = ["title", "id", "description", "author", "date", "tags", "falsepositives", "level", "logsource", "detection"]
TECHNIQUE = re.compile(r"^attack\.t\d{4}(\.\d{3})?$")

errors = []
seen_ids = {}

rule_files = sorted(RULES.rglob("*.yml"))
if not rule_files:
    print("No rules found under rules/")
    sys.exit(1)

for path in rule_files:
    rel = path.relative_to(ROOT)
    try:
        rule = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        errors.append(f"{rel}: YAML parse error: {e}")
        continue

    for field in REQUIRED:
        if not rule.get(field):
            errors.append(f"{rel}: missing '{field}'")

    tags = rule.get("tags") or []
    if not any(TECHNIQUE.match(t) for t in tags):
        errors.append(f"{rel}: no ATT&CK technique tag (e.g. attack.t1003.001)")

    rid = rule.get("id")
    if rid in seen_ids:
        errors.append(f"{rel}: duplicate id {rid} (also in {seen_ids[rid]})")
    seen_ids[rid] = rel

    test_doc = TESTS / f"{path.stem}.md"
    if not test_doc.exists():
        errors.append(f"{rel}: missing test record tests/{path.stem}.md")

if errors:
    print("Metadata validation FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"Metadata validation passed for {len(rule_files)} rule(s).")
