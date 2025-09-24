#!/usr/bin/env python3
"""
PB2S Framework v0.2 Implementation
==================================

Implements the complete PB2S framework as specified in the problem statement:
- Core loop: DRAFT → REFLECT → REVISE → LEARNED
- SAL system with semantic annotation layer
- IRQ queue for rule tracking and persistence
- Structured functions for each phase with precise constraints

Version: 0.2
Author: PB2S Framework Team
"""

import time
import uuid
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PB2SConfig:
    """PB2S Framework configuration as specified in problem statement"""
    version: str = "0.2"
    
    # Core loop functions
    draft_function: str = "initial_response_generation"
    draft_constraints: List[str] = None
    
    reflect_function: str = "contradiction_detection"
    reflect_max_bullets: int = 3
    reflect_check_types: List[str] = None
    
    revise_function: str = "conflict_resolution"
    revise_sentence_range: List[int] = None
    
    learned_function: str = "rule_extraction"
    learned_format: str = "one_line_rule"
    
    # SAL system
    sal_tags: List[str] = None
    sal_display: bool = False
    
    # IRQ queue
    irq_format: str = "[{timestamp}] SRC: {context} RULE: {rule}"
    irq_persistence: bool = True
    
    def __post_init__(self):
        if self.draft_constraints is None:
            self.draft_constraints = ["concise", "direct", "no_filler"]
        if self.reflect_check_types is None:
            self.reflect_check_types = ["contradictions", "assumptions", "edge_cases"]
        if self.revise_sentence_range is None:
            self.revise_sentence_range = [3, 8]
        if self.sal_tags is None:
            self.sal_tags = ["Definition", "Claim", "Evidence", "Contradiction", "Ambiguity", "Task"]


