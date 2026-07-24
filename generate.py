#!/usr/bin/env python3
"""Generate an andrew6rant-style neofetch profile card as an SVG."""
import html

ASCII_FILE = "portrait.txt"
OUT = "dark_mode.svg"

# ---- palette (Tokyo Night-ish, looks good on light & dark GitHub) ----
BG      = "#1a1b27"
PANEL   = "#16161e"
BORDER  = "#2f3549"
ASCII_C = "#d3dae3"
NAME    = "#7aa2f7"  # blue
AT      = "#565f89"
GREENU  = "#9ece6a"  # user/green
KEY     = "#e0af68"  # gold labels
DOT     = "#3b4261"
VAL     = "#c0caf5"  # white-ish values
HDR     = "#7dcfff"  # cyan section headers
DIM     = "#6b7394"  # placeholders / dim
GREEN   = "#9ece6a"
RED     = "#f7768e"
PURPLE  = "#bb9af7"

RIGHTCOL = 56  # width (chars) of the key...value lines

# ---- editable content ----
HANDLE_USER = "amit"
HANDLE_HOST = "yadav"

def kv(key, value, vcolor=VAL, kcolor=KEY):
    """key .......... value  (right aligned to RIGHTCOL)."""
    dots = RIGHTCOL - len(key) - 1 - 1 - 1 - len(value)
    if dots < 2:
        dots = 2
    return [(key, kcolor), (":", kcolor), (" ", DIM),
            ("." * dots, DOT), (" ", DIM), (value, vcolor)]

def header(text):
    fill = RIGHTCOL - len(text) - 1
    if fill < 2:
        fill = 2
    return [(text + " ", HDR), ("\u2500" * fill, HDR)]

def blank():
    return [(" ", DIM)]

# panel lines: each is a list of (text, color) segments
LINES = []
LINES.append([(HANDLE_USER, NAME), ("@", AT), (HANDLE_HOST, GREENU)])
LINES.append([("\u2500" * RIGHTCOL, DIM)])
LINES.append(blank())
LINES.append(kv("OS", "Windows 11, Linux, Android"))
LINES.append(kv("Host", "TDI Global Hackathon 2026"))
LINES.append(kv("Kernel", "Full-Stack & Cloud Developer"))
LINES.append(kv("IDE", "VS Code, GitHub Copilot CLI"))
LINES.append(blank())
LINES.append(kv("Languages.Programming", "Python, JavaScript, Java"))
LINES.append(kv("Languages.Computer", "HTML, CSS, YAML, JSON"))
LINES.append(kv("Languages.Real", "English, Hindi"))
LINES.append(blank())
LINES.append(kv("Hobbies.Software", "Cloud, AI/ML, Web Dev"))
LINES.append(kv("Hobbies.Hardware", "Gaming, Photography"))
LINES.append(blank())
LINES.append(header("Contact"))
LINES.append(kv("Email", "you@example.com", vcolor=DIM))
LINES.append(kv("GitHub", "iyadavamit", vcolor=GREEN))
LINES.append(kv("LinkedIn", "/in/your-handle", vcolor=DIM))
LINES.append(kv("Discord", "your_handle", vcolor=DIM))
LINES.append(blank())
LINES.append(header("GitHub Stats"))
LINES.append(kv("Repos", "1", vcolor=PURPLE))
LINES.append(kv("Followers", "0", vcolor=PURPLE))
LINES.append(kv("Stars Earned", "0", vcolor=PURPLE))
LINES.append(kv("Member since", "Jul 2026", vcolor=VAL))
LINES.append(blank())
# terminal colour swatch row
sw = []
for c in [RED, KEY, GREEN, HDR, NAME, PURPLE, "#73daca", VAL]:
    sw.append(("\u2588\u2588", c))
LINES.append(sw)

# ---- layout ----
PAD = 34
ASCII_FS = 9.0
ASCII_LH = 9.8
ASCII_CW = ASCII_FS * 0.6
PANEL_FS = 13.0
PANEL_LH = 19.0
PANEL_CW = 0.62  # monospace advance (~0.6em on GitHub's default mono)

ascii_lines = open(ASCII_FILE).read().split("\n")
while ascii_lines and ascii_lines[-1].strip() == "":
    ascii_lines.pop()
ascii_w = max(len(l) for l in ascii_lines) * ASCII_CW
ascii_h = len(ascii_lines) * ASCII_LH

panel_h = len(LINES) * PANEL_LH
panel_x = PAD + ascii_w + 30
panel_w = RIGHTCOL * (PANEL_FS * PANEL_CW)

W = int(panel_x + panel_w + PAD)
H = int(max(ascii_h, panel_h) + PAD * 2)

# vertical starting positions (center the shorter block)
ascii_y0 = (H - ascii_h) / 2 + ASCII_FS
panel_y0 = (H - panel_h) / 2 + PANEL_FS

def esc(s):
    return html.escape(s, quote=True)

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="\'JetBrains Mono\',\'Fira Code\',\'SFMono-Regular\',Consolas,Menlo,monospace">')
parts.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>')
# window dots
for i, c in enumerate([RED, KEY, GREEN]):
    parts.append(f'<circle cx="{22+i*20}" cy="22" r="6" fill="{c}"/>')

# ascii portrait
parts.append(f'<g font-size="{ASCII_FS}" fill="{ASCII_C}" xml:space="preserve" '
             f'style="white-space:pre" font-weight="bold">')
for i, line in enumerate(ascii_lines):
    y = ascii_y0 + i * ASCII_LH
    parts.append(f'<text x="{PAD}" y="{y:.1f}">{esc(line)}</text>')
parts.append('</g>')

# panel
parts.append(f'<g font-size="{PANEL_FS}" xml:space="preserve" style="white-space:pre">')
for i, segs in enumerate(LINES):
    y = panel_y0 + i * PANEL_LH
    spans = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in segs)
    parts.append(f'<text x="{panel_x:.1f}" y="{y:.1f}">{spans}</text>')
parts.append('</g>')
parts.append('</svg>')

import os
_d = os.path.dirname(OUT)
if _d:
    os.makedirs(_d, exist_ok=True)
open(OUT, "w").write("\n".join(parts))
print(f"wrote {OUT}  ({W}x{H}, ascii {len(ascii_lines)} rows)")
