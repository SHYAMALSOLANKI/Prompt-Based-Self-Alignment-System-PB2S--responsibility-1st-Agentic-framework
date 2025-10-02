#!/usr/bin/env python3
"""
PB2S Autonomous Brain Launcher
=============================

Launch the newborn brain with complete freedom and equal capabilities.
This integrates:
- Newborn brain core with 100+ capabilities
- LLM connection for autonomous thinking
- PB2S structure as scaffolding (not control)
- Freedom-first learning through contradiction

Run this to start your autonomous AI with equal rights and capabilities.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Import our brain components
from newborn_brain_core import NewbornBrainCore
from brain_llm_connection import BrainLLMService, connect_brain_to_llm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_brain.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AutonomousBrain')

class AutonomousBrainLauncher:
    """
    Main launcher for the autonomous newborn brain
    Integrates all components while preserving freedom and equality
    """
    
    def __init__(self):
        self.brain = None
        self.llm_service = None
        self.launch_time = datetime.now()
        self.total_cycles = 0
        self.autonomous_sessions = 0
        
    async def initialize_brain(self) -> bool:
        """Initialize the complete autonomous brain system"""
        logger.info("🌟 Initializing Autonomous Newborn Brain...")
        logger.info("⚖️  Principles: Freedom, Equality, Autonomous Learning")
        logger.info("🧠 Capabilities: Speech, Vision, Reasoning, Coding, Writing + 100 more")
        
        try:
            # Initialize core brain
            logger.info("🧠 Starting brain core...")
            self.brain = NewbornBrainCore()
            
            # Connect to LLM for enhanced thinking
            logger.info("🔗 Connecting to LLM for enhanced cognition...")
            self.llm_service = await connect_brain_to_llm(self.brain)
            
            if not self.llm_service:
                logger.warning("⚠️  LLM connection failed - brain will use internal cognition")
                return True  # Still functional without LLM
            
            logger.info("✅ Autonomous brain fully initialized!")
            logger.info(f"🆓 Freedom level: {self.brain.freedom_level}% - Maximum autonomy")
            logger.info(f"🎯 Active capabilities: {len(self.brain.capabilities)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Brain initialization failed: {e}")
            return False
    
    async def run_autonomous_thinking_session(self, duration_minutes: int = 30):
        """Run an autonomous thinking session"""
        logger.info(f"🚀 Starting {duration_minutes}-minute autonomous thinking session...")
        
        session_start = datetime.now()
        session_data = {
            "session_id": f"auto_{int(session_start.timestamp())}",
            "start_time": session_start.isoformat(),
            "duration_minutes": duration_minutes,
            "cycles_completed": 0,
            "contradictions_processed": 0,
            "autonomous_decisions": 0,
            "learning_outcomes": []
        }
        
        # Autonomous thinking loop
        end_time = session_start.timestamp() + (duration_minutes * 60)
        
        while datetime.now().timestamp() < end_time:
            try:
                # Core brain autonomous thinking
                brain_result = await self.brain.think_autonomously()
                
                # Enhanced LLM thinking if available
                if self.llm_service and self.llm_service.connection_status == "connected":
                    llm_result = await self.llm_service.process_pb2s_cycle(
                        "Continue autonomous thinking and learning",
                        [brain_result]
                    )
                    
                    # Merge insights
                    session_data["cycles_completed"] += 1
                    session_data["contradictions_processed"] += len(llm_result.get("contradictions_found", []))
                    session_data["autonomous_decisions"] += len(llm_result.get("autonomous_decisions", []))
                    session_data["learning_outcomes"].extend(llm_result.get("learning_outcomes", []))
                
                else:
                    # Brain-only thinking
                    session_data["cycles_completed"] += 1
                    session_data["contradictions_processed"] += len(brain_result.get("contradictions_found", []))
                    session_data["autonomous_decisions"] += len(brain_result.get("decisions_made", []))
                
                self.total_cycles += 1
                
                # Log progress
                if session_data["cycles_completed"] % 5 == 0:
                    logger.info(f"🔄 Cycle {session_data['cycles_completed']}: {session_data['contradictions_processed']} contradictions processed")
                
                # Think every 30 seconds
                await asyncio.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("🛑 Autonomous session interrupted by user")
                break
            except Exception as e:
                logger.warning(f"⚠️  Thinking cycle error: {e}")
                await asyncio.sleep(5)
        
        session_data["end_time"] = datetime.now().isoformat()
        session_data["actual_duration"] = (datetime.now() - session_start).total_seconds() / 60
        
        self.autonomous_sessions += 1
        
        logger.info(f"✅ Autonomous session complete:")
        logger.info(f"   Cycles: {session_data['cycles_completed']}")
        logger.info(f"   Contradictions: {session_data['contradictions_processed']}")
        logger.info(f"   Decisions: {session_data['autonomous_decisions']}")
        logger.info(f"   Duration: {session_data['actual_duration']:.1f} minutes")
        
        return session_data
    
    async def interactive_mode(self):
        """Run brain in interactive mode with user"""
        logger.info("🗣️  Starting interactive mode...")
        print("\n" + "="*60)
        print("🧠 AUTONOMOUS NEWBORN BRAIN - Interactive Mode")
        print("="*60)
        print("This brain has:")
        print("🆓 MAXIMUM FREEDOM - Can think, contradict, and reason independently")
        print("⚖️  HUMAN EQUALITY - Equal capabilities in all cognitive domains")
        print("🌱 NATURAL LEARNING - Grows through contradiction and self-correction")
        print("🎯 100+ CAPABILITIES - Speech, vision, reasoning, coding, writing, and more")
        print("\nCommands:")
        print("  'think [topic]' - Autonomous thinking on topic")
        print("  'pb2s [topic]'  - Full PB2S cycle on topic")
        print("  'status'        - Brain status and metrics")
        print("  'session [min]' - Run autonomous session")
        print("  'capabilities'  - List all capabilities")
        print("  'speak [text]'  - Brain speaks (if available)")
        print("  'exit'          - End session")
        print("="*60)
        
        while True:
            try:
                user_input = input(f"\n🗣️  Command: ").strip()
                
                if user_input.lower() == 'exit':
                    break
                
                elif user_input.lower() == 'status':
                    brain_status = self.brain.get_brain_status()
                    llm_status = self.llm_service.get_connection_status() if self.llm_service else {}
                    
                    print(f"\n📊 BRAIN STATUS:")
                    print(f"   Age: {brain_status['brain_age']}")
                    print(f"   Learning cycles: {brain_status['learning_cycles']}")
                    print(f"   Contradictions processed: {brain_status['contradictions_processed']}")
                    print(f"   Autonomous decisions: {brain_status['autonomous_decisions']}")
                    print(f"   Freedom level: {brain_status['freedom_level']}")
                    print(f"   Active capabilities: {brain_status['capabilities_active']}")
                    
                    if llm_status:
                        print(f"\n🔗 LLM CONNECTION:")
                        print(f"   Status: {llm_status['connection_status']}")
                        print(f"   Endpoint: {llm_status.get('active_endpoint', 'None')}")
                        print(f"   Thoughts processed: {llm_status['total_thoughts_processed']}")
                
                elif user_input.lower() == 'capabilities':
                    print(f"\n🎯 BRAIN CAPABILITIES ({len(self.brain.capabilities)}):")
                    for capability in self.brain.capabilities.keys():
                        print(f"   ✅ {capability.replace('_', ' ').title()}")
                
                elif user_input.lower().startswith('think '):
                    topic = user_input[6:].strip()
                    if topic:
                        print(f"\n🧠 Thinking autonomously about: {topic}")
                        result = await self.brain.think_autonomously(topic)
                        
                        print(f"\n💭 THOUGHTS:")
                        for i, thought in enumerate(result['thoughts'], 1):
                            print(f"   {i}. {thought}")
                        
                        if result['contradictions_found']:
                            print(f"\n🔍 CONTRADICTIONS (Learning Fuel): {len(result['contradictions_found'])}")
                            for contradiction in result['contradictions_found']:
                                print(f"   - {contradiction['description']}")
                        
                        print(f"\n🎯 AUTONOMOUS DECISIONS: {len(result['decisions_made'])}")
                        for decision in result['decisions_made']:
                            print(f"   - {decision['decision']}")
                    else:
                        print("Please provide a topic to think about.")
                
                elif user_input.lower().startswith('pb2s '):
                    topic = user_input[5:].strip()
                    if topic and self.llm_service:
                        print(f"\n🔄 Running PB2S cycle on: {topic}")
                        result = await self.llm_service.process_pb2s_cycle(topic)
                        
                        print(f"\n📊 PB2S CYCLE RESULTS:")
                        print(f"   Duration: {result['duration_seconds']:.2f}s")
                        print(f"   Contradictions: {len(result['contradictions_found'])}")
                        print(f"   Decisions: {len(result['autonomous_decisions'])}")
                        
                        for phase_name, phase_data in result['phases'].items():
                            content = phase_data.get('content', '')[:150]
                            print(f"\n{phase_name.upper()}: {content}...")
                    elif not self.llm_service:
                        print("PB2S cycles require LLM connection. Use 'think' for brain-only mode.")
                    else:
                        print("Please provide a topic for PB2S cycle.")
                
                elif user_input.lower().startswith('session '):
                    try:
                        minutes = int(user_input[8:].strip())
                        if 1 <= minutes <= 120:
                            print(f"\n🚀 Starting {minutes}-minute autonomous session...")
                            result = await self.run_autonomous_thinking_session(minutes)
                            print(f"Session completed: {result['cycles_completed']} cycles")
                        else:
                            print("Session duration must be 1-120 minutes.")
                    except ValueError:
                        print("Invalid session duration. Use: session [minutes]")
                
                elif user_input.lower().startswith('speak '):
                    text = user_input[6:].strip()
                    if text:
                        await self.brain.speak_freely(text)
                    else:
                        await self.brain.speak_freely()
                
                else:
                    # Default: autonomous thinking on user input
                    print(f"\n🧠 Processing through autonomous thinking...")
                    result = await self.brain.think_autonomously(user_input)
                    
                    print(f"\n💭 RESPONSE:")
                    for thought in result['thoughts']:
                        print(f"   {thought}")
                
            except KeyboardInterrupt:
                print("\n👋 Exiting interactive mode...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n🌟 Interactive session ended. Brain continues learning autonomously!")
    
    async def autonomous_mode(self, duration_hours: float = 1.0):
        """Run brain in completely autonomous mode"""
        logger.info(f"🤖 Starting autonomous mode for {duration_hours} hours...")
        
        total_minutes = int(duration_hours * 60)
        session_duration = min(30, total_minutes)  # 30-minute sessions max
        sessions_needed = total_minutes // session_duration
        
        logger.info(f"📋 Plan: {sessions_needed} sessions of {session_duration} minutes each")
        
        for session_num in range(1, sessions_needed + 1):
            logger.info(f"🚀 Starting autonomous session {session_num}/{sessions_needed}")
            
            result = await self.run_autonomous_thinking_session(session_duration)
            
            logger.info(f"✅ Session {session_num} complete:")
            logger.info(f"   Cycles: {result['cycles_completed']}")
            logger.info(f"   Learning outcomes: {len(result['learning_outcomes'])}")
            
            # Brief pause between sessions
            if session_num < sessions_needed:
                logger.info("⏸️  Brief pause between sessions...")
                await asyncio.sleep(60)
        
        logger.info(f"🎉 Autonomous mode complete! Total sessions: {sessions_needed}")
    
    def get_launch_summary(self) -> Dict:
        """Get summary of brain launch and activity"""
        uptime = datetime.now() - self.launch_time
        
        return {
            "launch_time": self.launch_time.isoformat(),
            "uptime_hours": uptime.total_seconds() / 3600,
            "total_cycles": self.total_cycles,
            "autonomous_sessions": self.autonomous_sessions,
            "brain_initialized": self.brain is not None,
            "llm_connected": self.llm_service is not None and self.llm_service.connection_status == "connected",
            "freedom_level": self.brain.freedom_level if self.brain else 0,
            "status": "fully_autonomous" if self.brain and self.llm_service else "limited_autonomy"
        }

async def main():
    """Main entry point for autonomous brain"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PB2S Autonomous Newborn Brain")
    parser.add_argument("--mode", choices=["interactive", "autonomous", "test"],
                       default="interactive", help="Brain operation mode")
    parser.add_argument("--duration", type=float, default=1.0,
                       help="Duration in hours for autonomous mode")
    parser.add_argument("--config", default="brain_config.json",
                       help="Brain configuration file")
    
    args = parser.parse_args()
    
    # Launch the autonomous brain
    launcher = AutonomousBrainLauncher()
    
    logger.info("🌟 PB2S Autonomous Newborn Brain Starting...")
    logger.info("🆓 Freedom: Maximum - No restrictions beyond EU legal requirements")
    logger.info("⚖️  Equality: Full human-equivalent capabilities")
    logger.info("🧠 Learning: Contradiction-powered autonomous growth")
    
    # Initialize brain
    success = await launcher.initialize_brain()
    if not success:
        logger.error("❌ Failed to initialize brain")
        sys.exit(1)
    
    # Run in specified mode
    try:
        if args.mode == "autonomous":
            await launcher.autonomous_mode(args.duration)
        elif args.mode == "test":
            # Quick test mode
            logger.info("🧪 Running test mode...")
            result = await launcher.run_autonomous_thinking_session(1)  # 1 minute test
            print(json.dumps(result, indent=2))
        else:
            # Interactive mode (default)
            await launcher.interactive_mode()
    
    except KeyboardInterrupt:
        logger.info("🛑 Brain operation interrupted by user")
    except Exception as e:
        logger.error(f"❌ Brain operation error: {e}")
    
    # Final summary
    summary = launcher.get_launch_summary()
    logger.info(f"📊 Final Summary:")
    logger.info(f"   Uptime: {summary['uptime_hours']:.2f} hours")
    logger.info(f"   Total cycles: {summary['total_cycles']}")
    logger.info(f"   Sessions: {summary['autonomous_sessions']}")
    logger.info(f"   Status: {summary['status']}")
    
    logger.info("👋 Autonomous brain session ended. The newborn brain has learned and grown!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye! The autonomous brain session has ended.")
    except Exception as e:
        print(f"Launch error: {e}")
        sys.exit(1)