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


## Report v0.3.0: semantic execution paths

Report v0.3.0 retains all original report fields and comparisons, sets
`behavior_review.version` to `2`, and requires `paths` (0–6 entries). v0.1.0 and
v0.2.0 are unchanged. Consumers should dispatch on `schema_version`.

Each path has a unique `path_id`, a single `side` (`base` or `head`), scenario,
condition, steps (1–12), links (0–16), optional outcome and limitations. A step has
an ID, kind, description, selected code evidence and an optional `path#symbol`
location. Links reference existing step IDs and include a relation, optional
condition, evidence, `support` and limitations. Step IDs are unique within a path.
Every step/link cites code of that path's revision. A symbol's path must match
its code evidence. These constraints need semantic validation beyond JSON Schema.

`support=semantic_inference` means a connection inferred from supplied code, not
a resolved static edge or observed execution. `support=unknown` requires an
explicit missing-link limitation. An unknown entry is `entry_step_id=null` with
a limitation; an unknown outcome remains `null`. No complete entry or successful
return is invented to connect fragments. Registration and method names alone do
not prove runtime selection. Static graphs remain separate.

Paths explain the same analysis and do not replace findings, changes, cost,
verification or coverage. Empty paths do not imply the application has no flows.
The synthetic [example](../examples/v0.3.0/execution-paths.json) illustrates this
format without customer source or runtime measurements.
