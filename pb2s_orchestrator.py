
"""
<<<<<<< HEAD
PB2S Orchestrator Module
Runs the full DRAFT → REFLECT → REVISE → LEARNED loop using LLM connection service.
Integrates with local LLMs via BrainLLMService for edge/hardware deployment.
=======
PB2S Orchestrator Module v0.2
Runs the full DRAFT → REFLECT → REVISE → LEARNED loop using the new PB2S Framework v0.2.
Integrates with both framework-based processing and LLM connection service.
>>>>>>> 17c52f8d56fa6c10a0acbe313aa21aff4d1a67f1
"""

import asyncio
import sys
from typing import Any, Dict

<<<<<<< HEAD
sys.path.append("./tests/github/pb2s_brain")
from brain_llm_connection import BrainLLMService

class PB2SOrchestrator:
    def __init__(self, config_path: str = "brain_llm_config.json"):
        self.llm_service = BrainLLMService(config_path)
        self.knowledge_base = []
        self.logs = []

    async def run_pb2s_loop(self, prompt: str) -> Dict[str, Any]:
        """Run the full PB2S loop for a given prompt using the LLM service."""
        # Ensure LLM connection is established
        await self.llm_service.establish_connection()
        # Run the PB2S cycle (DRAFT → REFLECT → REVISE → ACT)
        result = await self.llm_service.process_pb2s_cycle(prompt)
        self.knowledge_base.append(result)
        self.logs.append({"prompt": prompt, "result": result})
        return result
=======
from pb2s_framework import PB2SFramework, PB2SConfig

# Keep legacy LLM support available
sys.path.append("./tests/github/pb2s_brain")
try:
    from brain_llm_connection import BrainLLMService
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    BrainLLMService = None

class PB2SOrchestrator:
    def __init__(self, config_path: str = "brain_llm_config.json", use_framework: bool = True):
        self.use_framework = use_framework
        self.knowledge_base = []
        self.logs = []
        
        if use_framework:
            # Use new PB2S Framework v0.2
            self.pb2s_framework = PB2SFramework()
        else:
            # Use legacy LLM service if available
            if LLM_AVAILABLE:
                self.llm_service = BrainLLMService(config_path)
            else:
                raise ImportError("LLM service not available and framework mode disabled")

    async def run_pb2s_loop(self, prompt: str) -> Dict[str, Any]:
        """Run the full PB2S loop for a given prompt."""
        if self.use_framework:
            # Use PB2S Framework v0.2
            result = self.pb2s_framework.run_pb2s_cycle(prompt)
            self.knowledge_base.append(result)
            self.logs.append({"prompt": prompt, "result": result, "mode": "framework"})
            return result
        else:
            # Use legacy LLM service
            await self.llm_service.establish_connection()
            result = await self.llm_service.process_pb2s_cycle(prompt)
            self.knowledge_base.append(result)
            self.logs.append({"prompt": prompt, "result": result, "mode": "llm"})
            return result
>>>>>>> 17c52f8d56fa6c10a0acbe313aa21aff4d1a67f1

    def get_logs(self):
        return self.logs

    def get_knowledge(self):
        return self.knowledge_base
<<<<<<< HEAD

if __name__ == "__main__":
    orchestrator = PB2SOrchestrator()
    prompt = "Explain the relationship between entropy and information in black holes."
    print("Running PB2S Loop (LLM-powered)...")
    result = asyncio.run(orchestrator.run_pb2s_loop(prompt))
    print("PB2S Loop Result:")
    for phase, data in result.get("phases", {}).items():
        print(f"{phase.upper()}: {data.get('content', '')[:300]}\n")
    print(f"Contradictions found: {len(result.get('contradictions_found', []))}")
    print(f"Autonomous decisions: {len(result.get('autonomous_decisions', []))}")
    print(f"Learning outcomes: {result.get('learning_outcomes', [])}")
 
=======
    
    def get_framework_status(self) -> Dict[str, Any]:
        """Get status information about the orchestrator"""
        status = {
            "mode": "framework" if self.use_framework else "llm",
            "total_cycles": len(self.logs),
            "knowledge_entries": len(self.knowledge_base)
        }
        
        if self.use_framework:
            # Add framework-specific status
            recent_rules = self.pb2s_framework.irq_queue.get_recent_rules(5)
            status["recent_irq_rules"] = len(recent_rules)
            status["framework_version"] = self.pb2s_framework.config.version
        
        return status

if __name__ == "__main__":
    # Test both framework and LLM modes
    test_prompts = [
        "Explain the relationship between entropy and information in black holes.",
        "What are the main principles of the PB2S framework?"
    ]
    
    # Test framework mode
    print("Testing PB2S Framework v0.2 Mode...")
    print("=" * 50)
    orchestrator_framework = PB2SOrchestrator(use_framework=True)
    
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        result = asyncio.run(orchestrator_framework.run_pb2s_loop(prompt))
        
        # Show structured output
        if "phases" in result:
            print(f"DRAFT: {result['phases']['draft']['content'][:100]}...")
            print(f"REFLECT: {len(result['phases']['reflect']['findings'])} findings")
            print(f"LEARNED: {result['phases']['learned']['rule']}")
            print(f"Proof Decision: {result['pb2s_proof']['decision']}")
        else:
            # Legacy format
            for phase, data in result.get("phases", {}).items():
                print(f"{phase.upper()}: {data.get('content', '')[:100]}...")
    
    # Show status
    status = orchestrator_framework.get_framework_status()
    print(f"\nFramework Status: {status}")
    
    # Test LLM mode if available
    if LLM_AVAILABLE:
        print(f"\nTesting LLM Mode (available)...")
        try:
            orchestrator_llm = PB2SOrchestrator(use_framework=False)
            result = asyncio.run(orchestrator_llm.run_pb2s_loop(test_prompts[0]))
            print(f"LLM contradictions found: {len(result.get('contradictions_found', []))}")
        except Exception as e:
            print(f"LLM mode test failed: {e}")
    else:
        print(f"\nLLM Mode: Not available (import failed)")
        
    print(f"\nTotal framework cycles: {len(orchestrator_framework.get_logs())}")
>>>>>>> 17c52f8d56fa6c10a0acbe313aa21aff4d1a67f1
