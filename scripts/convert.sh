#!/usr/bin/env bash
# Convert every Sigma rule into Elastic (Lucene, EQL, ES|QL) and Microsoft Defender XDR KQL.
# Output lands in build/<target>/<rule>.txt plus a Kibana-importable NDJSON bundle.
set -euo pipefail

cd "$(dirname "$0")/.."
rm -rf build && mkdir -p build/lucene build/eql build/esql build/kql

shopt -s globstar nullglob
rules=(rules/**/*.yml)
[ ${#rules[@]} -gt 0 ] || { echo "No rules found"; exit 1; }

for rule in "${rules[@]}"; do
  name=$(basename "$rule" .yml)
  echo "Converting $name"
  sigma convert -t lucene -p ecs_windows "$rule" > "build/lucene/$name.txt"
  sigma convert -t eql    -p ecs_windows "$rule" > "build/eql/$name.txt"
  # ecs_windows isn't registered for the esql target, but the ECS field mapping is identical.
  sigma convert -t esql   -p ecs_windows --disable-pipeline-check "$rule" > "build/esql/$name.txt"
  sigma convert -t kusto  -p microsoft_xdr "$rule" > "build/kql/$name.txt"
done

# One file you can import into Kibana: Security > Rules > Import
sigma convert -t lucene -p ecs_windows -f siem_rule_ndjson rules/ > build/elastic_security_rules.ndjson

echo "Done. Output in build/"
