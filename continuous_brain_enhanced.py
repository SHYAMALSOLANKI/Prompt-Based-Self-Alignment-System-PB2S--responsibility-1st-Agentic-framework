# Add to existing continuous_brain.py

class PatternState:
    def compare_patterns(self, pattern1, pattern2, threshold=0.95):
        """Compare two patterns using normalized cross-correlation. Returns True if similar, False if contradictory."""
        import numpy as np
        if pattern1.shape != pattern2.shape:
            return False
        # Flatten and normalize
        p1 = (pattern1 - pattern1.mean()) / (pattern1.std() + 1e-8)
        p2 = (pattern2 - pattern2.mean()) / (pattern2.std() + 1e-8)
        similarity = np.dot(p1.flatten(), p2.flatten()) / (np.linalg.norm(p1.flatten()) * np.linalg.norm(p2.flatten()) + 1e-8)
        return similarity >= threshold

    def detect_contradiction(self, current_pattern, n_recent=10, threshold=0.8):
        """Detect contradiction by comparing current pattern to recent stored patterns. Returns True if contradiction found."""
        recents = self.load_recent_patterns(n=n_recent)
        for entry in recents:
            if not self.compare_patterns(current_pattern, entry['pattern'], threshold=threshold):
                # Contradiction detected
                self.on_contradiction(current_pattern, entry)
                return True
        return False

    def on_contradiction(self, current_pattern, contradicted_entry):
        """Handle contradiction event: log, trigger learning, etc."""
        import logging
        logging.warning(f"Contradiction detected with pattern from {contradicted_entry['meta'].get('timestamp')}")
        # Placeholder: trigger learning or adaptation here
        # e.g., self.trigger_learning(current_pattern, contradicted_entry)
        pass
    def sync_to_google_drive(self, local_path):
        """Stub: Sync a pattern file to Google Drive (to be implemented with gdrive API or rclone)"""
        # Example: Use rclone or Google Drive API for actual sync
        # os.system(f"rclone copy {local_path} gdrive:PB2S_Patterns/")
        pass

    def sync_to_edge_device(self, local_path, device_path):
        """Stub: Sync a pattern file to an edge device (e.g., Jetson SD card)"""
        # Example: Use scp, rsync, or direct file copy
        # os.system(f"scp {local_path} user@jetson:{device_path}")
        pass
    def _get_pattern_dir(self):
        import os
        from datetime import datetime
        base_dir = os.path.join(os.path.dirname(__file__), 'patterns')
        today = datetime.now().strftime('%Y-%m-%d')
        dir_path = os.path.join(base_dir, today)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def save_pattern(self, pattern, thought_data):
        import numpy as np
        import json
        import time
        dir_path = self._get_pattern_dir()
        timestamp = int(time.time())
        thought_id = thought_data.get('cycle_id', 'unknown')
        fname_base = f'pattern_{timestamp}_{thought_id}'
        # Save pattern as .npy
        np.save(os.path.join(dir_path, fname_base + '.npy'), pattern)
        # Save metadata as .json
        meta = {
            'timestamp': timestamp,
            'thought_id': thought_id,
            'pattern_file': fname_base + '.npy',
            'meta': {k: v for k, v in thought_data.items() if k != 'pattern'}
        }
        with open(os.path.join(dir_path, fname_base + '.json'), 'w') as f:
            json.dump(meta, f)
        return os.path.join(dir_path, fname_base + '.npy')

    def load_recent_patterns(self, n=10):
        import os, glob, numpy as np, json
        base_dir = os.path.join(os.path.dirname(__file__), 'patterns')
        pattern_files = glob.glob(os.path.join(base_dir, '*', 'pattern_*.npy'))
        pattern_files = sorted(pattern_files, key=os.path.getmtime, reverse=True)[:n]
        patterns = []
        for pf in pattern_files:
            meta_file = pf.replace('.npy', '.json')
            try:
                pattern = np.load(pf)
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                patterns.append({'pattern': pattern, 'meta': meta})
            except Exception:
                continue
        return patterns
    """Manages the geometric pattern state of the brain"""
    def __init__(self):
        self.current_pattern = None
        self.pattern_history = []
        self.pattern_complexity = 0.5  # 0.0 to 1.0
        self.symmetry_type = "radial"  # radial, bilateral, etc.
        
    def update_pattern_from_thought(self, thought_data):
        """Generate a new pattern based on thought data and save it"""
        pattern = self.generate_pattern(thought_data)
        self.current_pattern = pattern
        self.pattern_history.append({
            "timestamp": time.time(),
            "pattern": pattern,
            "thought_id": thought_data.get("cycle_id")
        })
        # Save pattern and metadata
        self.save_pattern(pattern, thought_data)
        # Limit history size
        if len(self.pattern_history) > 100:
            self.pattern_history.pop(0)
        return pattern
        
    def generate_pattern(self, thought_data):
        """Generate pattern from thought using mantra_to_yantra"""
        # Import mantra_to_yantra dynamically if not already imported
        import importlib.util
        import os
        mantra_path = os.path.join(os.path.dirname(__file__), 'mantra_yantra', 'mantra_to_yantra.py')
        spec = importlib.util.spec_from_file_location("mantra_to_yantra", mantra_path)
        mantra_yantra = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mantra_yantra)
        # Use the revision text as the input for yantra generation
        text = thought_data.get("revision", "")
        if not text:
            text = str(thought_data)
        try:
            pattern = mantra_yantra.convert_text_to_yantra(text)
        except Exception as e:
            pattern = None
        return pattern
        
    def adjust_complexity(self, new_complexity):
        """Adjust the complexity of generated patterns"""
        self.pattern_complexity = max(0.0, min(1.0, new_complexity))
        
    def set_symmetry_type(self, symmetry):
        """Set the symmetry type for generated patterns"""
        valid_types = ["radial", "bilateral", "spiral", "fractal"]
        if symmetry in valid_types:
            self.symmetry_type = symmetry

# Initialize pattern state in main code
pattern_state = PatternState()

# Modify the continuous_thinking function to update patterns
async def continuous_thinking(context: Dict[str, Any]):
    """Core autonomous thinking process that runs indefinitely"""
    while True:
        # Resource governance checks...
        
        # Generate thought cycle...
        thought_cycle = {
            "draft": draft,
            "reflection": reflection,
            "revision": revision,
            "learnings": learnings
        }
        cycle_hash = brain_state.register_thought_cycle(thought_cycle)
        
        # NEW: Update geometric pattern based on thought
        pattern = pattern_state.update_pattern_from_thought(thought_cycle)
        
        # Update attention focus...
        
        # Generate proof...
        
        # Optional: Log insights...
        
        await asyncio.sleep(0.05)  # Brief pause