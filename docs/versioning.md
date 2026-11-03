# Versioning

The public report JSON Schema uses semantic version strings in `schema_version`. The `.genesis/flows.yaml` format uses an integer `schema_version` because its format evolves independently. The private CLI-to-service `protocol_version` is maintained in the implementation repository and is not implied by either public format.

The private Pydantic models are the sole source of generated schemas. Changes to a public model require regenerated schemas and example validation in the same change. Changes to internal request/response models require updating the private protocol notes and fixed fixtures. The first implementation accepts an exact version match; compatibility negotiation is deferred until there is a released client and service.
