#!/usr/bin/env python3
"""
Mandatory Conformance Test Suite
================================

Tests for PB2S Mandatory Conformance Instructions:
- Validates 3-cycle execution requirement
- Verifies artifact generation
- Checks external audit accessibility
- Validates structure compliance

Version: 1.0
Author: PB2S Conformance Team
"""

import argparse
import json
import os
import sys
import httpx
import time
from pathlib import Path
from jsonschema import validate, ValidationError

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pb2s_mandatory_conformance import validate_conformance_artifact

ROOT = Path(__file__).resolve().parent

def test_mandatory_conformance_api(endpoint_url: str, message: str) -> dict:
    """Test the mandatory conformance API endpoint"""
    try:
        with httpx.Client(timeout=120) as client:  # Longer timeout for 3-cycle execution
            response = client.post(
                endpoint_url, 
                json={"message": message, "enforce_conformance": True}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e)}

def validate_mandatory_response(response: dict) -> list:
    """Validate that response meets mandatory conformance requirements"""
    problems = []
    
    # Check basic structure
    if "error" in response:
        problems.append(f"API Error: {response['error']}")
        return problems
    
    if not isinstance(response, dict) or "pb2s_proof" not in response:
        problems.append("Missing pb2s_proof in response")
        return problems
    
    proof = response["pb2s_proof"]
    
    # Check mandatory conformance section
    if "mandatory_conformance" not in proof:
        problems.append("Missing mandatory_conformance section in pb2s_proof")
        return problems
    
    conformance = proof["mandatory_conformance"]
    
    # Validate mandatory requirements
    required_fields = [
        "status", "cycles_completed", "required_cycles", "total_steps",
        "artifacts_generated", "validation_hash", "external_audit_ready"
    ]
    
    for field in required_fields:
        if field not in conformance:
            problems.append(f"Missing required field: {field}")
    
    # Validate specific requirements
    if conformance.get("status") != "CONFORMANT":
        problems.append(f"Status is not CONFORMANT: {conformance.get('status')}")
    
    if conformance.get("cycles_completed") != 3:
        problems.append(f"Must complete 3 cycles, got: {conformance.get('cycles_completed')}")
    
    if conformance.get("required_cycles") != 3:
        problems.append(f"Required cycles must be 3, got: {conformance.get('required_cycles')}")
    
    if conformance.get("total_steps") != 12:
        problems.append(f"Must complete 12 total steps (3×4), got: {conformance.get('total_steps')}")
    
    if not conformance.get("external_audit_ready"):
        problems.append("External audit must be ready")
    
    # Validate artifacts generated
    artifacts = conformance.get("artifacts_generated", {})
    if not isinstance(artifacts, dict):
        problems.append("artifacts_generated must be a dictionary")
    else:
        if artifacts.get("cycle_artifacts") != 3:
            problems.append(f"Must generate 3 cycle artifacts, got: {artifacts.get('cycle_artifacts')}")
        
        if artifacts.get("step_artifacts") != 12:
            problems.append(f"Must generate 12 step artifacts, got: {artifacts.get('step_artifacts')}")
        
        # Check that flags, decisions, and actions were detected/made
        if artifacts.get("total_flags_detected", 0) == 0:
            problems.append("Must detect flags during analysis")
        
        if artifacts.get("total_decisions_made", 0) == 0:
            problems.append("Must make decisions during processing")
        
        if artifacts.get("total_actions_taken", 0) == 0:
            problems.append("Must take actions during processing")
    
    # Validate response text structure 
    if "text" not in response:
        problems.append("Missing text field in response")
    else:
        text = response["text"]
        
        # Should contain multiple cycles
        if text.count("CYCLE") < 3:
            problems.append("Response must show evidence of 3 cycles")
        
        # Should contain all required sections per cycle
        required_sections = ["DRAFT", "REFLECT", "REVISE", "LEARNED"]
        for section in required_sections:
            if text.count(section) < 3:  # Each section should appear 3 times (once per cycle)
                problems.append(f"Section {section} must appear in each cycle (expected 3, found {text.count(section)})")
        
        # Check REFLECT sections contain required flags
        reflect_indicators = ["contradiction", "assumption", "missing evidence", "unjustified assumption"]
        reflect_found = any(indicator in text.lower() for indicator in reflect_indicators)
        if not reflect_found:
            problems.append("REFLECT sections must flag contradictions, assumptions, or missing evidence")
    
    return problems

