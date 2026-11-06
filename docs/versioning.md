# Versioning

The public report JSON Schema uses semantic version strings in `schema_version`. The `.genesis/flows.yaml` format uses an integer `schema_version` because its format evolves independently. The private CLI-to-service `protocol_version` is maintained in the implementation repository and is not implied by either public format.

The private Pydantic models are the sole source of generated schemas. Changes to a public model require regenerated schemas and example validation in the same change. Changes to internal request/response models require updating the private protocol notes and fixed fixtures.

Report v0.1.0 is retained unchanged. A report with a structured `behavior_review` uses v0.2.0, preserving every original report field. Consumers must dispatch on `schema_version` and validate against that exact version; do not feed v0.2.0 into the strict v0.1.0 schema. The implementation's `parse_analysis_response()` accepts both. Flow files still use schema 1. The private HTTP protocol negotiates optional behavior features independently; an older client continues to receive the legacy report content. Public schemas describe report artifacts, not wire service requests.
