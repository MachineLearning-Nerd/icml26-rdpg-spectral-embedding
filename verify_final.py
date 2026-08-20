#!/usr/bin/env python3
"""Verify the published RDPG audit contract without rerunning experiments."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_IDENTITY = (
    "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
)
EXPECTED_STATUS = (
    "INCONCLUSIVE_C1_C3_C4_C5_C6_FINITE_DIAGNOSTICS_VERIFIED_"
    "C2_FINITE_CHECK_FAILED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE"
)
EXPECTED_RECOVERY_SHA = (
    "3e03b531bc13549fcdb57b07eadf7725c0d9b6d0347d89aaeb794ab29841ff8a"
)


def fail(reason: str) -> None:
    print("FINAL_AUDIT=FAILED reason=" + reason)
    raise SystemExit(1)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("git_" + "_".join(args))
    return result.stdout.strip()


def load(relative_path: str) -> dict:
    try:
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(relative_path + "_invalid_" + type(error).__name__)
    raise AssertionError("unreachable")


branches = {
    line
    for line in git(
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:short)",
    ).splitlines()
    if line
}
if branches != {"main"}:
    fail("branches_" + ",".join(sorted(branches)))
if git("branch", "--show-current") != "main":
    fail("head_not_main")

all_refs = git(
    "for-each-ref",
    "--format=%(refname)",
).splitlines()
if any(
    ref.endswith("/master") or "/orx/" in ref
    for ref in all_refs
):
    fail("legacy_branch_ref")

commit_count = int(git("rev-list", "--count", "--all"))
if commit_count != 4:
    fail("commit_count_" + str(commit_count))

identity_rows = git(
    "log",
    "--all",
    "--format=%an <%ae>|%cn <%ce>",
).splitlines()
expected_row = EXPECTED_IDENTITY + "|" + EXPECTED_IDENTITY
if not identity_rows or any(row != expected_row for row in identity_rows):
    fail("noncanonical_commit_identity")

claims_doc = load("claims.json")
claims = {claim["id"]: claim for claim in claims_doc["claims"]}
expected_claims = {
    "C1": "VERIFIED_FINITE_DIAGNOSTIC",
    "C2": "FINITE_CHECK_FAILED",
    "C3": "VERIFIED_FINITE_DIAGNOSTIC",
    "C4": "VERIFIED_FINITE_DIAGNOSTIC",
    "C5": "VERIFIED_FINITE_DIAGNOSTIC",
    "C6": "VERIFIED_FINITE_DIAGNOSTIC",
}
if {claim_id: claims[claim_id]["status"] for claim_id in expected_claims} != expected_claims:
    fail("claim_statuses")
if claims_doc["audit"]["status"] != EXPECTED_STATUS:
    fail("claims_audit_status")
if claims_doc["audit"]["finite_diagnostics_passed"] != 5:
    fail("finite_diagnostics_passed")
if claims_doc["audit"]["paper_claims_verified"] != 0:
    fail("paper_claims_verified")
if claims_doc["audit"]["evidence_points"] != 10:
    fail("claims_evidence_points")

verdict = load("outputs/verdict.json")
expected_results = {
    "c1_delocalization": True,
    "c2_over_spec": False,
    "c3_under_spec": True,
    "c4_ase_bound": True,
    "c5_conjecture_binary": True,
    "c6_simulations": True,
}
for name, expected in expected_results.items():
    if verdict.get(name, {}).get("passed") is not expected:
        fail(name + "_result")
if abs(
    verdict["c2_over_spec"]["slope_over"]
    - verdict["c2_over_spec"]["slope_correct"]
) > 1e-15:
    fail("c2_slope_boundary")
if verdict["c3_under_spec"]["slope"] <= -0.3:
    fail("c3_threshold")
if verdict["c4_ase_bound"]["slope"] >= -0.2:
    fail("c4_threshold")
if verdict["c5_conjecture_binary"]["slope"] >= -0.2:
    fail("c5_threshold")
if verdict["c6_simulations"].get("over_larger") is not True:
    fail("c6_over_order")
if verdict["c6_simulations"].get("under_largest") is not True:
    fail("c6_under_order")

gate = load("publication_gate.json")
if gate.get("tests_passed") is not True:
    fail("gate_tests")
if gate.get("publication_gate_passed") is not True:
    fail("gate_publication")
if gate.get("finite_proxy_diagnostics_passed") != 5:
    fail("gate_finite_diagnostics")
if gate.get("paper_claims_verified") != 0:
    fail("gate_paper_claims")
if gate.get("overall_status") != "INCONCLUSIVE":
    fail("gate_status")

verdicts = load("reproduction_verdicts.json")
if verdicts.get("audit_status") != EXPECTED_STATUS:
    fail("verdict_status")
if verdicts.get("evidence", {}).get("current_score_claim") is not False:
    fail("current_score_claim")
if verdicts.get("evidence", {}).get("publication_allowed") is not False:
    fail("publication_boundary")

state = load("AUTONOMOUS_STATE.json")
if state.get("status") != EXPECTED_STATUS:
    fail("state_status")
if state.get("recovery", {}).get("bundle_sha256") != EXPECTED_RECOVERY_SHA:
    fail("recovery_sha")

manifest = load("EVIDENCE_MANIFEST.json")
missing = [
    path
    for path in manifest["required_paths"]
    if not (ROOT / path).is_file()
]
if missing:
    fail("missing_paths_" + ",".join(missing))

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for marker in (
    "2601.06014",
    "STATUS.md",
    "CLAIM_EVIDENCE.md",
    "Thank you",
    "not the authors' official implementation",
    "0/6 paper claims",
):
    if marker not in readme:
        fail("readme_" + marker.replace(" ", "_"))

branch_audit = (ROOT / "branch-audit.md").read_text(encoding="utf-8")
if EXPECTED_IDENTITY not in branch_audit:
    fail("branch_audit_identity")
if "6a71d9e3a1fd759c8f6f04dfd88bd6ca6044c5d1" not in branch_audit:
    fail("branch_audit_source_tip")

print(
    "FINAL_AUDIT=VERIFIED "
    "branches=1 "
    "commits=4 "
    "claims=C1:C3:C4:C5:C6_finite_diagnostic,C2_finite_check_failed "
    "evidence_points=10 "
    "paper_claims_verified=0 "
    "current_score_claim=false "
    "publication_allowed=false"
)
