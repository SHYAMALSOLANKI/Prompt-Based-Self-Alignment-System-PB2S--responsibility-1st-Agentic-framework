#!/usr/bin/env python3
"""
Mantra → Yantra (cymatics-style) desktop app

- Load a mantra audio (WAV/FLAC/OGG) or record from mic
- Extract dominant spectral peaks
- Synthesize a 2D standing-wave interference field driven by those peaks
- Display/save the resulting yantra-like pattern

This is a *visual simulation*, not a material-plate solver. It’s designed to be
stable, reproducible, and responsive on a laptop.
"""

import io
import sys
import time
import math
import threading
import queue
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import find_peaks
from scipy.fft import rfft, rfftfreq

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# --------------------------- DSP Utilities ---------------------------

def normalize_audio(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64).flatten()
    if x.size == 0:
        return x
    m = np.max(np.abs(x))
    return x / m if m > 0 else x


def load_audio_file(path: str):
    data, sr = sf.read(path, always_2d=False)
    if data.ndim == 2:  # stereo -> mono
        data = data.mean(axis=1)
    data = normalize_audio(data)
    return data, sr


def record_audio(seconds=5, sr=44100):
    rec = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    data = rec[:, 0].astype(np.float64)
    data = normalize_audio(data)
    return data, sr


def spectral_peaks(x, sr, n_peaks=6, min_freq=40.0, max_freq=4000.0):
    """Return (peak_freqs, peak_mags) of top spectral components."""
    if x.size == 0:
        return np.array([]), np.array([])
    # Window to reduce spectral leakage
    w = np.hanning(len(x))
    X = rfft(x * w)
    freqs = rfftfreq(len(x), d=1/sr)
    mags = np.abs(X)

    # Restrict band
    band = np.where((freqs >= min_freq) & (freqs <= max_freq))[0]
    if band.size == 0:
        return np.array([]), np.array([])

    bf = freqs[band]
    bm = mags[band]

    # Peak picking
    # A small prominence avoids picking noise; tune mildly
    peaks, _ = find_peaks(bm, prominence=np.max(bm)*0.02 if bm.size else 0.0)
    if peaks.size == 0:
        return np.array([]), np.array([])

    # Sort by magnitude
    idx = np.argsort(bm[peaks])[::-1]
    idx = idx[:n_peaks]
    pf = bf[peaks][idx]
    pm = bm[peaks][idx]
    # Normalize amplitudes
    if pm.size:
        pm = pm / (pm.max() + 1e-12)
    return pf, pm


# --------------------- Cymatic Pattern Synthesis ---------------------

def yantra_field(freqs, amps, grid_size=400, contrast=3.0, circular_mask=True, seed=1234):
    """
    Build a 2D interference field from peak frequencies:
      Z(x,y) = sum_i A_i * sin(k_i * (x*cos(theta_i) + y*sin(theta_i)) + phi_i)
    where k_i ~ scaled freq, theta_i spread for symmetry, phi_i fixed
    """
    if len(freqs) == 0:
        return np.zeros((grid_size, grid_size))

    # Normalized spatial wavenumbers (relative)
    fmin = np.min(freqs)
    if fmin <= 0:
        fmin = 1.0
    ks = (freqs / fmin) * math.pi * 0.75  # scale factor chosen to produce clear patterns

    # Grid
    xs = np.linspace(-1.0, 1.0, grid_size)
    ys = np.linspace(-1.0, 1.0, grid_size)
    X, Y = np.meshgrid(xs, ys)

    rng = np.random.default_rng(seed)
    # Arrange directions more deterministically for symmetry
    thetas = np.linspace(0, 2*np.pi, len(ks), endpoint=False)
    thetas = (thetas + 0.37) % (2*np.pi)
    phis = rng.uniform(0, 2*np.pi, size=len(ks))

    Z = np.zeros_like(X)
    for k, a, th, ph in zip(ks, amps, thetas, phis):
        # Plane wave projection
        proj = X*np.cos(th) + Y*np.sin(th)
        Z += a * np.sin(k*proj + ph)

    # Optional circular mask (plate-like)
    if circular_mask:
        R = np.sqrt(X*X + Y*Y)
        mask = (R <= 1.0).astype(float)
        Z *= mask

    # Nonlinear contrast to emphasize nodal lines
    # Use tanh on absolute to bring out “Chladni-like” clarity
    Zn = np.tanh(contrast * np.abs(Z))
    return Zn


