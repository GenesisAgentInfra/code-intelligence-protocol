# Code Intelligence Protocol

Public data formats for the standalone Genesis Code Intelligence product. The source Pydantic models and deterministic schema exporter live in the private `GenesisAgentInfra/code-intelligence` repository; generated JSON Schema files in this repository must not be edited by hand.

## Contents

- `schemas/v0.1.0/analysis-response.schema.json`: stable, user-readable Markdown/JSON report contract.
- `schemas/v0.2.0/analysis-response.schema.json`: opt-in report with source-backed business behavior comparisons; all v0.1.0 report fields remain.
- `schemas/v0.1.0/flows.schema.json`: machine-readable `.genesis/flows.yaml` contract.
- `specs/flows-yaml.md`: lifecycle and field semantics.
- `examples/v0.1.0/`: small, synthetic examples with no customer source.
- `examples/v0.2.0/behavior-comparison.json`: synthetic notification/wait comparison, including an explicitly incomplete scope.
- `specs/behavior-comparison.md`: scenario, side-specific evidence, coverage and version handling.

The four reports demonstrate a complete result, unresolved dynamic call, missing intent/tests, and stale flow entry. They are protocol examples, not evidence of analyzer accuracy.

Internal CLI-to-service requests, source excerpts, analysis facts, semantic service responses, API keys, and usage records are private implementation details and are not part of this public protocol.

The JSON Schema format is Draft 2020-12. Report schema, private request protocol, and flow-file schema have separate versions. Report completeness describes only declared analysis coverage; it does not mean a test passed or a change is approved.

The repository visibility is public. A license has not yet been selected; do not infer license grants from visibility.

## Validation

Run python scripts/validate_examples.py with jsonschema 4.x and PyYAML 6.x installed. GitHub Actions runs the same validation on pushes and pull requests via .github/workflows/validate.yml.
