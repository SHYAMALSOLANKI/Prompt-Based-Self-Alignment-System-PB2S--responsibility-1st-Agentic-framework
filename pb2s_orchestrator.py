
"""
PB2S Orchestrator Module
Runs the full DRAFT → REFLECT → REVISE → LEARNED loop using LLM connection service.
Integrates with local LLMs via BrainLLMService for edge/hardware deployment.
"""

import asyncio
import sys
from typing import Any, Dict

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

    def get_logs(self):
        return self.logs

    def get_knowledge(self):
        return self.knowledge_base

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
