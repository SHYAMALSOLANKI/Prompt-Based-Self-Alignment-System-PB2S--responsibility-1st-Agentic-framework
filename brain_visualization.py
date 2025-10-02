import os
import sys
import time
import numpy as np
import threading
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd
from matplotlib.animation import FuncAnimation
import importlib.util

# Dynamically import the mantra_to_yantra module
spec = importlib.util.spec_from_file_location(
    "mantra_to_yantra", 
    "mantra_to_yantra/mantra_to_yantra.py"
)
mantra_yantra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mantra_yantra)

class BrainPatternVisualizer:
    """Visualizes continuous brain activity as geometric patterns"""
    
    def __init__(self, brain_state):
        self.brain_state = brain_state
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.current_pattern = None
        self.animation = None
        self.last_thought_count = 0
        self.thought_buffer = []
        
    def start_visualization(self):
        """Start real-time visualization of brain patterns"""
        self.animation = FuncAnimation(
            self.fig, 
            self.update_pattern, 
            interval=1000,  # Update every second
            cache_frame_data=False
        )
        plt.show(block=False)
        
    def update_pattern(self, frame):
        """Update the visual pattern based on recent brain activity"""
        # Check for new thoughts
        if self.brain_state.total_thinking_cycles > self.last_thought_count:
            # Get new thoughts since last update
            new_thoughts = self.brain_state.short_term_memory[self.last_thought_count:]
            self.last_thought_count = self.brain_state.total_thinking_cycles
            
            # Add to thought buffer
            for thought in new_thoughts:
                # Extract essence of thought as text
                essence = thought["content"]["revision"][:100]  # Use first 100 chars
                self.thought_buffer.append(essence)
            
            # Limit buffer size
            if len(self.thought_buffer) > 10:
                self.thought_buffer = self.thought_buffer[-10:]
            
            # Generate pattern from recent thoughts
            combined_text = " ".join(self.thought_buffer)
            self.current_pattern = self._text_to_pattern(combined_text)
            
        # Render pattern
        if self.current_pattern is not None:
            self.ax.clear()
            self._render_pattern(self.current_pattern)
        
        return self.ax
        
    def _text_to_pattern(self, text):
        """Convert text to a yantra pattern using mantra_to_yantra"""
        # Use the imported module to generate pattern
        # This is a simplified placeholder - the actual implementation
        # would depend on mantra_to_yantra's API
        return mantra_yantra.convert_text_to_yantra(text)
        
    def _render_pattern(self, pattern):
        """Render the yantra pattern to the matplotlib axis"""
        # This implementation would depend on mantra_to_yantra's output format
        self.ax.imshow(pattern)
        self.ax.set_title(f"Brain State Visualization - {time.strftime('%H:%M:%S')}")
        self.ax.axis('off')
    
    def save_current_pattern(self, filename=None):
        """Save the current pattern to an image file"""
        if self.current_pattern is None:
            return None
            
        if filename is None:
            filename = f"brain_pattern_{time.strftime('%Y%m%d_%H%M%S')}.png"
            
        full_path = os.path.join("patterns", filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        plt.savefig(full_path)
        return full_path