#!/usr/bin/env python3
"""
PB2S Framework v0.2 Validation Script
=====================================

Validates that the implemented PB2S framework meets all requirements 
from the problem statement.
"""

import json
import subprocess
import sys
from pathlib import Path

def test_framework_direct():
    """Test the framework module directly"""
    print("=== Direct Framework Test ===")
    try:
        from pb2s_framework import PB2SFramework, PB2SConfig
        
        # Test configuration matches problem statement
        config = PB2SConfig()
        assert config.version == "0.2"
        assert config.draft_function == "initial_response_generation"
        assert config.draft_constraints == ["concise", "direct", "no_filler"]
        assert config.reflect_function == "contradiction_detection"
        assert config.reflect_max_bullets == 3
        assert config.reflect_check_types == ["contradictions", "assumptions", "edge_cases"]
        assert config.revise_function == "conflict_resolution"
        assert config.revise_sentence_range == [3, 8]
        assert config.learned_function == "rule_extraction"
        assert config.learned_format == "one_line_rule"
        assert config.sal_tags == ["Definition", "Claim", "Evidence", "Contradiction", "Ambiguity", "Task"]
        assert config.sal_display == False
        assert config.irq_format == "[{timestamp}] SRC: {context} RULE: {rule}"
        assert config.irq_persistence == True
        
        print("✅ Configuration matches problem statement")
        
        # Test framework functionality
        framework = PB2SFramework(config)
        result = framework.run_pb2s_cycle("Test prompt for validation")
        
        assert "phases" in result
        assert all(phase in result["phases"] for phase in ["draft", "reflect", "revise", "learned"])
        assert "pb2s_proof" in result
        assert result["pb2s_proof"]["decision"] in ["APPROVE", "CLARIFY"]
        assert 0 <= result["pb2s_proof"]["cycles"] <= 2
        assert "audit_ref" in result["pb2s_proof"]
        
        print("✅ Framework cycle execution successful")
        
        # Test IRQ queue
        irq_entries = framework.irq_queue.get_recent_rules(1)
        assert len(irq_entries) > 0
        assert all(key in irq_entries[0] for key in ["timestamp", "context", "rule", "id"])
        
        print("✅ IRQ queue operational")
        
        # Test SAL system
        sal_annotations = framework.sal_system.annotate("Define quantum entanglement contradiction")
        assert isinstance(sal_annotations, dict)
        
        print("✅ SAL system operational")
        
        return True
        
    except Exception as e:
        print(f"❌ Framework test failed: {e}")
        return False

def test_conformance():
    """Test conformance validation"""
    print("\n=== Conformance Test ===")
    try:
        result = subprocess.run([
            sys.executable, "scripts/conformance.py", 
            "--endpoint", "http://127.0.0.1:8000/chat"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and "PASSED" in result.stdout:
            print("✅ Conformance tests passed")
            return True
        else:
            print(f"❌ Conformance test failed: {result.stdout}")
            return False
    except Exception as e:
        print(f"❌ Conformance test error: {e}")
        return False

def test_irq_format():
    """Test IRQ queue format matches specification"""
    print("\n=== IRQ Format Test ===")
    try:
        irq_file = Path("pb2s_irq_queue.log")
        if irq_file.exists():
            with open(irq_file, "r") as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    # Check format: [timestamp] SRC: context RULE: rule
                    if (last_line.startswith("[") and 
                        "] SRC: " in last_line and 
                        " RULE: " in last_line):
                        print("✅ IRQ format matches specification")
                        print(f"   Sample: {last_line[:80]}...")
                        return True
                    else:
                        print(f"❌ IRQ format incorrect: {last_line}")
                        return False
                else:
                    print("❌ IRQ log empty")
                    return False
        else:
            print("❌ IRQ log file not found")
            return False
    except Exception as e:
        print(f"❌ IRQ format test error: {e}")
        return False

def test_api_response():
    """Test API response structure"""
    print("\n=== API Response Test ===")
    try:
        import httpx
        
        response = httpx.post(
            "http://127.0.0.1:8000/chat",
            json={"message": "Test PB2S framework validation"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            assert "text" in data and "pb2s_proof" in data
            text = data["text"]
            
            # Check section order
            sections = ["DRAFT", "REFLECT", "REVISE", "LEARNED"]
            for section in sections:
                if section not in text:
                    print(f"❌ Missing section: {section}")
                    return False
            
            # Check REFLECT format
            reflect_section = text.split("REFLECT")[1].split("REVISE")[0]
            required_keywords = ["contradiction", "unjustified assumption", "missing evidence"]
            if not any(keyword in reflect_section.lower() for keyword in required_keywords):
                print(f"❌ REFLECT missing required keywords: {required_keywords}")
                return False
            
            # Check proof object
            proof = data["pb2s_proof"]
            assert proof["decision"] in ["APPROVE", "CLARIFY"]
            assert 0 <= proof["cycles"] <= 2
            assert "audit_ref" in proof
            
            print("✅ API response structure valid")
            print(f"   Decision: {proof['decision']}")
            print(f"   Cycles: {proof['cycles']}")
            return True
        else:
            print(f"❌ API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def main():
    """Run all validation tests"""
    print("PB2S Framework v0.2 Validation")
    print("=" * 40)
    
    tests = [
        ("Framework Direct", test_framework_direct),
        ("Conformance", test_conformance),
        ("IRQ Format", test_irq_format),
        ("API Response", test_api_response)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\n=== Validation Summary ===")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - PB2S v0.2 implementation complete!")
        return 0
    else:
        print("❌ Some tests failed - implementation needs review")
        return 1

if __name__ == "__main__":
    sys.exit(main())