#!/usr/bin/env python3
"""
🧠 PB2S Conversational AI Dashboard
LLM-style brain with sophisticated 4-step reasoning
No pattern formation - pure conversational intelligence
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import importlib.util
import time
import json
import sounddevice as sd
from scipy.io.wavfile import write as write_wav

# Load mantra_to_yantra dynamically
mantra_path = os.path.join(os.path.dirname(__file__), 'mantra_yantra', 'mantra_to_yantra.py')
spec = importlib.util.spec_from_file_location("mantra_to_yantra", mantra_path)
mantra_yantra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mantra_yantra)

# Pattern storage directory
PATTERN_DIR = os.path.join(os.path.dirname(__file__), 'patterns')
os.makedirs(PATTERN_DIR, exist_ok=True)

# Simple brain logic (echo with pattern/contradiction check)


class SimpleBrain:
    def __init__(self):
        self.pattern_history = []
        self.pattern_signatures = set()
        self.letter_patterns = {}
        self.word_patterns = {}
        self.sentence_patterns = {}
        self.pattern_meanings = {}  # {pattern_hash: meaning} - kept for patterns only
        self.chat_history = []
        self.rules = self.load_rules()
        self.memory = self.load_memory()
        self.load_existing_patterns()

    def pattern_hash(self, pattern):
        # Use a hash of the pattern array for fast lookup
        return str(np.round(pattern, 4).tobytes())

    def load_existing_patterns(self):
        # Load all previously stored patterns and their hashes
        for fname in os.listdir(PATTERN_DIR):
            if fname.endswith('.npy'):
                pattern = np.load(os.path.join(PATTERN_DIR, fname))
                sig = self.pattern_hash(pattern)
                self.pattern_signatures.add(sig)

    def store_pattern(self, pattern, meta):
        sig = self.pattern_hash(pattern)
        if sig in self.pattern_signatures:
            return False  # Already learned
        timestamp = int(time.time())
        fname_base = f'pattern_{timestamp}'
        np.save(os.path.join(PATTERN_DIR, fname_base + '.npy'), pattern)
        with open(os.path.join(PATTERN_DIR, fname_base + '.json'), 'w') as f:
            json.dump(meta, f)
        self.pattern_signatures.add(sig)
        return True

    def store_letter_patterns(self, text):
        for letter in text:
            if letter.strip() == '':
                continue
            pattern = text_to_yantra(letter)
            sig = self.pattern_hash(pattern)
            if letter not in self.letter_patterns:
                self.letter_patterns[letter] = sig
                self.store_pattern(pattern, {'type': 'letter', 'value': letter})

    def store_word_patterns(self, text):
        words = text.split()
        for word in words:
            pattern = text_to_yantra(word)
            sig = self.pattern_hash(pattern)
            if word not in self.word_patterns:
                self.word_patterns[word] = sig
                self.store_pattern(pattern, {'type': 'word', 'value': word})

    def store_sentence_pattern(self, text):
        pattern = text_to_yantra(text)
        sig = self.pattern_hash(pattern)
        if text not in self.sentence_patterns:
            self.sentence_patterns[text] = sig
            self.store_pattern(pattern, {'type': 'sentence', 'value': text})
        return pattern, sig

    def load_rules(self):
        rules_path = os.path.join(PATTERN_DIR, 'brain_rules.json')
        if os.path.exists(rules_path):
            with open(rules_path, 'r') as f:
                return json.load(f)
        return {}

    def save_rules(self):
        rules_path = os.path.join(PATTERN_DIR, 'brain_rules.json')
        with open(rules_path, 'w') as f:
            json.dump(self.rules, f)

    def load_memory(self):
        mem_path = os.path.join(PATTERN_DIR, 'brain_memory.json')
        if os.path.exists(mem_path):
            with open(mem_path, 'r') as f:
                return json.load(f)
        return []

    def save_memory(self):
        mem_path = os.path.join(PATTERN_DIR, 'brain_memory.json')
        with open(mem_path, 'w') as f:
            json.dump(self.memory, f)

    def learn_rule(self, keyword, response):
        self.rules[keyword.lower()] = response
        self.save_rules()

    def get_meaning(self, text):
        """Efficiently lookup meaning from imported knowledge without loading all at once"""
        json_file = os.path.join(PATTERN_DIR, 'imported_meanings.json')
        txt_file = os.path.join(PATTERN_DIR, 'imported_meanings.txt')
        
        # Try JSON first (for smaller files)
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    # Try to load efficiently
                    data = json.load(f)
                    return data.get(text.lower())
            except (MemoryError, json.JSONDecodeError):
                pass
        
        # Fall back to text format (for very large files)
        if os.path.exists(txt_file):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '|' in line:
                            key, value = line.strip().split('|', 1)
                            if key.lower() == text.lower():
                                return value
            except Exception:
                pass
        
        return None

    def respond(self, user_text):
        # Store patterns for learning/visualization only (decoupled from reply logic)
        self.store_letter_patterns(user_text)
        self.store_word_patterns(user_text)
        pattern, sig = self.store_sentence_pattern(user_text)

        # LLM-style reply logic using direct string matching
        reply = None
        contradiction = False

        # First try full sentence
        meaning = self.get_meaning(user_text)
        if meaning:
            reply = meaning
        else:
            # Try word-by-word lookup
            words = [w.strip(",.?!") for w in user_text.lower().split()]
            known = []
            unknown = []
            
            for word in words:
                word_meaning = self.get_meaning(word)
                if word_meaning:
                    known.append(f"{word}: {word_meaning}")
                else:
                    unknown.append(word)
            
            if known:
                reply = " | ".join(known)
                if unknown:
                    reply += f" | Unknown: {', '.join(unknown)}"
            else:
                reply = f"What does '{user_text}' mean? Please provide a meaning or example. I don't know the meaning of: {', '.join(unknown)}. Please teach me."

        # Contradiction detection (compare to all previous patterns for learning)
        for prev_pattern in self.pattern_history:
            if not self.compare_patterns(pattern, prev_pattern):
                contradiction = True
                break
        
        self.pattern_history.append(pattern)
        self.chat_history.append({'user': user_text, 'pattern': pattern, 'contradiction': contradiction})
        self.memory.append({'user': user_text, 'brain': reply})
        self.save_memory()

        return reply, pattern, contradiction

    def compare_patterns(self, p1, p2, threshold=0.95):
        if p1.shape != p2.shape:
            return False
        p1n = (p1 - p1.mean()) / (p1.std() + 1e-8)
        p2n = (p2 - p2.mean()) / (p2.std() + 1e-8)
        sim = np.dot(p1n.flatten(), p2n.flatten()) / (np.linalg.norm(p1n.flatten()) * np.linalg.norm(p2n.flatten()) + 1e-8)
        return sim >= threshold


brain = SimpleBrain()

def record_voice(duration=5, fs=44100):
    st.info(f"Recording for {duration} seconds...")
    rec = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    audio = rec[:, 0].astype(np.float64)
    filename = f"temp_voice_{int(time.time())}.wav"
    write_wav(filename, fs, audio)
    return filename

st.title("Pattern Chat Dashboard (No LLM)")
st.write("Chat with the brain, see yantra patterns, and contradiction learning in action.")

if 'chat' not in st.session_state:
    st.session_state.chat = []


tab1, tab2 = st.tabs(["💬 Text Chat", "🎤 Voice Input"])

with tab1:
    user_input = st.text_input("You:", "")
    if st.button("Send", key="send_text") and user_input.strip():
        response, pattern, contradiction = brain.respond(user_input)
        st.session_state.chat.append({'user': user_input, 'brain': response, 'pattern': pattern, 'contradiction': contradiction})

        # Meaning input UI: if the last brain response asks for a meaning, show an input box
        if st.session_state.chat:
            last_entry = st.session_state.chat[-1]
            if last_entry['brain'] and "Please provide a meaning" in last_entry['brain']:
                meaning_input = st.text_input("Provide meaning for your last input:", "", key="meaning_input")
                if st.button("Submit Meaning", key="submit_meaning") and meaning_input.strip():
                    # Store the meaning for the last pattern
                    pattern, sig = brain.store_sentence_pattern(last_entry['user'])
                    brain.pattern_meanings[sig] = meaning_input.strip()
                    st.success(f"Meaning for '{last_entry['user']}' stored: {meaning_input.strip()}")

with tab2:
    st.write("Record your voice and generate a yantra pattern. The brain will respond to your voice input.")
    if st.button("Record Voice", key="record_voice"):
        filename = record_voice()
        st.audio(filename, format="audio/wav")
        # Convert audio to yantra pattern
        try:
            pattern = mantra_yantra.convert_audio_to_yantra(filename)
            # Save pattern and metadata
            timestamp = int(time.time())
            fname_base = f'pattern_{timestamp}_voice'
            np.save(os.path.join(PATTERN_DIR, fname_base + '.npy'), pattern)
            meta = {
                'timestamp': timestamp,
                'user_text': f"[voice] {filename}",
                'pattern_file': fname_base + '.npy'
            }
            with open(os.path.join(PATTERN_DIR, fname_base + '.json'), 'w') as f:
                json.dump(meta, f)
            # Contradiction detection (simple: compare to last pattern)
            contradiction = False
            if brain.pattern_history:
                last_pattern = brain.pattern_history[-1]
                contradiction = not brain.compare_patterns(pattern, last_pattern)
            brain.pattern_history.append(pattern)
            brain.chat_history.append({'user': '[voice]', 'pattern': pattern, 'contradiction': contradiction})
            response = f"Brain received your voice input."
            st.session_state.chat.append({'user': '[voice]', 'brain': response, 'pattern': pattern, 'contradiction': contradiction})
        except Exception as e:
            st.error(f"Failed to process voice input: {e}")


# Display chat and patterns
for entry in st.session_state.chat:
    st.markdown(f"**You:** {entry['user']}")
    st.markdown(f"**Brain:** {entry['brain']}")
    buf = io.BytesIO()
    fig, ax = plt.subplots(figsize=(4,4))
    ax.imshow(entry['pattern'])
    ax.axis('off')
    plt.tight_layout()
    fig.savefig(buf, format='png')
    st.image(buf, caption="Yantra Pattern", use_container_width=False)
    if entry['contradiction']:
        st.warning("Contradiction detected! Learning triggered.")
    st.markdown("---")

# Optionally, show pattern history gallery
if st.checkbox("Show Pattern Gallery"):
    files = [f for f in os.listdir(PATTERN_DIR) if f.endswith('.npy')]
    files = sorted(files, reverse=True)[:10]
    for f in files:
        pattern = np.load(os.path.join(PATTERN_DIR, f))
        buf = io.BytesIO()
        fig, ax = plt.subplots(figsize=(2,2))
        ax.imshow(pattern)
        ax.axis('off')
        plt.tight_layout()
        fig.savefig(buf, format='png')
    st.image(buf, caption=f, use_container_width=False)