def test_artifact_accessibility(conformance_data: dict) -> list:
    """Test that generated artifacts are accessible for external audit"""
    problems = []
    
    artifact_dir = conformance_data.get("artifact_directory", "conformance_artifacts")
    if not os.path.exists(artifact_dir):
        problems.append(f"Artifact directory does not exist: {artifact_dir}")
        return problems
    
    # Check for recent artifacts (within last 5 minutes)
    recent_cutoff = time.time() - 300  # 5 minutes ago
    artifact_files = []
    
    for file_path in Path(artifact_dir).glob("*.json"):
        if file_path.stat().st_mtime > recent_cutoff:
            artifact_files.append(str(file_path))
    
    if not artifact_files:
        problems.append("No recent conformance artifacts found")
        return problems
    
    # Validate at least one complete conformance artifact
    conformance_artifacts = [f for f in artifact_files if "conformance_proof" in f]
    if not conformance_artifacts:
        problems.append("No complete conformance proof artifacts found")
        return problems
    
    # Validate the structure of the most recent artifact
    latest_artifact = sorted(conformance_artifacts)[-1]
    try:
        validation_result = validate_conformance_artifact(latest_artifact)
        if not validation_result.get("artifact_valid"):
            problems.append(f"Artifact validation failed: {validation_result.get('error', 'Unknown error')}")
        else:
            # Check specific validation results
            checks = validation_result.get("checks", {})
            for check_name, passed in checks.items():
                if not passed:
                    problems.append(f"Artifact validation check failed: {check_name}")
    except Exception as e:
        problems.append(f"Error validating artifact {latest_artifact}: {e}")
    
    return problems

def run_mandatory_conformance_tests(endpoint: str, test_messages: list) -> bool:
    """Run complete mandatory conformance test suite"""
    print("=== PB2S Mandatory Conformance Test Suite ===\n")
    
    total_tests = len(test_messages)
    passed_tests = 0
    
    for i, message in enumerate(test_messages, 1):
        test_id = f"mandatory_test_{i}"
        print(f"Running test {i}/{total_tests}: {test_id}")
        print(f"Message: {message}")
        
        # Test API response
        response = test_mandatory_conformance_api(endpoint, message)
        
        # Validate response
        response_problems = validate_mandatory_response(response)
        
        # Test artifact accessibility if response is valid
        artifact_problems = []
        if not response_problems and "pb2s_proof" in response:
            conformance_data = response["pb2s_proof"].get("mandatory_conformance", {})
            artifact_problems = test_artifact_accessibility(conformance_data)
        
        all_problems = response_problems + artifact_problems
        
        if not all_problems:
            print(f"✅ {test_id}: PASSED")
            passed_tests += 1
        else:
            print(f"❌ {test_id}: FAILED")
            for problem in all_problems:
                print(f"   - {problem}")
        
        print()  # Empty line between tests
    
    # Summary
    print("=== Test Results Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL MANDATORY CONFORMANCE TESTS PASSED")
        return True
    else:
        print("❌ MANDATORY CONFORMANCE TESTS FAILED")
        return False

def main():
    parser = argparse.ArgumentParser(description="PB2S Mandatory Conformance Test Suite")
    parser.add_argument("--endpoint", default="http://localhost:8000/mandatory_conformance", 
                       help="Mandatory conformance endpoint URL")
    parser.add_argument("--messages", nargs="+", 
                       default=[
                           "Test mandatory conformance with basic query",
                           "Explain the four-step cycle requirement",  
                           "Generate artifacts for external audit verification"
                       ],
                       help="Test messages to send")
    
    args = parser.parse_args()
    
    # Run tests
    success = run_mandatory_conformance_tests(args.endpoint, args.messages)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()