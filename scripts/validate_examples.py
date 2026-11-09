"""Validate public artifacts without access to the private implementation."""
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def main():
    validators = {}
    for name in ("analysis-response", "flows"):
        schema = json.loads((ROOT / "schemas/v0.1.0" / (name + ".schema.json")).read_text())
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema)
    reports = sorted((ROOT / "examples/v0.1.0").glob("*.json"))
    assert len(reports) == 4
    for path in reports:
        report = json.loads(path.read_text())
        validators["analysis-response"].validate(report)
        assert report["scope"]["execution_mode"] == "mock"
        assert "excerpts" not in report and "facts" not in report and "api_key" not in report
        refs = {item["evidence_id"] for item in report["evidence"]}
        assert len(refs) == len(report["evidence"])
        assert all(item["snapshot_id"] == report["snapshot_id"] for item in report["evidence"])
        def check_refs(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key.endswith("evidence_ids"):
                        assert set(child) <= refs
                    else:
                        check_refs(child)
            elif isinstance(value, list):
                for child in value:
                    check_refs(child)
        check_refs(report)
        if report["analysis_status"] == "complete":
            assert all(section["status"] == "analyzed" for section in report["section_status"].values())
            assert not any(item["affects_completeness"] for item in report["limitations"])
    comparison_schema = json.loads((ROOT / "schemas/v0.2.0/analysis-response.schema.json").read_text())
    Draft202012Validator.check_schema(comparison_schema)
    comparison_reports = sorted((ROOT / "examples/v0.2.0").glob("*.json"))
    assert comparison_reports
    for path in comparison_reports:
        report = json.loads(path.read_text())
        Draft202012Validator(comparison_schema).validate(report)
        assert report["scope"]["execution_mode"] == "mock"
        refs = {item["evidence_id"]: item for item in report["evidence"]}
        findings = {item["finding_id"] for item in report["findings"]}
        changes = report["behavior_review"]["changes"]
        assert len({change["change_id"] for change in changes}) == len(changes)
        for change in changes:
            assert set(change["finding_ids"]) <= findings
            for label, side in (("before", "base"), ("after", "head")):
                ids = change[label + "_evidence_ids"]
                assert (change[label] is not None) == bool(ids)
                assert all(refs[ident]["kind"] == "code" and refs[ident]["side"] == side for ident in ids)
            assert set(change["evidence_ids"]) <= refs.keys()
            assert any(refs[ident]["kind"] == "code" for ident in change["evidence_ids"])
            assert change["before"] is not None or change["after"] is not None
            assert (change["before"] is not None and change["after"] is not None) or change["limitations"]
        if report["analysis_status"] == "complete":
            assert report["behavior_review"]["coverage"]["status"] == "analyzed"
    path_schema = json.loads((ROOT / "schemas/v0.3.0/analysis-response.schema.json").read_text())
    Draft202012Validator.check_schema(path_schema)
    path_reports = sorted((ROOT / "examples/v0.3.0").glob("*.json"))
    assert path_reports
    for path in path_reports:
        report = json.loads(path.read_text())
        Draft202012Validator(path_schema).validate(report)
        assert report["scope"]["execution_mode"] == "mock"
        refs = {ref["evidence_id"]: ref for ref in report["evidence"]}
        paths = report["behavior_review"]["paths"]
        assert len({item["path_id"] for item in paths}) == len(paths)
        for item in paths:
            steps = {step["step_id"]: step for step in item["steps"]}
            assert len(steps) == len(item["steps"])
            assert item["entry_step_id"] in steps or (item["entry_step_id"] is None and item["limitations"])
            for node in [*item["steps"], *item["links"]]:
                assert all(refs[ident]["side"] == item["side"] and refs[ident]["kind"] == "code" for ident in node["evidence_ids"])
            for step in item["steps"]:
                if step["symbol"] is not None:
                    assert "#" in step["symbol"]
                    assert any(refs[ident]["path"] == step["symbol"].split("#", 1)[0] for ident in step["evidence_ids"])
            for link in item["links"]:
                assert link["source"] in steps and link["target"] in steps
                assert link["support"] != "unknown" or link["limitations"]
    flows = yaml.safe_load((ROOT / "examples/v0.1.0/flows.yaml").read_text())
    validators["flows"].validate(flows)
    assert len({flow["id"] for flow in flows["flows"]}) == len(flows["flows"])
    assert all(not flow.get("acceptance") for flow in flows["flows"] if flow["status"] == "draft")
    print(f"Validated {len(reports)} public report examples and one flow map")


if __name__ == "__main__":
    main()
