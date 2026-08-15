# Reference image from this Exeperiment :
# Title : Analyzing 8b/10b Encoded Signals with a Real-time Oscilloscope
# Link  :  https://download.tek.com/document/55W_26438_2.pdf

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

# -------------------------------------------------------------
# 1. Bit Definitions (Standard 8b/10b Transmission)
# -------------------------------------------------------------
hex_labels = ["A0_h", "00_h", "00_h", "BF_h"]

raw_bytes = [
    [1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1]
]

encoded_syms = [
    [1, 0, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1]
]

flat_encoded = [b for sym in encoded_syms for b in sym]

# -------------------------------------------------------------
# 2. Figure & Layout Setup
# -------------------------------------------------------------
fig = plt.figure(figsize=(13, 6.2), facecolor='#EAE6DF')

# Top schematic axis
ax_top = fig.add_axes([0.16, 0.44, 0.78, 0.46])
ax_top.set_facecolor('#EAE6DF')
ax_top.axis('off')
ax_top.set_xlim(0, 40)
ax_top.set_ylim(0, 5.0)

# Bottom graph axis
ax_graph = fig.add_axes([0.16, 0.08, 0.78, 0.32])
ax_graph.set_facecolor('white')

# -------------------------------------------------------------
# 3. Waveform Drawing Helper
# -------------------------------------------------------------
def get_step_waveform(bits, x_offset=0, bit_width=1.0, y_base=0.0, y_high=0.6):
    x, y = [], []
    for i, b in enumerate(bits):
        x0 = x_offset + i * bit_width
        x1 = x0 + bit_width
        val = y_base + (y_high if b == 1 else 0.0)

        if len(x) > 0 and y[-1] != val:
            x.append(x0)
            y.append(val)
        x.extend([x0, x1])
        y.extend([val, val])
    return x, y

# -------------------------------------------------------------
# 4. Draw Schematic (Boxes, Text, Waveforms)
# -------------------------------------------------------------
# Row Labels on Left
fig.text(0.04, 0.81, 'Raw Binary', fontsize=11, fontweight='bold', va='center')
fig.text(0.04, 0.63, '8b/10b Symbol', fontsize=11, fontweight='bold', va='center')

# --- Raw Binary Row ---
for i, (lbl, byte) in enumerate(zip(hex_labels, raw_bytes)):
    x_pos = i * 10
    # Hex label above each byte group
    ax_top.text(x_pos + 4.0, 4.5, lbl, fontsize=11, fontweight='bold', ha='center', va='center')

    # 8 boxes per byte group
    for j, bit in enumerate(byte):
        rect = plt.Rectangle((x_pos + j, 3.55), 1.0, 0.6, fill=False, edgecolor='#244986', lw=1.3)
        ax_top.add_patch(rect)
        ax_top.text(x_pos + j + 0.5, 3.85, str(bit), ha='center', va='center', fontsize=10, fontweight='bold')

    # Raw waveform directly beneath its respective 8-bit group
    wx, wy = get_step_waveform(byte, x_offset=x_pos, bit_width=1.0, y_base=2.6, y_high=0.6)
    ax_top.plot(wx, wy, color='black', lw=1.5)

# --- 8b/10b Row ---
for j, bit in enumerate(flat_encoded):
    rect = plt.Rectangle((j, 1.45), 1.0, 0.6, fill=False, edgecolor='#244986', lw=1.3)
    ax_top.add_patch(rect)
    ax_top.text(j + 0.5, 1.75, str(bit), ha='center', va='center', fontsize=10, fontweight='bold')

# Continuous 8b/10b waveform
wx_enc, wy_enc = get_step_waveform(flat_encoded, x_offset=0, bit_width=1.0, y_base=0.5, y_high=0.6)
ax_top.plot(wx_enc, wy_enc, color='black', lw=1.5)

# -------------------------------------------------------------
# 5. Correct Physical RC Integrator for Running Average
# -------------------------------------------------------------
# First-order IIR filter simulating an AC coupling circuit (tau ~ 10 bit periods)
alpha = 0.15
b_coeff = [alpha]
a_coeff = [1.0, -(1.0 - alpha)]

# 8b/10b sequence: sample at each bit period
enc_samples = np.array(flat_encoded, dtype=float)
enc_avg = lfilter(b_coeff, a_coeff, enc_samples, zi=[0.55*(1-alpha)])[0]

# Raw sequence: constructed across the transmission interval
raw_dense = np.zeros(40)
for i, byte in enumerate(raw_bytes):
    raw_dense[i*10 : i*10 + 8] = byte

raw_avg_full = lfilter(b_coeff, a_coeff, raw_dense, zi=[0.90*(1-alpha)])[0]

# Extract points corresponding to where raw bits are valid
raw_x_idx = []
for i in range(4):
    raw_x_idx.extend(range(i * 10, i * 10 + 8))
raw_x_pts = np.array(raw_x_idx) + 0.5
raw_y_pts = raw_avg_full[raw_x_idx]

enc_x_pts = np.arange(40) + 0.5

# -------------------------------------------------------------
# 6. Render Graph
# -------------------------------------------------------------
ax_graph.set_title('Average Value of Transmitted Signal', fontsize=9.5, loc='left', pad=4, style='italic')
ax_graph.grid(True, which='both', color='#A8D0E6', linestyle='-', linewidth=0.8)

ax_graph.set_xlim(0, 40)
ax_graph.set_ylim(-0.05, 1.05)

# Plot data traces
ax_graph.plot(raw_x_pts, raw_y_pts, marker='d', markersize=3.5, color='#2B5CA3', lw=1.3, label='Raw Binary')
ax_graph.plot(enc_x_pts, enc_avg, marker='^', markersize=3.5, color='black', lw=1.3, label='8b/10b Symbol')

ax_graph.set_xticks(np.arange(0, 41, 2))
ax_graph.set_xticklabels([])
ax_graph.set_yticks(np.linspace(0, 1, 9))
ax_graph.set_yticklabels([])
ax_graph.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8)

# -------------------------------------------------------------
# 7. Red Callout Text & Connecting Arrow
# -------------------------------------------------------------
fig.text(0.70, 0.94, 'Relatively constant average value,\nMany transitions for clock recovery',
         color='#D9381E', fontsize=11, style='italic', fontweight='bold', ha='center', va='center')

# Draw arrow from text to the stabilized 8b/10b curve around bit 27
ax_graph.annotate(
    '',
    xy=(27.0, enc_avg[27]),
    xycoords='data',
    xytext=(0.67, 0.90),
    textcoords='figure fraction',
    arrowprops=dict(arrowstyle="->", color='#D9381E', lw=1.8, connectionstyle="arc3,rad=-0.12")
)

plt.show()
