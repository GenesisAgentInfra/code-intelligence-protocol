# Flow Map Format v1

The flow map is a user-maintained `.genesis/flows.yaml` file at the repository root. It gives stable names to business entry points and stores acceptance statements supplied by the user. It is versioned alongside the analyzed code.

```yaml
schema_version: 1
flows:
  - id: submit-report
    name: Submit report
    status: confirmed
    entries:
      - src/report/submit.py#submit_report
    acceptance:
      - A rejected submission does not send a success notification
    notes: A third-party response with success=false is a business failure
```

`schema_version` is the integer `1`. Flow IDs are unique lowercase kebab-case identifiers. `entries` contains one or more repository-relative `path#symbol` references; line numbers are deliberately excluded so routine edits do not invalidate the map. `acceptance` contains plain-language criteria written or confirmed by a user. An analyzer may propose entry points, names, and descriptions, but it must not infer acceptance criteria from existing code.

`draft` entries are provisional grouping hints. Their acceptance list must be empty. Confirm the flow before entering acceptance criteria; the runtime validator rejects nonempty acceptance on drafts. Only `confirmed` entries contribute acceptance statements as user intent. A missing or stale entry is reported; the analyzer never edits this file automatically.

Flow mapping is static reachability within the analyzer's supported syntax. It does not claim that the flow ran or that calls happen in a particular runtime order. Unresolved dynamic calls remain unknown.

JSON Schema checks structure; unique IDs, safe repository paths, and draft lifecycle rules additionally require semantic validation. The reference implementation enforces these rules.
