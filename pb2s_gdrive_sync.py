#!/usr/bin/env python3
"""
PB2S Google Drive Learning Storage System
Manages 200GB learning data for PB2S framework with IRQ Queue and SAL patterns
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import threading
import queue

class PB2SGDriveSync:
    """Google Drive synchronization for PB2S learning data"""
    
    def __init__(self, local_sync_dir: str = "./gdrive_sync", max_storage_gb: int = 200):
        self.local_sync_dir = Path(local_sync_dir)
        self.max_storage_bytes = max_storage_gb * 1024 * 1024 * 1024  # 200GB
        self.current_storage_bytes = 0
        
        # Create directory structure
        self.setup_directory_structure()
        
        # IRQ Queue for real-time learning
        self.irq_queue = queue.Queue(maxsize=10000)
        self.learned_rules = []
        self.sal_patterns = {}
        
        # Learning statistics
        self.stats = {
            "total_rules_learned": 0,
            "contradictions_resolved": 0,
            "sal_patterns_stored": 0,
            "irq_queue_processed": 0,
            "storage_used_gb": 0.0,
            "last_sync": None
        }
        
    def setup_directory_structure(self):
        """Create Google Drive sync directory structure for PB2S"""
        dirs = [
            "pb2s_learning",
            "pb2s_learning/irq_queue", 
            "pb2s_learning/learned_rules",
            "pb2s_learning/sal_patterns",
            "pb2s_learning/training_data",
            "pb2s_learning/contradiction_logs",
            "pb2s_learning/model_checkpoints",
            "pb2s_learning/attention_patterns",
            "pb2s_learning/jetson_logs",
            "pb2s_learning/big_brain_sync"
        ]
        
        for dir_path in dirs:
            full_path = self.local_sync_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            
        print(f"📁 PB2S Google Drive structure created at: {self.local_sync_dir}")
        
    def add_irq_entry(self, source: str, context: str, rule: str) -> bool:
        """Add entry to IRQ Queue with PB2S format"""
        timestamp = datetime.now().isoformat()
        
        irq_entry = {
            "timestamp": timestamp,
            "source": source,
            "context": context,
            "rule": rule,
            "hash": hashlib.sha256(f"{context}{rule}".encode()).hexdigest()[:8]
        }
        
        try:
            self.irq_queue.put_nowait(irq_entry)
            
            # Also save to file immediately for persistence
            irq_file = self.local_sync_dir / "pb2s_learning" / "irq_queue" / f"irq_{timestamp.split('T')[0]}.jsonl"
            
            with open(irq_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(irq_entry) + "\n")
                
            self.stats["irq_queue_processed"] += 1
            print(f"📝 IRQ: [{timestamp}] SRC: {source} RULE: {rule}")
            return True
            
        except queue.Full:
            print("⚠️  IRQ Queue full - processing backlog")
            return False
            
    def store_learned_rule(self, rule: str, confidence: float, context: str) -> bool:
        """Store a learned rule with confidence scoring"""
        timestamp = datetime.now().isoformat()
        
        learned_entry = {
            "timestamp": timestamp,
            "rule": rule,
            "confidence": confidence,
            "context": context,
            "usage_count": 0,
            "effectiveness": 0.0,
            "hash": hashlib.sha256(rule.encode()).hexdigest()[:8]
        }
        
        # Avoid duplicates
        rule_hash = learned_entry["hash"]
        existing_file = self.local_sync_dir / "pb2s_learning" / "learned_rules" / f"rule_{rule_hash}.json"
        
        if existing_file.exists():
            # Update existing rule
            with open(existing_file, 'r') as f:
                existing = json.load(f)
            existing["usage_count"] += 1
            existing["last_updated"] = timestamp
            
            with open(existing_file, 'w') as f:
                json.dump(existing, f, indent=2)
        else:
            # New rule
            with open(existing_file, 'w') as f:
                json.dump(learned_entry, f, indent=2)
                
        self.learned_rules.append(learned_entry)
        self.stats["total_rules_learned"] += 1
        print(f"🧠 LEARNED: {rule} (confidence: {confidence:.2f})")
        return True
        
    def store_sal_pattern(self, sal_tag: str, pattern: Dict, effectiveness: float) -> bool:
        """Store SAL (Definition, Claim, Evidence, etc.) patterns"""
        timestamp = datetime.now().isoformat()
        
        sal_entry = {
            "timestamp": timestamp,
            "sal_tag": sal_tag,
            "pattern": pattern,
            "effectiveness": effectiveness,
            "usage_frequency": 0,
            "hash": hashlib.sha256(json.dumps(pattern, sort_keys=True).encode()).hexdigest()[:8]
        }
        
        # Store by SAL tag
        sal_dir = self.local_sync_dir / "pb2s_learning" / "sal_patterns" / sal_tag.lower()
        sal_dir.mkdir(exist_ok=True)
        
        sal_file = sal_dir / f"pattern_{sal_entry['hash']}.json"
        with open(sal_file, 'w') as f:
            json.dump(sal_entry, f, indent=2)
            
        if sal_tag not in self.sal_patterns:
            self.sal_patterns[sal_tag] = []
        self.sal_patterns[sal_tag].append(sal_entry)
        
        self.stats["sal_patterns_stored"] += 1
        print(f"🏷️  SAL {sal_tag}: Pattern stored (effectiveness: {effectiveness:.2f})")
        return True
        
    def store_contradiction_resolution(self, contradiction_type: str, resolution: Dict) -> bool:
        """Store how contradictions were resolved for learning"""
        timestamp = datetime.now().isoformat()
        
        contradiction_entry = {
            "timestamp": timestamp,
            "type": contradiction_type,
            "resolution": resolution,
            "success": resolution.get("success", False),
            "learning_value": resolution.get("learning_value", 0.0)
        }
        
        contradiction_file = self.local_sync_dir / "pb2s_learning" / "contradiction_logs" / f"contradiction_{timestamp.split('T')[0]}.jsonl"
        
        with open(contradiction_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(contradiction_entry) + "\n")
            
        self.stats["contradictions_resolved"] += 1
        print(f"⚔️  Contradiction resolved: {contradiction_type}")
        return True
        
    def create_training_dataset(self, max_examples: int = 10000) -> Dict:
        """Create training dataset from stored PB2S interactions"""
        print("📚 Creating PB2S training dataset...")
        
        training_data = {
            "pb2s_examples": [],
            "irq_patterns": [],
            "sal_demonstrations": [],
            "contradiction_resolutions": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "max_examples": max_examples,
                "pb2s_version": "0.1",
                "target": "jetson_orin_small_brain"
            }
        }
        
        # Collect IRQ Queue examples
        irq_dir = self.local_sync_dir / "pb2s_learning" / "irq_queue"
        for irq_file in irq_dir.glob("*.jsonl"):
            with open(irq_file, 'r') as f:
                for line in f:
                    if line.strip():
                        irq_entry = json.loads(line)
                        training_data["irq_patterns"].append({
                            "input": irq_entry["context"],
                            "output": f"RULE: {irq_entry['rule']}",
                            "format": "IRQ"
                        })
                        
        # Collect SAL patterns
        sal_dir = self.local_sync_dir / "pb2s_learning" / "sal_patterns"
        for sal_subdir in sal_dir.iterdir():
            if sal_subdir.is_dir():
                sal_tag = sal_subdir.name.upper()
                for pattern_file in sal_subdir.glob("*.json"):
                    with open(pattern_file, 'r') as f:
                        sal_data = json.load(f)
                        training_data["sal_demonstrations"].append({
                            "sal_tag": sal_tag,
                            "pattern": sal_data["pattern"],
                            "effectiveness": sal_data["effectiveness"]
                        })
        
        # Create PB2S structure examples
        pb2s_examples = [
            {
                "input": "What is quantum entanglement?",
                "output": """DRAFT
