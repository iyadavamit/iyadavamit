#!/usr/bin/env python3
"""Generate an andrew6rant-style neofetch profile card (SVG) for iyadavamit.

GitHub Stats auto-refresh from the GitHub API (see fetch_stats). A GitHub
Action re-runs this at midnight (IST) and commits the updated card.
Edit the CONFIG block below to change any personal detail, then run:

    python3 generate.py        # rewrites dark_mode.svg
"""
import html, os, sys, json, urllib.request

USER = "iyadavamit"
ASCII_FILE = "portrait.txt"
OUT = "dark_mode.svg"

# ---------------- CONFIG (edit these) ----------------
HEADER_USER = "amit"
HEADER_HOST = "yadav"

SYSTEM = [
    ("IDE", "IntelliJ IDEA, VS Code"),
]
SKILLS = [
    ("Languages", "Java, C, C++, SQL"),
    ("Frameworks", "Spring Boot, Apache Kafka, RESTful APIs, Microservices Architecture"),
    ("Cloud & DevOps", "Google Cloud Platform (GCP), Terraform, GitHub Actions, Docker, CI/CD Pipelines"),
    ("Databases", "Oracle Database"),
    ("Tools", "Git, Maven, Postman, IntelliJ IDEA, Swagger, Jira, Confluence, gcloud CLI, Shell (Bash), SWIFT Translator"),
]
EMAIL = "ay3593161@gmail.com"
LEETCODE = "Amit_yadav01"

DEFAULT_STATS = {"repos": 1, "stars": 0, "followers": 0, "following": 1, "since": "Jul 2026"}
# -----------------------------------------------------

# palette (Tokyo Night)
BG="#1a1b27"; BORDER="#2f3549"; ASCII_C="#d3dae3"
NAME="#7aa2f7"; AT="#565f89"; GREENU="#9ece6a"
KEY="#e0af68"; DOT="#3b4261"; VAL="#c0caf5"; HDR="#7dcfff"
DIM="#6b7394"; GREEN="#9ece6a"; RED="#f7768e"; PURPLE="#bb9af7"; LEET="#ffa116"

COLS = 56  # panel width in monospace columns

MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def month_year(ym):
    try:
        y,m = ym.split("-")[:2]; return f"{MONTHS[int(m)-1]} {y}"
    except Exception:
        return ym or "\u2014"

def api(path):
    req = urllib.request.Request("https://api.github.com"+path,
        headers={"User-Agent":"profile-card","Accept":"application/vnd.github+json"})
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok: req.add_header("Authorization","Bearer "+tok)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def fetch_stats():
    u = api("/users/"+USER)
    repos = api("/users/%s/repos?per_page=100&type=owner"%USER)
    stars = sum(int(r.get("stargazers_count",0)) for r in repos if not r.get("fork"))
    return {"repos":int(u.get("public_repos",0)),
            "stars":stars,
            "followers":int(u.get("followers",0)),
            "following":int(u.get("following",0)),
            "since":month_year(str(u.get("created_at",""))[:7])}

def load_stats():
    try:
        s = fetch_stats()
        json.dump(s, open("stats.json","w"), indent=2)
        return s
    except Exception as e:
        sys.stderr.write("stats fetch failed (%s); using cache/defaults\n"%e)
        try: return json.load(open("stats.json"))
        except Exception: return DEFAULT_STATS

# ---- line builders: each line = list of (text, color) ----
def kv(key, value, vcolor=VAL, kcolor=KEY):
    left = key + ":"
    dots = COLS - len(left) - 2 - len(value)
    if dots < 2: dots = 2
    return [(left,kcolor),(" ",DIM),("."*dots,DOT),(" ",DIM),(value,vcolor)]

def header(text):
    fill = COLS - len(text) - 1
    if fill < 2: fill = 2
    return [(text+" ",HDR),("\u2500"*fill,HDR)]

def blank(): return [(" ",DIM)]

def wrap_commas(value, width):
    items=[s.strip() for s in value.split(",")]
    lines=[]; cur=""
    for i,it in enumerate(items):
        piece = it + ("," if i < len(items)-1 else "")
        cand = piece if not cur else cur+" "+piece
        if len(cand) <= width or not cur:
            cur = cand
        else:
            lines.append(cur); cur = piece
    if cur: lines.append(cur)
    return lines