# ------------------------------ GUI ---------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mantra → Yantra (Cymatics)")
        self.geometry("960x720")

        # State
        self.audio = np.array([], dtype=np.float64)
        self.sr = 44100
        self.freqs = np.array([])
        self.amps = np.array([])

        # Controls
        ctrl = ttk.Frame(self)
        ctrl.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        ttk.Label(ctrl, text="Input").pack(anchor="w")
        ttk.Button(ctrl, text="Load Audio…", command=self.on_load).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Record Mic (5s)", command=self.on_record).pack(fill=tk.X, pady=2)
        ttk.Separator(ctrl, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        self.npeaks_var = tk.IntVar(value=6)
        self.contrast_var = tk.DoubleVar(value=3.0)
        self.grid_var = tk.IntVar(value=400)
        self.mask_var = tk.BooleanVar(value=True)

        row = ttk.Frame(ctrl); row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Peaks").pack(side=tk.LEFT)
        ttk.Spinbox(row, from_=1, to=16, width=5, textvariable=self.npeaks_var).pack(side=tk.RIGHT)

        row = ttk.Frame(ctrl); row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Contrast").pack(side=tk.LEFT)
        ttk.Scale(row, from_=0.5, to=6.0, orient=tk.HORIZONTAL, variable=self.contrast_var).pack(side=tk.RIGHT, fill=tk.X, expand=True)

        row = ttk.Frame(ctrl); row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Resolution").pack(side=tk.LEFT)
        ttk.Spinbox(row, from_=200, to=1000, increment=50, width=6, textvariable=self.grid_var).pack(side=tk.RIGHT)

        ttk.Checkbutton(ctrl, text="Circular mask", variable=self.mask_var).pack(anchor="w", pady=2)

        ttk.Button(ctrl, text="Analyze Peaks", command=self.on_analyze).pack(fill=tk.X, pady=6)
        ttk.Button(ctrl, text="Render Yantra", command=self.on_render).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Save Image…", command=self.on_save).pack(fill=tk.X, pady=2)

        # Info box
        self.info = tk.Text(ctrl, height=18, width=34)
        self.info.pack(fill=tk.BOTH, expand=False, pady=6)
        self.info.insert(tk.END, "Load/record audio, Analyze Peaks, then Render.\n")

        # Plot area
        fig = Figure(figsize=(6.8, 6.8), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_axis_off()
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._render_placeholder()

    def _render_placeholder(self):
        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.text(0.5, 0.5, "Mantra → Yantra", ha='center', va='center', fontsize=18)
        self.canvas.draw_idle()

    def on_load(self):
        path = filedialog.askopenfilename(
            title="Open audio",
            filetypes=[("Audio", "*.wav *.flac *.ogg *.aiff *.aif *.aifc *.au *.snd"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            data, sr = load_audio_file(path)
        except Exception as e:
            messagebox.showerror("Load error", str(e))
            return
        self.audio, self.sr = data, sr
        self._log(f"Loaded: {path}\nSamples: {len(self.audio)}, sr={self.sr}\n")

    def on_record(self):
        try:
            self._log("Recording 5 seconds…\n")
            self.update()
            data, sr = record_audio(seconds=5, sr=44100)
            self.audio, self.sr = data, sr
            self._log(f"Recorded mic: {len(self.audio)} samples @ {self.sr} Hz\n")
        except Exception as e:
            messagebox.showerror("Record error", str(e))

    def on_analyze(self):
        if self.audio.size == 0:
            messagebox.showwarning("No audio", "Load or record audio first.")
            return
        npeaks = int(self.npeaks_var.get())
        freqs, amps = spectral_peaks(self.audio, self.sr, n_peaks=npeaks)
        self.freqs, self.amps = freqs, amps

        if len(freqs) == 0:
            self._log("No peaks detected. Try a different recording or increase volume.\n")
            return

        self._log("Top peaks (Hz, amplitude):\n")
        for f, a in zip(freqs, amps):
            self._log(f"  {f:8.2f}  {a:5.3f}\n")

    def on_render(self):
        if len(self.freqs) == 0:
            messagebox.showwarning("No peaks", "Analyze peaks first.")
            return
        grid = int(self.grid_var.get())
        contrast = float(self.contrast_var.get())
        mask = bool(self.mask_var.get())

        self._log(f"Rendering grid={grid}, contrast={contrast}, circular_mask={mask}\n")
        Zn = yantra_field(self.freqs, self.amps, grid_size=grid, contrast=contrast, circular_mask=mask)

        self.ax.clear()
        self.ax.set_axis_off()
        # Use a symmetric colormap to emphasize nodes
        self.ax.imshow(Zn, cmap="inferno", origin="lower", interpolation="bilinear")
        self.canvas.draw_idle()

    def on_save(self):
        fpath = filedialog.asksaveasfilename(
            title="Save image",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("TIFF", "*.tif;*.tiff"), ("All files", "*.*")]
        )
        if not fpath:
            return
        # Render current figure to file
        try:
            self.canvas.figure.savefig(fpath, dpi=300, bbox_inches="tight", pad_inches=0)
            self._log(f"Saved image: {fpath}\n")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    def _log(self, msg):
        self.info.insert(tk.END, msg)
        self.info.see(tk.END)


if __name__ == "__main__":
    App().mainloop()