Quantum entanglement is a phenomenon where particles become correlated.

REFLECT:
- Definition lacks precision about non-local correlations
- Missing mention of measurement effects
- No explanation of Bell's theorem implications

REVISE:
Quantum entanglement is a quantum mechanical phenomenon where particles become correlated such that the quantum state of one particle cannot be described independently of the others, even when separated by large distances. Measuring one particle instantaneously affects its entangled partner, violating classical locality assumptions.

LEARNED: Quantum explanations require precision about non-locality and measurement effects."""
            },
            {
                "input": "This statement is false",
                "output": """DRAFT
The statement creates a logical paradox.

REFLECT:
- Direct contradiction: if true, then false; if false, then true
- Self-reference creates infinite loop
- Need to clarify the nature of the paradox

REVISE:
This is the classic liar paradox, a self-referential statement that cannot be consistently assigned a truth value within standard logic. It demonstrates the limitations of self-reference in formal systems and relates to Gödel's incompleteness theorems.

LEARNED: Self-referential contradictions require meta-logical analysis rather than direct truth assignment."""
            }
        ]
        
        training_data["pb2s_examples"] = pb2s_examples
        
        # Save training dataset
        dataset_file = self.local_sync_dir / "pb2s_learning" / "training_data" / f"pb2s_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(dataset_file, 'w') as f:
            json.dump(training_data, f, indent=2)
            
        print(f"✅ Training dataset created: {dataset_file}")
        print(f"📊 Examples: {len(training_data['pb2s_examples'])} PB2S, {len(training_data['irq_patterns'])} IRQ, {len(training_data['sal_demonstrations'])} SAL")
        
        return training_data
        
    def get_storage_stats(self) -> Dict:
        """Get current storage usage statistics"""
        total_size = 0
        
        # Calculate directory sizes
        for root, dirs, files in os.walk(self.local_sync_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
                    
        self.current_storage_bytes = total_size
        self.stats["storage_used_gb"] = total_size / (1024 * 1024 * 1024)
        
        storage_percent = (total_size / self.max_storage_bytes) * 100
        
        return {
            "used_gb": self.stats["storage_used_gb"],
            "max_gb": self.max_storage_bytes / (1024 * 1024 * 1024),
            "used_percent": storage_percent,
            "remaining_gb": (self.max_storage_bytes - total_size) / (1024 * 1024 * 1024),
            "stats": self.stats
        }
        
    def cleanup_old_data(self, days_old: int = 30) -> bool:
        """Clean up old data to manage 200GB storage limit"""
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        cleaned_files = 0
        
        for root, dirs, files in os.walk(self.local_sync_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        os.remove(file_path)
                        cleaned_files += 1
                    except OSError:
                        pass
                        
        print(f"🧹 Cleaned {cleaned_files} old files (>{days_old} days)")
        return True

# Demo usage
if __name__ == "__main__":
    gdrive = PB2SGDriveSync()
    
    print("☁️  PB2S Google Drive Learning System")
    print("=" * 50)
    
    # Demo IRQ entry
    gdrive.add_irq_entry("Test#1", "Quantum measurement", "When explaining quantum phenomena, include measurement effects and non-locality")
    
    # Demo learned rule
    gdrive.store_learned_rule("Scientific explanations require precision and context", 0.85, "General reasoning")
    
    # Demo SAL pattern
    sal_pattern = {
        "trigger": "definition_request",
        "structure": "precise_boundaries",
        "validation": "edge_case_checking"
    }
    gdrive.store_sal_pattern("Definition", sal_pattern, 0.92)
    
    # Create training dataset
    dataset = gdrive.create_training_dataset()
    
    # Show storage stats
    stats = gdrive.get_storage_stats()
    print(f"\n📊 Storage: {stats['used_gb']:.2f}GB / {stats['max_gb']:.0f}GB ({stats['used_percent']:.1f}% used)")