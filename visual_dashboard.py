import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import threading
import io
from PIL import Image
import sounddevice as sd
from scipy.io.wavfile import write as write_wav
import base64
import importlib.util

# Import our brain components
from continuous_brain import brain_state
from brain_visualization import BrainPatternVisualizer

# Load mantra_to_yantra dynamically
spec = importlib.util.spec_from_file_location(
    "mantra_to_yantra", 
    "mantra_to_yantra/mantra_to_yantra.py"
)
mantra_yantra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mantra_yantra)

# Initialize visualizer
visualizer = BrainPatternVisualizer(brain_state)

def main():
    st.title("PB2S Autonomous Brain Visualization")
    
    st.sidebar.header("Controls")
    visualization_mode = st.sidebar.selectbox(
        "Visualization Mode",
        ["Real-time Patterns", "Thought Stream", "Voice Input"]
    )
    
    if visualization_mode == "Real-time Patterns":
        real_time_patterns()
    elif visualization_mode == "Thought Stream":
        thought_stream()
    elif visualization_mode == "Voice Input":
        voice_input()
        
def real_time_patterns():
    st.header("Real-time Brain Patterns")
    st.write("""
    This view shows the geometric patterns generated from the autonomous brain's
    continuous thinking process. The patterns evolve as new thoughts emerge.
    """)
    
    pattern_placeholder = st.empty()
    
    # Button to capture current pattern
    if st.button("Save Current Pattern"):
        path = visualizer.save_current_pattern()
        if path:
            st.success(f"Pattern saved to {path}")
    
    # Auto-refresh the pattern
    while True:
        # Generate pattern image from current brain state
        fig = plt.figure(figsize=(10, 10))
        if visualizer.current_pattern is not None:
            plt.imshow(visualizer.current_pattern)
        plt.axis('off')
        
        # Convert to image and display
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pattern_placeholder.image(buf)
        plt.close(fig)
        
        # Update every 2 seconds
        time.sleep(2)
        
def thought_stream():
    st.header("Continuous Thought Stream")
    st.write("""
    This view shows the continuous stream of thoughts from the autonomous brain,
    with corresponding pattern snippets for each thought transition.
    """)
    
    # Display recent thoughts with mini-patterns
    thoughts = brain_state.short_term_memory[-10:]
    
    for i, thought in enumerate(thoughts):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Display thought text
            st.subheader(f"Thought #{thought['cycle_id']}")
            st.write(thought['content']['revision'][:200] + "...")
            st.caption(f"Attention: {', '.join(thought['attention_state'])}")
            
        with col2:
            # Generate mini-pattern for this thought
            text = thought['content']['revision'][:50]
            pattern = mantra_yantra.convert_text_to_yantra(text)
            
            fig = plt.figure(figsize=(5, 5))
            plt.imshow(pattern)
            plt.axis('off')
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            st.image(buf)
            plt.close(fig)
            
        st.markdown("---")
        
def voice_input():
    st.header("Voice Input Visualization")
    st.write("""
    Speak a question or statement to visualize how the brain would process it.
    This directly uses the mantra-to-yantra system to visualize your voice input.
    """)
    
    # Voice recording interface
    if "recording" not in st.session_state:
        st.session_state.recording = False
        st.session_state.audio_data = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.recording:
            if st.button("Start Recording"):
                st.session_state.recording = True
                st.session_state.audio_data = []
                
                # Start recording in thread
                def record_audio():
                    fs = 44100  # Sample rate
                    duration = 5  # 5 seconds
                    st.session_state.audio_data = sd.rec(
                        int(duration * fs), 
                        samplerate=fs,
                        channels=1, 
                        dtype='float32'
                    )
                    sd.wait()
                    st.session_state.recording = False
                
                threading.Thread(target=record_audio).start()
        else:
            st.write("Recording... (5 seconds)")
            
    with col2:
        if st.session_state.audio_data is not None and not st.session_state.recording:
            # Save audio
            fs = 44100
            filename = f"temp_recording_{time.strftime('%Y%m%d_%H%M%S')}.wav"
            write_wav(filename, fs, st.session_state.audio_data)
            
            # Display audio player
            with open(filename, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/wav")
                
            # Process and visualize
            st.write("Generating yantra pattern from your voice...")
            pattern = mantra_yantra.convert_audio_to_yantra(filename)
            
            fig = plt.figure(figsize=(10, 10))
            plt.imshow(pattern)
            plt.axis('off')
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            st.image(buf)
            plt.close(fig)
            
            # Send to brain for processing
            if st.button("Process in Brain"):
                # This would send the audio/text to the brain for processing
                st.write("Sending to autonomous brain for processing...")
                # (Implementation would depend on brain API)

if __name__ == "__main__":
    main()