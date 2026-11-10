# Code Intelligence Protocol

Public data formats for the standalone Genesis Code Intelligence product. The source Pydantic models and deterministic schema exporter live in the public `GenesisAgentInfra/genesis-cli` repository; generated JSON Schema files in this repository must not be edited by hand.

## Contents

- `schemas/v0.1.0/analysis-response.schema.json`: stable, user-readable Markdown/JSON report contract.
- `schemas/v0.3.0/analysis-response.schema.json`: opt-in report with revision-specific, evidence-backed semantic execution paths.
- `schemas/v0.2.0/analysis-response.schema.json`: opt-in report with source-backed business behavior comparisons; all v0.1.0 report fields remain.
- `schemas/v0.1.0/flows.schema.json`: machine-readable `.genesis/flows.yaml` contract.
- `specs/flows-yaml.md`: lifecycle and field semantics.
- `examples/v0.1.0/`: small, synthetic examples with no customer source.
- `examples/v0.2.0/behavior-comparison.json`: synthetic notification/wait comparison, including an explicitly incomplete scope.
- `specs/behavior-comparison.md`: scenario, side-specific evidence, coverage and version handling.

The four reports demonstrate a complete result, unresolved dynamic call, missing intent/tests, and stale flow entry. They are protocol examples, not evidence of analyzer accuracy.

The open-source CLI implements local extraction and API delivery; the hosted semantic service is maintained separately. CLI-to-service request internals are not a stable public report contract. Customer source excerpts, API keys and usage records are confidential and do not belong in this repository.

Start with [genesis-cli](https://github.com/GenesisAgentInfra/genesis-cli) for installation and usage. This repository documents data formats.

The JSON Schema format is Draft 2020-12. Report schema, private request protocol, and flow-file schema have separate versions. Report completeness describes only declared analysis coverage; it does not mean a test passed or a change is approved.

The repository visibility is public. A license has not yet been selected; do not infer license grants from visibility.

## Validation

Run python scripts/validate_examples.py with jsonschema 4.x and PyYAML 6.x installed. GitHub Actions runs the same validation on pushes and pull requests via .github/workflows/validate.yml.
