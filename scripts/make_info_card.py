"""
Build a neofetch-style info card SVG (Andrew6rant style) to sit to the RIGHT of
the ASCII portrait: colored key/value rows for work experience, tech stack, and
highlights -- NOT GitHub stats (the contribution graph covers those).

Static content, hand-authored below. Lines fade/slide in on a short stagger so
it feels like the panel is printing alongside the portrait. STATIC=1 emits the
frozen state for Quick Look previews.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = True  # GitHub's Camo proxy strips CSS animations; always render static

W, H = 480, 440
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 20.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange keys (matches Andrew)
SECTION = "#58a6ff"  # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# ===========================================================================
#  EDIT THIS  -- your info panel. It re-lays-out automatically; if it gets too
#  tall for the card, bump H above (and the width= in your profile README).
#  The username in the header is HOST below.
#
#  row types:
#    ("host",)              -> "you@github" header + rule
#    ("kv", key, value)     -> orange key + light value
#    ("sec", title)         -> blue "— title —" section rule
#    ("bul", text)          -> green dot + light bullet
#    ("gap",)               -> a little vertical space
# ===========================================================================
HOST = "Mjangid2004"   # shown as  Mjangid2004@github  in the header

ROWS = [
    ("host",),
    ("kv", "Name", "Mohan Sharma"),
    ("kv", "Role", "Data Science Intern @ Hackveda Solutions"),
    ("kv", "Edu", "B.Tech CSE (Data Science), CMR Univ - CGPA 9.0"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Languages", "Python, SQL, C/C++ (basics), HTML/CSS"),
    ("kv", "ML / AI", "Scikit-learn, Pandas, NumPy, Matplotlib"),
    ("kv", "Backend", "Django, REST APIs, Socket Programming"),
    ("kv", "Tools", "Power BI, Git, USDA API, YouTube API"),
    ("gap",),
    ("sec", "Projects"),
    ("bul", "Foodie Calorie Finder — Django + USDA API nutrition tracker"),
    ("bul", "Water Footprint Estimator — Linear Regression + Matplotlib"),
    ("bul", "Desi Beats — ad-free music streaming via YouTube API"),
    ("bul", "Qrio — anonymous academic Q&A platform"),
    ("gap",),
    ("sec", "Highlights"),
    ("bul", "NPTEL: Artificial Intelligence & Mobile VR certified"),
    ("bul", "District-level Table Tennis player — 2x Silver medalist"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """fade + slight upward slide via CSS animation (GitHub-safe)."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    cls = f"r{i}"
    return f'<g class="{cls}">{inner}</g>', cls, delay


def css_rule(cls, delay):
    return (f".{cls}{{opacity:0;animation:rise 0.4s cubic-bezier(.2,.8,.2,1) "
            f"{delay:.2f}s forwards;}}")


css_rules = []

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">{esc(HOST)}@github: ~$ neofetch</text>')

y = TITLEBAR_H + 30
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "host":
        host = esc(HOST)
        rule_x = KEY_X + (len(HOST) + 7) * 8 + 8
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                 f'<tspan fill="{GREEN}">{host}</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">github</tspan></text>'
                 f'<line x1="{rule_x}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
                 f'&#8212; {title}</text>'
                 f'<line x1="{KEY_X + 12 + len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>')
    else:
        continue
    result = rise(inner, i)
    if isinstance(result, tuple):
        g_html, cls, delay = result
        css_rules.append(css_rule(cls, delay))
        parts.append(g_html)
    else:
        parts.append(result)
    y += LINE_H

if css_rules and not STATIC:
    # inject per-row CSS rules into the existing <style> block
    rule_str = "".join(css_rules)
    parts[2] = parts[2].replace("</style>", rule_str + "</style>")

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
