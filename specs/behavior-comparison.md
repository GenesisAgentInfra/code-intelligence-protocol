# Business behavior comparisons

Report v0.2.0 adds the required `behavior_review` object to all fields of v0.1.0. The original five sections, findings, estimates, verification suggestions and limitations remain. The comparison is semantic inference from frozen source, not a user requirement, runtime observation or test result.

`behavior_review.version` is `1`. `coverage` uses the same status/reason/analyzed-scope structure as section coverage. `changes` contains at most 12 comparisons. An empty array may mean no supported comparison was produced; read coverage and the five sections before inferring safety or absence of change.

Each comparison contains:

| Field | Meaning |
| --- | --- |
| `change_id` | Unique within the report |
| `scenario`, `condition` | Concrete use case and trigger under which the explanation applies |
| `before`, `after` | Source-backed behavior of each revision, or `null` when that side cannot be described |
| `before_evidence_ids`, `after_evidence_ids` | Selected code evidence belonging to base or head respectively |
| `explanation`, `impact` | Why the connected code changes the behavior, and the observable consequence |
| `preserved_behavior` | Relevant behavior that remains, or `null` when no supported statement is available |
| `evidence_ids` | Evidence supporting the explanation, including at least one code reference |
| `finding_ids` | Existing local/semantic findings in the same report; may be empty |
| `limitations` | Missing links, conditional assumptions and unresolved scope |

A described side needs nonempty side-specific references. At least one side must be described. An unavailable side needs an explicit limitation; absence of a selected excerpt does not prove absence of code or behavior. Source references retain the report snapshot, side, path, range and digest identity. Finding references cannot introduce findings that are absent from the report.

Some constraints (reference existence, side and kind, unique change IDs, finding linkage) require semantic validation in addition to JSON Schema. A `complete` report also requires analyzed comparison coverage, every original section analyzed, and no completeness-affecting limitations. Partial comparisons still retain supported changes. These checks do not prove a natural-language claim is correct.

The concise and detailed Markdown reports are deterministic presentations of this same object. Neither renderer generates a second model answer. Internal AST/behavior-unit formats are intentionally separate from this public report contract.

The synthetic example describes an asynchronous notification added between submitting a report and returning its result. Its scope is partial because the caller and notification implementation are absent. It demonstrates the format, not measured analyzer accuracy.