def skill(key, value):
    prefix = key + ": "
    lines = wrap_commas(value, COLS - len(prefix))
    rows=[[(key+":",KEY),(" ",DIM),(lines[0],VAL)]]
    for cont in lines[1:]:
        rows.append([(" "*len(prefix),DIM),(cont,VAL)])
    return rows

# ---- assemble panel ----
stats = load_stats()
LINES=[]
LINES.append([(HEADER_USER,NAME),("@",AT),(HEADER_HOST,GREENU)])
LINES.append([("\u2500"*COLS,DIM)])
LINES.append(blank())
for k,v in SYSTEM: LINES.append(kv(k,v))
LINES.append(blank())
LINES.append(header("Technical Skills"))
for k,v in SKILLS: LINES += skill(k,v)
LINES.append(blank())
LINES.append(header("Contact"))
LINES.append(kv("Email", EMAIL))
LINES.append(kv("GitHub", USER, vcolor=GREEN))
LINES.append(kv("LeetCode", LEETCODE, vcolor=LEET))
LINES.append(blank())
LINES.append(header("GitHub Stats"))
LINES.append(kv("Repos", str(stats["repos"]), vcolor=PURPLE))
LINES.append(kv("Stars Earned", str(stats["stars"]), vcolor=PURPLE))
LINES.append(kv("Followers", str(stats["followers"]), vcolor=PURPLE))
LINES.append(kv("Following", str(stats["following"]), vcolor=PURPLE))
LINES.append(kv("Member since", str(stats["since"])))
LINES.append(blank())
LINES.append([("\u2588\u2588",c) for c in [RED,KEY,GREEN,HDR,NAME,PURPLE,"#73daca",VAL]])

# ---- geometry ----
PAD=30
ASCII_FS=9.0; ASCII_LH=9.8; ASCII_CW=0.62
PANEL_FS=13.0; PANEL_LH=18.5; PANEL_CW=0.62

ascii_lines=open(ASCII_FILE).read().split("\n")
while ascii_lines and ascii_lines[-1].strip()=="":
    ascii_lines.pop()
ascii_w=max(len(l) for l in ascii_lines)*ASCII_FS*ASCII_CW
ascii_h=len(ascii_lines)*ASCII_LH
panel_h=len(LINES)*PANEL_LH
panel_w=COLS*PANEL_FS*PANEL_CW

panel_x=PAD+ascii_w+34
W=int(panel_x+panel_w+PAD)
H=int(max(panel_h, ascii_h)+PAD*2)
panel_y0=(H-panel_h)/2+PANEL_FS
ascii_y0=(H-ascii_h)/2+ASCII_FS

def esc(s): return html.escape(s, quote=True)
p=[]
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="\'DejaVu Sans Mono\',\'Menlo\',\'JetBrains Mono\',monospace">')
p.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>')
for i,c in enumerate([RED,KEY,GREEN]):
    p.append(f'<circle cx="{22+i*20}" cy="22" r="6" fill="{c}"/>')
p.append(f'<g font-size="{ASCII_FS}" fill="{ASCII_C}" xml:space="preserve" style="white-space:pre">')
for i,line in enumerate(ascii_lines):
    p.append(f'<text x="{PAD}" y="{ascii_y0+i*ASCII_LH:.1f}">{esc(line)}</text>')
p.append('</g>')
p.append(f'<g font-size="{PANEL_FS}" xml:space="preserve" style="white-space:pre">')
for i,segs in enumerate(LINES):
    y=panel_y0+i*PANEL_LH
    spans="".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t,c in segs)
    p.append(f'<text x="{panel_x:.1f}" y="{y:.1f}">{spans}</text>')
p.append('</g>')
p.append('</svg>')

d=os.path.dirname(OUT)
if d: os.makedirs(d, exist_ok=True)
open(OUT,"w").write("\n".join(p))
print(f"wrote {OUT} {W}x{H} panel_rows={len(LINES)} ascii_rows={len(ascii_lines)}")
