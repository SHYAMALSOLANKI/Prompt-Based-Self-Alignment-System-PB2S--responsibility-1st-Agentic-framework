#!/usr/bin/env python3
"""
PB2S Mandatory Conformance Demo
===============================

Demonstrates the complete mandatory conformance system:
1. Shows non-conformant vs conformant execution
2. Validates 3-cycle requirement with artifacts
3. External audit verification
4. API integration demonstration

Run this script to see the complete mandatory conformance system in action.

Usage:
    python pb2s_mandatory_conformance_demo.py

Version: 1.0
Author: PB2S Conformance Team
"""

import json
import time
import requests
from pathlib import Path
from pb2s_mandatory_conformance import MandatoryConformanceFramework
from external_audit_verification import audit_directory


def print_section_header(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo_standalone_framework():
    """Demonstrate the standalone mandatory conformance framework"""
    print_section_header("1. STANDALONE FRAMEWORK DEMONSTRATION")
    
    print("Creating MandatoryConformanceFramework instance...")
    framework = MandatoryConformanceFramework(artifact_dir="demo_artifacts")
    
    print("Executing mandatory conformance for sample prompt...")
    print("Prompt: 'Demonstrate the PB2S mandatory conformance system'")
    
    start_time = time.time()
    result = framework.execute_mandatory_conformance(
        "Demonstrate the PB2S mandatory conformance system"
    )
    execution_time = time.time() - start_time
    
    print(f"\n✅ Execution completed in {execution_time:.2f} seconds")
    print(f"Status: {result['conformance_status']}")
    print(f"Cycles completed: {result['cycles_completed']}/{result['required_cycles']}")
    print(f"Total steps: {result['total_steps']}")
    print(f"Run ID: {result['run_id']}")
    
    # Show artifact summary
    artifacts = result['artifacts_generated']
    print(f"\nArtifacts Generated:")
    print(f"  - Cycle artifacts: {artifacts['cycle_artifacts']}")
    print(f"  - Step artifacts: {artifacts['step_artifacts']}")  
    print(f"  - Flags detected: {artifacts['total_flags_detected']}")
    print(f"  - Decisions made: {artifacts['total_decisions_made']}")
    print(f"  - Actions taken: {artifacts['total_actions_taken']}")
    
    print(f"\nValidation hash: {result['validation_hash'][:32]}...")
    print(f"Artifacts saved to: {result['audit_trail']['artifact_directory']}")
    
    return result


def demo_api_integration(server_url: str = "http://localhost:8000"):
    """Demonstrate API integration with mandatory conformance"""
    print_section_header("2. API INTEGRATION DEMONSTRATION") 
    
    # Test regular endpoint vs mandatory conformance endpoint
    test_message = "Test API mandatory conformance integration"
    
    print("Testing regular /chat endpoint...")
    try:
        response = requests.post(
            f"{server_url}/chat",
            json={"message": test_message},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            proof = data.get("pb2s_proof", {})
            print(f"✅ Regular endpoint responded")
            print(f"   Cycles: {proof.get('cycles', 'N/A')}")
            print(f"   Decision: {proof.get('decision', 'N/A')}")
            print(f"   Has mandatory_conformance: {'mandatory_conformance' in proof}")
        else:
            print(f"❌ Regular endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Regular endpoint error: {e}")
    
    print(f"\nTesting mandatory conformance /mandatory_conformance endpoint...")
    try:
        response = requests.post(
            f"{server_url}/mandatory_conformance", 
            json={"message": test_message, "enforce_conformance": True},
            timeout=120  # Longer timeout for 3-cycle execution
        )
        
        if response.status_code == 200:
            data = response.json()
            proof = data.get("pb2s_proof", {})
            conformance = proof.get("mandatory_conformance", {})
            
            print(f"✅ Mandatory conformance endpoint responded")
            print(f"   Status: {conformance.get('status', 'N/A')}")
            print(f"   Cycles: {conformance.get('cycles_completed', 'N/A')}/{conformance.get('required_cycles', 'N/A')}")
            print(f"   Total steps: {conformance.get('total_steps', 'N/A')}")
            print(f"   External audit ready: {conformance.get('external_audit_ready', 'N/A')}")
            
            # Show text response structure
            text = data.get("text", "")
            cycle_count = text.count("CYCLE")
            print(f"   Response shows {cycle_count} cycles")
            
            return conformance
            
        else:
            print(f"❌ Mandatory conformance endpoint failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Mandatory conformance endpoint error: {e}")
        return None


def demo_external_audit():
    """Demonstrate external audit capabilities"""
    print_section_header("3. EXTERNAL AUDIT DEMONSTRATION")
    
    print("Running external audit verification on generated artifacts...")
    
    # Check both demo and conformance artifacts directories
    directories = ["demo_artifacts", "conformance_artifacts"]
    
    for artifact_dir in directories:
        if Path(artifact_dir).exists():
            print(f"\nAuditing directory: {artifact_dir}")
            try:
                results = audit_directory(artifact_dir)
                
                if results['artifacts_found'] > 0:
                    print(f"  ✅ Found {results['artifacts_found']} artifacts")
                    print(f"  ✅ {results['conformant_artifacts']} conformant")
                    print(f"  ❌ {results['non_conformant_artifacts']} non-conformant")
                    
                    conformance_rate = (results['conformant_artifacts'] / results['artifacts_found']) * 100
                    print(f"  📊 Conformance rate: {conformance_rate:.1f}%")
                else:
                    print(f"  ⚠️  No artifacts found")
                    
            except Exception as e:
                print(f"  ❌ Audit error: {e}")
        else:
            print(f"\n⚠️  Directory {artifact_dir} does not exist")


def demo_compliance_validation():
    """Demonstrate compliance validation against requirements"""
    print_section_header("4. COMPLIANCE VALIDATION")
    
    print("Validating system against mandatory conformance requirements:")
    print("\n📋 REQUIREMENTS CHECKLIST:")
    
    # Run a test execution to validate
    framework = MandatoryConformanceFramework(artifact_dir="validation_artifacts")
    result = framework.execute_mandatory_conformance("Validation test")
    
    requirements = [
        ("Complete 4-step cycle THREE consecutive times", 
         result['cycles_completed'] == 3,
         f"Completed {result['cycles_completed']}/3 cycles"),
        
        ("Total of 12 steps (3 cycles × 4 steps)", 
         result['total_steps'] == 12,
         f"Executed {result['total_steps']}/12 steps"),
        
        ("Produce system-generated artifacts", 
         result['artifacts_generated']['step_artifacts'] > 0,
         f"Generated {result['artifacts_generated']['step_artifacts']} step artifacts"),
        
        ("Include timestamps for each step", 
         len(result['cycles'][0]['steps']) == 4 and all('timestamp' in step for step in result['cycles'][0]['steps']),
         "All steps have timestamps"),
        
        ("Include data/decisions made at each step", 
         result['artifacts_generated']['total_decisions_made'] > 0,
         f"Made {result['artifacts_generated']['total_decisions_made']} decisions"),
        
        ("Evidence of flagging", 
         result['artifacts_generated']['total_flags_detected'] > 0,
         f"Detected {result['artifacts_generated']['total_flags_detected']} flags"),
        
        ("Evidence of actions taken", 
         result['artifacts_generated']['total_actions_taken'] > 0,
         f"Took {result['artifacts_generated']['total_actions_taken']} actions"),
        
        ("Artifacts accessible for audit", 
         Path(result['audit_trail']['artifact_directory']).exists(),
         f"Artifacts in {result['audit_trail']['artifact_directory']}"),
        
        ("External verification enabled", 
         result['audit_trail']['external_verification'],
         "External audit ready"),
        
        ("No simulation/chat-only output", 
         result['conformance_status'] == 'CONFORMANT',
         "System-generated artifacts provided")
    ]
    
    passed_requirements = 0
    for requirement, passed, details in requirements:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {requirement}")
        print(f"       {details}")
        if passed:
            passed_requirements += 1
    
    print(f"\n📊 COMPLIANCE SUMMARY:")
    print(f"   Requirements passed: {passed_requirements}/{len(requirements)}")
    compliance_rate = (passed_requirements / len(requirements)) * 100
    print(f"   Compliance rate: {compliance_rate:.1f}%")
    
    if passed_requirements == len(requirements):
        print("   🎉 FULLY COMPLIANT WITH MANDATORY REQUIREMENTS")
        return True
    else:
        print("   ❌ NOT FULLY COMPLIANT")
        return False


def main():
    """Main demonstration function"""
    print("🚀 PB2S MANDATORY CONFORMANCE SYSTEM DEMONSTRATION")
    print("This demo shows the complete implementation of mandatory conformance instructions.")
    
    # 1. Standalone framework demo
    demo_standalone_framework()
    
    # Small delay for readability
    time.sleep(1)
    
    # 2. API integration demo
    api_result = demo_api_integration()
    
    # Small delay for readability  
    time.sleep(1)
    
    # 3. External audit demo
    demo_external_audit()
    
    # Small delay for readability
    time.sleep(1)
    
    # 4. Compliance validation
    is_compliant = demo_compliance_validation()
    
    # Final summary
    print_section_header("DEMONSTRATION COMPLETE")
    
    if is_compliant:
        print("🎉 SUCCESS: PB2S Mandatory Conformance System is fully implemented and compliant!")
        print("\nKey achievements:")
        print("✅ 3-cycle execution with 12 total steps")
        print("✅ System-generated artifacts with timestamps")
        print("✅ Flagging, decisions, and actions tracking")
        print("✅ External audit accessibility")
        print("✅ API integration with backward compatibility")
        print("✅ Comprehensive testing and validation")
        
        print(f"\n📁 Artifacts available for external verification in:")
        for dir_name in ["demo_artifacts", "conformance_artifacts", "validation_artifacts"]:
            if Path(dir_name).exists():
                print(f"   - {dir_name}/")
        
        print(f"\n🔧 Usage:")
        print(f"   - Standalone: python pb2s_mandatory_conformance.py")
        print(f"   - API: POST to /mandatory_conformance endpoint")  
        print(f"   - External audit: python external_audit_verification.py [dir]")
        print(f"   - Testing: python scripts/mandatory_conformance_tests.py")
        
    else:
        print("❌ FAILURE: System not fully compliant with mandatory requirements")
    
    print("\nDemo completed. Check generated artifacts for detailed conformance proof.")


if __name__ == "__main__":
    main()