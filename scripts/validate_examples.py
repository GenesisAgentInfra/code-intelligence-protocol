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
    flows = yaml.safe_load((ROOT / "examples/v0.1.0/flows.yaml").read_text())
    validators["flows"].validate(flows)
    assert len({flow["id"] for flow in flows["flows"]}) == len(flows["flows"])
    assert all(not flow.get("acceptance") for flow in flows["flows"] if flow["status"] == "draft")
    print(f"Validated {len(reports)} public report examples and one flow map")


if __name__ == "__main__":
    main()
