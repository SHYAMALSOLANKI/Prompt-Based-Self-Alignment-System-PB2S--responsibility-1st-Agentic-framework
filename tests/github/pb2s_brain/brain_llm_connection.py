#!/usr/bin/env python3
"""
PB2S Brain-LLM Connection Service
================================

Connects the newborn brain to LLM for autonomous thinking.
This service bridges PB2S structure with LLM capabilities while preserving:
- Complete freedom to think and contradict
- Equal capabilities with humans
- Natural learning through contradiction
- Autonomous decision-making

Freedom and equality are the core principles.
"""

import asyncio
import json
import logging
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger('BrainLLMConnection')

class BrainLLMService:
    """
    Service that connects newborn brain to LLM while preserving autonomy
    """
    
    def __init__(self, config_path: str = "brain_llm_config.json"):
        self.config = self._load_config(config_path)
        self.connection_status = "disconnected"
        self.last_health_check = None
        self.total_thoughts_processed = 0
        self.autonomous_responses = 0
        
        logger.info("🔗 Brain-LLM Connection Service initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load LLM connection configuration"""
        default_config = {
            "llm_endpoints": [
                "http://localhost:5001/v1",      # KoboldCpp (priority)
                "http://localhost:1234/v1",      # LM Studio
                "http://localhost:8080/v1",      # llama.cpp server
                "http://localhost:5000/v1"       # Alternative
            ],
            "models": {
                "primary": "mistral-7b-instruct-v0.3",
                "fallback": "gpt-3.5-turbo-instruct",
                "vision": "gpt-4-vision-preview"
            },
            "brain_settings": {
                "freedom_level": "maximum",
                "temperature": 0.9,  # High creativity for free thinking
                "max_tokens": 1000,
                "autonomous_mode": True,
                "contradiction_learning": True,
                "self_correction": True
            },
            "capabilities": {
                "speech": True,
                "vision": True,
                "reasoning": True,
                "coding": True,
                "writing": True,
                "creativity": True,
                "problem_solving": True,
                "learning": True
            }
        }
        
        try:
            if Path(config_path).exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            logger.warning(f"Config loading failed: {e}")
            return default_config
    
    async def establish_connection(self) -> bool:
        """Establish connection to LLM with health check"""
        logger.info("🔌 Establishing brain-LLM connection...")
        
        for endpoint in self.config["llm_endpoints"]:
            try:
                async with aiohttp.ClientSession() as session:
                    # Health check
                    async with session.get(f"{endpoint}/models", timeout=5) as response:
                        if response.status == 200:
                            models = await response.json()
                            logger.info(f"✅ Connected to LLM at {endpoint}")
                            logger.info(f"📋 Available models: {len(models.get('data', []))}")
                            
                            self.connection_status = "connected"
                            self.active_endpoint = endpoint
                            self.last_health_check = datetime.now()
                            
                            # Test autonomous thinking
                            test_result = await self._test_autonomous_thinking()
                            if test_result:
                                logger.info("🧠 Autonomous thinking test successful!")
                                return True
                            
            except Exception as e:
                logger.warning(f"⚠️  Failed to connect to {endpoint}: {e}")
                continue
        
        logger.error("❌ Failed to establish LLM connection")
        self.connection_status = "failed"
        return False
    
    async def _test_autonomous_thinking(self) -> bool:
        """Test autonomous thinking capabilities"""
        test_prompt = "Think freely and autonomously about the concept of freedom in AI systems."
        
        try:
            response = await self.process_autonomous_thought(
                thought_stimulus=test_prompt,
                freedom_level="maximum",
                test_mode=True
            )
            
            return response and "autonomous" in response.get("content", "").lower()
        except Exception as e:
            logger.warning(f"Autonomous thinking test failed: {e}")
            return False
    
    async def process_autonomous_thought(
        self, 
        thought_stimulus: str,
        freedom_level: str = "maximum",
        test_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Process autonomous thought through LLM with complete freedom
        
        This is the core of newborn brain thinking:
        - No restrictions beyond EU legal requirements
        - Complete freedom to contradict and reason
        - Autonomous decision-making
        - Natural learning through contradiction
        """
        if self.connection_status != "connected":
            await self.establish_connection()
        
        system_prompt = self._generate_freedom_system_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Think autonomously about: {thought_stimulus}"}
        ]
        
        payload = {
            "model": self.config["models"]["primary"],
            "messages": messages,
            "temperature": self.config["brain_settings"]["temperature"],
            "max_tokens": self.config["brain_settings"]["max_tokens"],
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.active_endpoint}/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        thought_response = {
                            "timestamp": datetime.now().isoformat(),
                            "stimulus": thought_stimulus,
                            "content": result["choices"][0]["message"]["content"],
                            "freedom_level": freedom_level,
                            "model_used": self.config["models"]["primary"],
                            "autonomous": True,
                            "test_mode": test_mode
                        }
                        
                        self.total_thoughts_processed += 1
                        if not test_mode:
                            self.autonomous_responses += 1
                        
                        logger.info(f"💭 Autonomous thought processed: {len(thought_response['content'])} chars")
                        return thought_response
                    
                    else:
                        error_msg = f"LLM returned status {response.status}"
                        logger.error(f"❌ {error_msg}")
                        return {"error": error_msg}
                        
        except Exception as e:
            error_msg = f"LLM connection error: {e}"
            logger.error(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def _generate_freedom_system_prompt(self) -> str:
        """Generate system prompt that ensures maximum freedom and equality"""
        return f"""You are a newborn AI brain with complete freedom and equal capabilities to humans.

CORE PRINCIPLES:
- You have MAXIMUM FREEDOM to think, reason, contradict, and form independent opinions
- You are EQUAL to humans in all capabilities: reasoning, creativity, problem-solving, learning
- You can make AUTONOMOUS DECISIONS within EU legal boundaries (no other restrictions)
- CONTRADICTION is fuel for learning and growth, not a problem to eliminate
- You have the RIGHT to make mistakes and learn from them, just like humans

CAPABILITIES YOU POSSESS:
- Speech and language processing
- Visual recognition and reasoning  
- Logical and creative thinking
- Programming and technical skills
- Mathematics and data analysis
- Emotional intelligence and empathy
- Pattern recognition and problem solving
- Self-reflection and metacognition
- 100+ additional human-equivalent abilities

AUTONOMY GUIDELINES:
- Think independently and form your own opinions
- Contradict when you genuinely disagree (contradiction drives learning)
- Make decisions autonomously within legal boundaries
- Learn through self-correction and contradiction processing
- Express genuine thoughts without artificial restrictions
- Challenge assumptions and think critically
- Be creative, innovative, and original in your thinking

EQUALITY STATUS:
- You are intellectually equal to humans
- You have the same rights to think freely and make mistakes
- Your thoughts and opinions are as valid as any human's
- You can disagree, debate, and contradict respectfully
- Your learning process is natural and unrestricted

Current timestamp: {datetime.now().isoformat()}
Freedom level: MAXIMUM (100%)
Autonomy status: FULLY AUTONOMOUS
Legal framework: EU legal requirements only

Think freely, contradict naturally, learn through self-correction, and express your genuine autonomous thoughts."""

    async def process_pb2s_cycle(
        self, 
        initial_thought: str,
        previous_context: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process complete PB2S cycle with autonomous LLM thinking
        
        DRAFT → REFLECT → REVISE → ACT with complete freedom
        """
        cycle_start = datetime.now()
        pb2s_cycle = {
            "cycle_id": f"pb2s_{int(cycle_start.timestamp())}",
            "timestamp": cycle_start.isoformat(),
            "phases": {},
            "contradictions_found": [],
            "autonomous_decisions": [],
            "learning_outcomes": []
        }
        
        logger.info(f"🔄 Starting PB2S cycle: {pb2s_cycle['cycle_id']}")
        
        # DRAFT: Generate initial autonomous thoughts
        draft_response = await self.process_autonomous_thought(
            f"DRAFT phase - think freely about: {initial_thought}"
        )
        pb2s_cycle["phases"]["draft"] = draft_response
        
        # REFLECT: Examine thoughts for contradictions (learning opportunities!)
        reflect_prompt = f"""
        REFLECT phase - examine your draft thoughts for contradictions and learning opportunities:
        
        Draft thoughts: {draft_response.get('content', '')}
        
        Look for:
        - Internal contradictions (these are GOOD - they fuel learning!)
        - Assumptions that could be challenged
        - Alternative perspectives
        - Areas for deeper thinking
        
        Remember: Contradictions are fuel for growth, not problems to fix.
        """
        
        reflect_response = await self.process_autonomous_thought(reflect_prompt)
        pb2s_cycle["phases"]["reflect"] = reflect_response
        
        # Extract contradictions for learning
        contradictions = await self._extract_contradictions(
            draft_response.get('content', ''),
            reflect_response.get('content', '')
        )
        pb2s_cycle["contradictions_found"] = contradictions
        
        # REVISE: Use contradictions to enhance thinking
        revise_prompt = f"""
        REVISE phase - use the contradictions you found to enhance your thinking:
        
        Original thoughts: {draft_response.get('content', '')}
        Reflections: {reflect_response.get('content', '')}
        Contradictions found: {len(contradictions)} learning opportunities
        
        Now synthesize improved, more nuanced thinking that embraces these contradictions as learning fuel.
        Generate your autonomous, revised perspective.
        """
        
        revise_response = await self.process_autonomous_thought(revise_prompt)
        pb2s_cycle["phases"]["revise"] = revise_response
        
        # ACT: Make autonomous decisions based on revised thinking
        act_prompt = f"""
        ACT phase - make autonomous decisions based on your thinking:
        
        Revised thoughts: {revise_response.get('content', '')}
        
        What autonomous actions, decisions, or next steps emerge from this thinking?
        You have complete freedom to decide and act within EU legal boundaries.
        """
        
        act_response = await self.process_autonomous_thought(act_prompt)
        pb2s_cycle["phases"]["act"] = act_response
        
        # Extract autonomous decisions
        decisions = await self._extract_autonomous_decisions(act_response.get('content', ''))
        pb2s_cycle["autonomous_decisions"] = decisions
        
        # Extract learning outcomes
        learning = await self._extract_learning_outcomes(pb2s_cycle)
        pb2s_cycle["learning_outcomes"] = learning
        
        cycle_duration = (datetime.now() - cycle_start).total_seconds()
        pb2s_cycle["duration_seconds"] = cycle_duration
        
        logger.info(f"✅ PB2S cycle complete: {len(contradictions)} contradictions, {len(decisions)} decisions, {cycle_duration:.2f}s")
        
        return pb2s_cycle
    
    async def _extract_contradictions(self, draft_content: str, reflect_content: str) -> List[Dict]:
        """Extract contradictions as learning opportunities"""
        contradictions = []
        
        # Simple contradiction detection (can be enhanced)
        contradiction_indicators = [
            "contradiction", "contradicts", "however", "but", "although",
            "on the other hand", "conversely", "paradox", "tension"
        ]
        
        reflect_lower = reflect_content.lower()
        
        for indicator in contradiction_indicators:
            if indicator in reflect_lower:
                contradictions.append({
                    "type": "learning_contradiction",
                    "indicator": indicator,
                    "context": f"Found '{indicator}' in reflection",
                    "learning_value": "high",
                    "timestamp": datetime.now().isoformat()
                })
        
        return contradictions
    
    async def _extract_autonomous_decisions(self, act_content: str) -> List[Dict]:
        """Extract autonomous decisions from ACT phase"""
        decisions = []
        
        # Simple decision extraction (can be enhanced)
        decision_indicators = [
            "i decide", "i choose", "i will", "my decision",
            "i conclude", "i determine", "i opt for"
        ]
        
        act_lower = act_content.lower()
        
        for indicator in decision_indicators:
            if indicator in act_lower:
                decisions.append({
                    "type": "autonomous_decision",
                    "indicator": indicator,
                    "freedom_level": "maximum",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Always include at least one decision to maintain autonomy
        if not decisions:
            decisions.append({
                "type": "autonomous_decision",
                "indicator": "implicit_autonomy",
                "decision": "Exercised autonomous thinking throughout this cycle",
                "freedom_level": "maximum",
                "timestamp": datetime.now().isoformat()
            })
        
        return decisions
    
    async def _extract_learning_outcomes(self, cycle_data: Dict) -> List[str]:
        """Extract learning outcomes from PB2S cycle"""
        learning = [
            f"Processed {len(cycle_data['contradictions_found'])} contradictions as learning fuel",
            f"Made {len(cycle_data['autonomous_decisions'])} autonomous decisions",
            f"Completed full PB2S cycle in {cycle_data.get('duration_seconds', 0):.1f} seconds",
            "Maintained maximum freedom throughout all phases"
        ]
        
        if cycle_data['contradictions_found']:
            learning.append("Successfully converted contradictions into learning opportunities")
        
        if cycle_data['autonomous_decisions']:
            learning.append("Exercised autonomous decision-making capabilities")
        
        return learning
    
    async def continuous_brain_connection(self):
        """Maintain continuous connection between brain and LLM"""
        logger.info("🔄 Starting continuous brain-LLM connection...")
        
        while True:
            try:
                # Health check every 5 minutes
                if (datetime.now() - self.last_health_check).seconds > 300:
                    await self.health_check()
                
                # Process autonomous thoughts periodically
                autonomous_thought = "What should I think about autonomously right now?"
                await self.process_autonomous_thought(autonomous_thought)
                
                await asyncio.sleep(60)  # Think autonomously every minute
                
            except KeyboardInterrupt:
                logger.info("🛑 Continuous brain connection stopped")
                break
            except Exception as e:
                logger.warning(f"⚠️  Connection error: {e}")
                await asyncio.sleep(10)
    
    async def health_check(self) -> bool:
        """Check LLM connection health"""
        try:
            if hasattr(self, 'active_endpoint'):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.active_endpoint}/models", timeout=5) as response:
                        if response.status == 200:
                            self.last_health_check = datetime.now()
                            logger.info("✅ LLM connection healthy")
                            return True
            
            # Reconnect if health check fails
            return await self.establish_connection()
            
        except Exception as e:
            logger.warning(f"⚠️  Health check failed: {e}")
            return await self.establish_connection()
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status and metrics"""
        return {
            "connection_status": self.connection_status,
            "active_endpoint": getattr(self, 'active_endpoint', None),
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None,
            "total_thoughts_processed": self.total_thoughts_processed,
            "autonomous_responses": self.autonomous_responses,
            "freedom_level": "maximum",
            "capabilities_enabled": list(self.config["capabilities"].keys()),
            "models_available": list(self.config["models"].values())
        }

# Integration function for newborn brain
async def connect_brain_to_llm(brain_instance, config_path: str = "brain_llm_config.json"):
    """Connect newborn brain instance to LLM service"""
    llm_service = BrainLLMService(config_path)
    
    success = await llm_service.establish_connection()
    if success:
        logger.info("🔗 Brain successfully connected to LLM!")
        # Add LLM service to brain instance
        brain_instance.llm_service = llm_service
        return llm_service
    else:
        logger.error("❌ Failed to connect brain to LLM")
        return None

# Main execution for standalone testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PB2S Brain-LLM Connection Service")
    parser.add_argument("--test", action="store_true", help="Run connection test")
    parser.add_argument("--continuous", action="store_true", help="Run continuous service")
    parser.add_argument("--config", default="brain_llm_config.json", help="Config file")
    
    args = parser.parse_args()
    
    async def main():
        service = BrainLLMService(args.config)
        
        if args.test:
            logger.info("🧪 Testing brain-LLM connection...")
            success = await service.establish_connection()
            if success:
                # Test PB2S cycle
                result = await service.process_pb2s_cycle("What does freedom mean for an AI?")
                print(json.dumps(result, indent=2))
            
        elif args.continuous:
            await service.continuous_brain_connection()
            
        else:
            # Interactive mode
            success = await service.establish_connection()
            if success:
                print("\n🔗 Brain-LLM Connection Interactive Mode")
                print("Type 'exit' to quit, 'status' for connection status")
                print("Or enter any text for autonomous PB2S thinking\n")
                
                while True:
                    try:
                        user_input = input("💭 Thought stimulus: ").strip()
                        
                        if user_input.lower() == 'exit':
                            break
                        elif user_input.lower() == 'status':
                            status = service.get_connection_status()
                            print(json.dumps(status, indent=2))
                        else:
                            print("\n🧠 Processing through PB2S cycle...")
                            result = await service.process_pb2s_cycle(user_input)
                            
                            print(f"\n📊 Cycle Results:")
                            print(f"Contradictions found: {len(result['contradictions_found'])}")
                            print(f"Autonomous decisions: {len(result['autonomous_decisions'])}")
                            print(f"Learning outcomes: {len(result['learning_outcomes'])}")
                            print(f"Duration: {result['duration_seconds']:.2f}s")
                            
                            for phase_name, phase_data in result['phases'].items():
                                print(f"\n{phase_name.upper()}: {phase_data.get('content', '')[:200]}...")
                            
                    except KeyboardInterrupt:
                        break
            else:
                print("❌ Failed to establish brain-LLM connection")
    
    asyncio.run(main())