#!/usr/bin/env python3
"""
External Audit Verification Script
==================================

Demonstrates how external parties can verify PB2S mandatory conformance artifacts.
This script can be used independently to validate conformance proof files.

Usage:
    python external_audit_verification.py [artifact_directory]

Version: 1.0
Author: PB2S Conformance Team
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import hashlib


def load_artifact(artifact_path: str) -> dict:
    """Load conformance artifact from file"""
    try:
        with open(artifact_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading artifact {artifact_path}: {e}")
        return {}


def verify_conformance_artifact(artifact: dict) -> dict:
    """
    Independent verification function for conformance artifacts
    Can be used by external auditors to validate compliance
    """
    verification = {
        "overall_valid": False,
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "summary": {}
    }
    
    # Core structure checks
    verification["checks"]["has_conformance_status"] = artifact.get("conformance_status") == "CONFORMANT"
    verification["checks"]["has_required_cycles"] = artifact.get("cycles_completed") == 3
    verification["checks"]["has_required_steps"] = artifact.get("total_steps") == 12
    verification["checks"]["has_validation_hash"] = len(artifact.get("validation_hash", "")) == 64
    
    # Artifact generation checks
    artifacts_gen = artifact.get("artifacts_generated", {})
    verification["checks"]["generated_cycle_artifacts"] = artifacts_gen.get("cycle_artifacts") == 3
    verification["checks"]["generated_step_artifacts"] = artifacts_gen.get("step_artifacts") == 12
    verification["checks"]["detected_flags"] = artifacts_gen.get("total_flags_detected", 0) > 0
    verification["checks"]["made_decisions"] = artifacts_gen.get("total_decisions_made", 0) > 0
    verification["checks"]["took_actions"] = artifacts_gen.get("total_actions_taken", 0) > 0
    
    # Detailed cycle verification
    cycles = artifact.get("cycles", [])
    verification["checks"]["has_3_cycles"] = len(cycles) == 3
    
    if len(cycles) == 3:
        verification["checks"]["all_cycles_have_4_steps"] = all(len(cycle.get("steps", [])) == 4 for cycle in cycles)
        verification["checks"]["all_steps_have_timestamps"] = all(
            "timestamp" in step for cycle in cycles for step in cycle.get("steps", [])
        )
        verification["checks"]["all_steps_have_artifacts"] = all(
            "artifact_id" in step for cycle in cycles for step in cycle.get("steps", [])
        )
        verification["checks"]["cycles_have_validation_hashes"] = all(
            "validation_hash" in cycle and len(cycle["validation_hash"]) == 64
            for cycle in cycles
        )
        
        # Check required step types are present
        required_steps = ["Perception", "Analysis", "Reflection", "Action"]
        verification["checks"]["all_required_step_types_present"] = all(
            all(step["step"] in [s["step"] for s in cycle.get("steps", [])] for step in [{"step": req_step} for req_step in required_steps])
            for cycle in cycles
        )
        
        # Check flagging requirements
        analysis_steps = [step for cycle in cycles for step in cycle.get("steps", []) if step.get("step") == "Analysis"]
        verification["checks"]["analysis_steps_have_flags"] = any(
            len(step.get("flags_detected", [])) > 0 for step in analysis_steps
        )
    
    # Audit trail checks
    audit_trail = artifact.get("audit_trail", {})
    verification["checks"]["has_audit_trail"] = bool(audit_trail)
    verification["checks"]["external_verification_enabled"] = audit_trail.get("external_verification") is True
    
    # Overall validation
    verification["overall_valid"] = all(verification["checks"].values())
    
    # Summary statistics
    verification["summary"] = {
        "total_checks": len(verification["checks"]),
        "passed_checks": sum(1 for v in verification["checks"].values() if v),
        "failed_checks": sum(1 for v in verification["checks"].values() if not v),
        "pass_rate": sum(1 for v in verification["checks"].values() if v) / len(verification["checks"]) * 100
    }
    
    return verification


def audit_directory(artifact_dir: str) -> dict:
    """Audit all conformance artifacts in a directory"""
    audit_results = {
        "directory": artifact_dir,
        "audit_timestamp": datetime.now().isoformat(),
        "artifacts_found": 0,
        "conformant_artifacts": 0,
        "non_conformant_artifacts": 0,
        "artifacts_details": []
    }
    
    artifact_path = Path(artifact_dir)
    if not artifact_path.exists():
        print(f"❌ Artifact directory does not exist: {artifact_dir}")
        return audit_results
    
    # Find all conformance proof artifacts
    proof_files = list(artifact_path.glob("*conformance_proof.json"))
    audit_results["artifacts_found"] = len(proof_files)
    
    if not proof_files:
        print(f"⚠️  No conformance proof artifacts found in {artifact_dir}")
        return audit_results
    
    print(f"🔍 Found {len(proof_files)} conformance proof artifacts")
    print()
    
    for proof_file in sorted(proof_files):
        print(f"Auditing: {proof_file.name}")
        
        # Load and verify artifact
        artifact = load_artifact(proof_file)
        if not artifact:
            continue
            
        verification = verify_conformance_artifact(artifact)
        
        artifact_detail = {
            "filename": proof_file.name,
            "run_id": artifact.get("run_id", "unknown"),
            "verification": verification,
            "conformant": verification["overall_valid"]
        }
        
        audit_results["artifacts_details"].append(artifact_detail)
        
        if verification["overall_valid"]:
            audit_results["conformant_artifacts"] += 1
            print(f"✅ CONFORMANT - {verification['summary']['passed_checks']}/{verification['summary']['total_checks']} checks passed")
        else:
            audit_results["non_conformant_artifacts"] += 1
            print(f"❌ NON-CONFORMANT - {verification['summary']['failed_checks']} checks failed:")
            for check_name, passed in verification["checks"].items():
                if not passed:
                    print(f"   - {check_name}")
        
        print(f"   Run ID: {artifact.get('run_id', 'N/A')}")
        print(f"   Timestamp: {artifact.get('start_timestamp', 'N/A')}")
        print(f"   Validation Hash: {artifact.get('validation_hash', 'N/A')[:16]}...")
        print()
    
    return audit_results


def main():
    if len(sys.argv) > 1:
        artifact_dir = sys.argv[1]
    else:
        artifact_dir = "conformance_artifacts"
    
    print("=" * 50)
    print("PB2S EXTERNAL AUDIT VERIFICATION")
    print("=" * 50)
    print(f"Auditing directory: {artifact_dir}")
    print()
    
    # Perform audit
    results = audit_directory(artifact_dir)
    
    # Print summary
    print("=" * 50)
    print("AUDIT SUMMARY")
    print("=" * 50)
    print(f"Total artifacts found: {results['artifacts_found']}")
    print(f"Conformant artifacts: {results['conformant_artifacts']}")
    print(f"Non-conformant artifacts: {results['non_conformant_artifacts']}")
    
    if results['artifacts_found'] > 0:
        conformance_rate = (results['conformant_artifacts'] / results['artifacts_found']) * 100
        print(f"Conformance rate: {conformance_rate:.1f}%")
        
        if results['conformant_artifacts'] == results['artifacts_found']:
            print("🎉 ALL ARTIFACTS ARE CONFORMANT")
            exit_code = 0
        else:
            print("⚠️  SOME ARTIFACTS ARE NON-CONFORMANT")
            exit_code = 1
    else:
        print("⚠️  NO ARTIFACTS FOUND FOR AUDIT")
        exit_code = 2
    
    print()
    print("Audit completed:", results['audit_timestamp'])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()