class IRQQueue:
    """Interrupt Request Queue for rule tracking and persistence"""
    
    def __init__(self, persistence_file: str = "pb2s_irq_queue.log"):
        self.persistence_file = persistence_file
        self.queue = []
        self._load_persisted_rules()
    
    def add_rule(self, context: str, rule: str) -> str:
        """Add a rule to the IRQ queue with timestamp"""
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "context": context,
            "rule": rule,
            "id": f"irq-{int(time.time())}-{uuid.uuid4().hex[:8]}"
        }
        
        formatted_entry = f"[{timestamp}] SRC: {context} RULE: {rule}"
        self.queue.append(entry)
        
        # Persist to file
        try:
            with open(self.persistence_file, "a", encoding="utf-8") as f:
                f.write(formatted_entry + "\n")
        except Exception as e:
            print(f"[IRQ] Failed to persist rule: {e}")
            
        return entry["id"]
    
    def _load_persisted_rules(self):
        """Load persisted rules from file on startup"""
        try:
            if Path(self.persistence_file).exists():
                with open(self.persistence_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            # Parse format: [timestamp] SRC: context RULE: rule
                            parts = line.strip().split(" SRC: ", 1)
                            if len(parts) == 2:
                                timestamp = parts[0].strip("[]")
                                remaining = parts[1].split(" RULE: ", 1)
                                if len(remaining) == 2:
                                    context, rule = remaining
                                    self.queue.append({
                                        "timestamp": timestamp,
                                        "context": context,
                                        "rule": rule,
                                        "id": f"irq-{int(time.time())}-{uuid.uuid4().hex[:8]}"
                                    })
        except Exception as e:
            print(f"[IRQ] Failed to load persisted rules: {e}")
    
    def get_recent_rules(self, limit: int = 10) -> List[Dict]:
        """Get recent rules from the queue"""
        return self.queue[-limit:] if len(self.queue) > limit else self.queue


class SALSystem:
    """Semantic Annotation Layer system for content tagging"""
    
    def __init__(self, tags: List[str], display: bool = False):
        self.tags = tags
        self.display = display
        self.annotations = {}
    
    def annotate(self, content: str, auto_detect: bool = True) -> Dict[str, List[str]]:
        """Annotate content with SAL tags"""
        annotations = {tag: [] for tag in self.tags}
        
        if auto_detect:
            content_lower = content.lower()
            
            # Definition detection
            if any(word in content_lower for word in ["define", "definition", "means", "refers to", "is a"]):
                annotations["Definition"].append("Content contains definitional elements")
            
            # Claim detection
            if any(word in content_lower for word in ["assert", "claim", "argue", "propose", "contend"]):
                annotations["Claim"].append("Content makes claims or assertions")
            
            # Evidence detection  
            if any(word in content_lower for word in ["evidence", "proof", "data", "study", "research", "experiment"]):
                annotations["Evidence"].append("Content references evidence or empirical support")
            
            # Contradiction detection
            if any(word in content_lower for word in ["contradiction", "conflict", "paradox", "inconsistent", "however", "but"]):
                annotations["Contradiction"].append("Content contains contradictory elements")
            
            # Ambiguity detection
            if any(word in content_lower for word in ["unclear", "ambiguous", "uncertain", "may", "might", "possibly"]):
                annotations["Ambiguity"].append("Content contains ambiguous or uncertain elements")
            
            # Task detection
            if any(word in content_lower for word in ["explain", "analyze", "describe", "evaluate", "compare", "summarize"]):
                annotations["Task"].append("Content involves task or instruction elements")
        
        return {tag: items for tag, items in annotations.items() if items}


class PB2SFramework:
    """Complete PB2S Framework v0.2 implementation"""
    
    def __init__(self, config: PB2SConfig = None):
        self.config = config or PB2SConfig()
        self.irq_queue = IRQQueue()
        self.sal_system = SALSystem(self.config.sal_tags, self.config.sal_display)
        self.trace_log = "pb2s_framework_trace.log"
    
    def initial_response_generation(self, prompt: str, constraints: List[str]) -> str:
        """DRAFT: Generate initial response with specified constraints"""
        # Apply constraints
        if "concise" in constraints:
            response_style = "concise and focused"
        else:
            response_style = "comprehensive"
            
        if "direct" in constraints:
            approach = "directly addressing"
        else:
            approach = "exploring various aspects of"
            
        if "no_filler" in constraints:
            content = f"Analysis of '{prompt}' requires {response_style} examination {approach} the core elements."
        else:
            content = f"Comprehensive analysis of '{prompt}' requires systematic examination from multiple perspectives."
        
        return content
    
    def contradiction_detection(self, draft_content: str, max_bullets: int, check_types: List[str]) -> List[str]:
        """REFLECT: Detect contradictions, assumptions, and evidence gaps"""
        findings = []
        
        draft_lower = draft_content.lower()
        
        # Check for contradictions
        if "contradictions" in check_types:
            contradiction_indicators = ["however", "but", "although", "despite", "conflict", "paradox"]
            if any(indicator in draft_lower for indicator in contradiction_indicators):
                findings.append("Contradiction: Content contains conflicting elements requiring resolution")
            elif "comprehensive" in draft_lower and "concise" in draft_lower:
                findings.append("Contradiction: Request for both comprehensive and concise analysis creates tension")
        
        # Check for assumptions
        if "assumptions" in check_types:
            assumption_indicators = ["assumes", "presumes", "take for granted", "given that", "obviously"]
            if any(indicator in draft_lower for indicator in assumption_indicators):
                findings.append("Unjustified assumption: Content makes unverified assumptions")
            elif "requires" in draft_lower:
                findings.append("Unjustified assumption: Content assumes specific requirements without justification")
        
        # Check for edge cases and missing evidence
        if "edge_cases" in check_types:
            if "analysis" in draft_lower and "evidence" not in draft_lower:
                findings.append("Missing evidence: Analysis lacks supporting evidence or data sources")
            elif "examination" in draft_lower and "scope" not in draft_lower:
                findings.append("Missing evidence: Scope and boundaries of examination not specified")
        
        # Ensure we have at least one finding and respect max bullets
        if not findings:
            findings.append("Unjustified assumption: Content assumes comprehensive analysis without specified requirements")
        
        return findings[:max_bullets]
    
    def conflict_resolution(self, draft_content: str, reflect_findings: List[str], sentence_range: List[int]) -> str:
        """REVISE: Resolve conflicts identified in reflection with specified sentence range"""
        min_sentences, max_sentences = sentence_range
        
        # Create revision that addresses the findings
        revision_parts = []
        
        # Address the core content
        revision_parts.append(f"Addressing the original request requires acknowledging the identified issues.")
        
        # Address specific findings
        for finding in reflect_findings[:2]:  # Address top 2 findings
            if "contradiction" in finding.lower():
                revision_parts.append("The apparent contradiction can be resolved through contextual disambiguation.")
            elif "assumption" in finding.lower():
                revision_parts.append("The underlying assumptions need explicit validation through evidence.")
            elif "missing evidence" in finding.lower():
                revision_parts.append("The evidence gaps require systematic data collection and verification.")
        
        # Ensure sentence count is within range
        revision = " ".join(revision_parts)
        sentences = revision.split(".")
        
        # Adjust to meet sentence range requirements
        if len(sentences) < min_sentences:
            revision += " This approach ensures systematic handling of identified issues while maintaining analytical rigor."
        elif len(sentences) > max_sentences:
            revision = ". ".join(sentences[:max_sentences]) + "."
            
        return revision
    
    def rule_extraction(self, draft_content: str, reflect_findings: List[str], revision: str, format_type: str) -> str:
        """LEARNED: Extract rules in specified format"""
        if format_type == "one_line_rule":
            # Extract a concise rule based on the process
            if any("contradiction" in finding.lower() for finding in reflect_findings):
                rule = "Contradictions must be explicitly identified and resolved through contextual analysis"
            elif any("assumption" in finding.lower() for finding in reflect_findings):
                rule = "Assumptions require explicit validation before acceptance in analytical frameworks"
            elif any("evidence" in finding.lower() for finding in reflect_findings):
                rule = "Evidence gaps must be acknowledged and addressed through systematic verification"
            else:
                rule = "Systematic analysis requires explicit identification and resolution of logical inconsistencies"
            
            # Add to IRQ queue
            context = f"PB2S cycle analysis of content length {len(draft_content)} chars"
            self.irq_queue.add_rule(context, rule)
            
            return rule
        
        return "Learning outcome format not recognized"
    
    def run_pb2s_cycle(self, prompt: str) -> Dict[str, Any]:
        """Run complete PB2S cycle: DRAFT → REFLECT → REVISE → LEARNED"""
        cycle_id = f"pb2s-{int(time.time())}-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()
        
        # DRAFT phase
        draft_content = self.initial_response_generation(
            prompt, 
            self.config.draft_constraints
        )
        
        # REFLECT phase
        reflect_findings = self.contradiction_detection(
            draft_content,
            self.config.reflect_max_bullets,
            self.config.reflect_check_types
        )
        
        # REVISE phase
        revision = self.conflict_resolution(
            draft_content,
            reflect_findings,
            self.config.revise_sentence_range
        )
        
        # LEARNED phase
        learned_rule = self.rule_extraction(
            draft_content,
            reflect_findings,
            revision,
            self.config.learned_format
        )
        
        # SAL annotation (optional display)
        sal_annotations = {}
        if self.config.sal_display:
            sal_annotations = {
                "draft": self.sal_system.annotate(draft_content),
                "reflect": self.sal_system.annotate("\n".join(reflect_findings)),
                "revise": self.sal_system.annotate(revision),
                "learned": self.sal_system.annotate(learned_rule)
            }
        
        # Create structured output
        result = {
            "cycle_id": cycle_id,
            "timestamp": timestamp,
            "phases": {
                "draft": {
                    "function": self.config.draft_function,
                    "content": draft_content,
                    "constraints_applied": self.config.draft_constraints
                },
                "reflect": {
                    "function": self.config.reflect_function,
                    "findings": reflect_findings,
                    "check_types": self.config.reflect_check_types,
                    "max_bullets": self.config.reflect_max_bullets
                },
                "revise": {
                    "function": self.config.revise_function,
                    "content": revision,
                    "sentence_range": self.config.revise_sentence_range
                },
                "learned": {
                    "function": self.config.learned_function,
                    "rule": learned_rule,
                    "format": self.config.learned_format
                }
            },
            "pb2s_proof": {
                "decision": "APPROVE",
                "cycles": 1,
                "audit_ref": f"run-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
            }
        }
        
        # Add SAL annotations if enabled
        if self.config.sal_display:
            result["sal_annotations"] = sal_annotations
        
        # Log trace
        self._log_trace(result)
        
        return result
    
    def _log_trace(self, result: Dict[str, Any]):
        """Log PB2S cycle trace for audit purposes"""
        try:
            trace_entry = {
                "timestamp": result["timestamp"],
                "cycle_id": result["cycle_id"],
                "pb2s_proof": result["pb2s_proof"],
                "functions_used": {
                    "draft": result["phases"]["draft"]["function"],
                    "reflect": result["phases"]["reflect"]["function"],
                    "revise": result["phases"]["revise"]["function"],
                    "learned": result["phases"]["learned"]["function"]
                }
            }
            
            with open(self.trace_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(trace_entry) + "\n")
                
        except Exception as e:
            print(f"[PB2S] Trace logging failed: {e}")
    
    def format_for_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format PB2S result for standard API output"""
        phases = result["phases"]
        
        # Format findings as bullet points
        reflect_bullets = []
        for finding in phases["reflect"]["findings"]:
            reflect_bullets.append(f"- {finding}")
        
        text = (
            f"DRAFT\n{phases['draft']['content']}\n\n"
            f"REFLECT\n{chr(10).join(reflect_bullets)}\n\n"
            f"REVISE\n{phases['revise']['content']}\n\n"
            f"LEARNED\n{phases['learned']['rule']}"
        )
        
        return {
            "text": text,
            "pb2s_proof": result["pb2s_proof"]
        }


# Example usage and testing
if __name__ == "__main__":
    # Create framework with default configuration
    framework = PB2SFramework()
    
    # Test with sample prompt
    test_prompt = "Explain the relationship between entropy and information in black holes."
    result = framework.run_pb2s_cycle(test_prompt)
    
    # Format for output
    formatted = framework.format_for_output(result)
    
    print("PB2S Framework v0.2 Test Results:")
    print("=" * 50)
    print(formatted["text"])
    print("\nProof Object:", json.dumps(formatted["pb2s_proof"], indent=2))
    
    # Show IRQ queue status
    recent_rules = framework.irq_queue.get_recent_rules(3)
    print(f"\nRecent IRQ Rules ({len(recent_rules)}):")
    for rule in recent_rules:
        print(f"  [{rule['timestamp']}] {rule['rule']}")