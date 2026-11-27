"""Builds project detail pages and the homepage game list from tools/projects.py.

Run: python3 tools/build.py
- writes /<slug>/index.html for every project (except own_page ones);
  privacy/terms/safety sub-pages are never touched;
- keeps each old page's Credits block (saved once to content/credits/<slug>.html);
- rewrites the `const games=` line of /index.html.
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from projects import PROJECTS, ROOT  # noqa: E402

EMAIL_B64 = "bW9jLmxpYW1nQGxzdG1udg=="  # reversed + base64; assembled by JS on click only
MAIL_JS = '<script>document.addEventListener("click",function(e){var a=e.target.closest("a[data-m]");if(!a||a.dataset.open)return;var m=atob(a.dataset.m).split("").reverse().join("");a.href="mailto:"+m+(a.dataset.s?"?subject="+a.dataset.s:"");if(a.dataset.show)a.textContent=m;a.dataset.open=1})</script>'
LABELS = {"Quest": "Meta Quest", "iPhone": "iPhone", "Watch": "Apple Watch", "Web": "Web"}
STORE = {"Quest": "Meta Horizon Store", "iPhone": "App Store", "Watch": "App Store", "Web": "Playgama"}
LEGAL = [("privacy", "Privacy Policy"), ("terms", "Terms of Use"), ("safety", "AI and Safety")]

e = html.escape


def inline(t):
    t = e(t)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)


def is_heading(line):
    s = line.strip().strip("*").strip()
    if not s or len(s) > 48 or s.startswith("•"):
        return False
    letters = [c for c in s if c.isalpha()]
    return (letters and all(c.isupper() for c in letters)) or (s.endswith(":") and len(s) < 32)


def about_html(text):
    out, ul = [], False
    for line in text.split("\n"):
        line = line.rstrip()
        if line.startswith("• "):
            if not ul:
                out.append("<ul>"); ul = True
            out.append(f"<li>{inline(line[2:])}</li>"); continue
        if ul:
            out.append("</ul>"); ul = False
        if not line.strip():
            continue
        if is_heading(line):
            out.append(f"<h3>{inline(line.strip().strip('*').rstrip(':'))}</h3>")
        else:
            out.append(f"<p>{inline(line)}</p>")
    if ul:
        out.append("</ul>")
    return "\n".join(out)


def credits_for(slug):
    os.makedirs(os.path.join(ROOT, "content", "credits"), exist_ok=True)
    saved = os.path.join(ROOT, "content", "credits", slug + ".html")
    if os.path.exists(saved):
        return open(saved, encoding="utf-8").read()
    old = os.path.join(ROOT, slug, "index.html")
    block = ""
    if os.path.exists(old):
        s = open(old, encoding="utf-8").read()
        m = re.search(r"<h2>Credits</h2>\s*<ul>.*?</ul>", s, re.S)
        if m and "80085-detail" not in s:
            block = m.group(0)
    open(saved, "w", encoding="utf-8").write(block)
    return block


CSS = """*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.6 'Segoe UI',Arial,sans-serif;color:#163b32;background:#83c6b8}
.bg{position:fixed;inset:0;z-index:-1;background:url(/img/pool.jpg) center 70%/cover;filter:saturate(.95)}
.bg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#e9fff433,#0d3a3060)}
a{color:inherit}
header{position:sticky;top:0;z-index:5;padding:14px clamp(16px,4vw,60px);display:flex;align-items:center;justify-content:space-between;gap:12px;background:linear-gradient(180deg,#f5fff0c0,#d9f4e870);border-bottom:1px solid #ffffff80;backdrop-filter:blur(10px)}
.brand{font-size:26px;font-weight:800;letter-spacing:-1.7px;text-decoration:none;white-space:nowrap}.brand span{font-weight:400}
nav{display:flex;gap:22px;font-weight:600}nav a{text-decoration:none}nav a:hover{text-decoration:underline}
main{max-width:980px;margin:28px auto 60px;padding:0 clamp(14px,4vw,40px)}
.back{display:inline-block;margin:0 0 14px;font-weight:650;text-decoration:none;background:#effff0d0;border-radius:20px;padding:5px 14px}
.back:hover{text-decoration:underline}
.panel{border:1px solid #fff;border-radius:22px;background:linear-gradient(155deg,#ffffffee,#e9f9eedd);backdrop-filter:blur(14px);box-shadow:0 16px 40px #123f3740,inset 0 1px 1px #fff;padding:10px}
.art{position:relative;border-radius:15px;overflow:hidden;aspect-ratio:16/9;background:#000}
.art img{width:100%;height:100%;object-fit:cover;display:block}
.art.wide{aspect-ratio:10/3}
.art.icon{display:grid;place-items:center;background:radial-gradient(circle at 50% 35%,#f4fff0,#9ed9c4 65%,#5fae9a);aspect-ratio:21/9}
.art.icon img{width:auto;height:70%;aspect-ratio:1;border-radius:22%;box-shadow:0 10px 24px #123f3750}
.badge{position:absolute;top:14px;right:14px;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:#173f35d8;border-radius:20px;padding:5px 12px}
.body{padding:22px clamp(14px,3vw,34px) 26px}
h1{font-size:clamp(32px,5vw,54px);line-height:1.05;letter-spacing:-.05em;margin:4px 0 8px}
.lead{font-size:19px;font-weight:600;margin:0 0 18px;color:#214e40}
.platforms{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 6px}
.store{display:inline-flex;flex-direction:column;line-height:1.2;font-weight:700;color:#173f35;text-decoration:none;border:1px solid #fff;border-radius:16px;padding:8px 16px;background:linear-gradient(#e5ffcb,#9ed9a5);box-shadow:0 3px 8px #153f3230,inset 0 1px 1px #fff}
.store small{font-weight:600;font-size:12px;opacity:.8}
.store:hover{filter:brightness(1.05)}
.store.soon{background:#ffffff90;border-style:dashed;box-shadow:none;cursor:default}
.about{margin-top:22px}
.about h3{font-size:15px;letter-spacing:.08em;text-transform:uppercase;margin:22px 0 6px;color:#1d5a49}
.about p{margin:8px 0}.about ul{margin:6px 0;padding-left:20px}.about li{margin:4px 0}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
.card{border:1px solid #fff;border-radius:18px;background:#f2fff0d8;backdrop-filter:blur(12px);box-shadow:0 10px 26px #124c3c30;padding:20px 22px}
.card h2{font-size:20px;margin:0 0 8px;letter-spacing:-.02em}
dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0;font-size:14px}dt{font-weight:700}dd{margin:0}
.card ul{margin:6px 0 0;padding-left:18px;font-size:14px}
footer{text-align:center;padding:20px;color:#204c3e;background:#effff1c0}
a:focus-visible{outline:3px solid #126b70;outline-offset:3px}
@media(max-width:700px){.cols{grid-template-columns:1fr}.brand{font-size:21px}nav{gap:12px;font-size:13px}}"""


def page(p):
    slug = p["slug"]
    title = p["name"]
    img = f"/img/games/{p['image']}"
    cls = "wide" if p.get("wide") else ("icon" if p.get("icon") else "")
    badge = '<span class="badge">Coming soon</span>' if p["status"] == "soon" else ""
    btns = []
    for pl in p["platforms"]:
        url = p["links"].get(pl)
        if url:
            btns.append(f'<a class="store" href="{e(url)}" target="_blank" rel="noopener">{LABELS[pl]} ↗<small>{STORE[pl]}</small></a>')
        else:
            btns.append(f'<span class="store soon">{LABELS[pl]}<small>Coming soon</small></span>')
    for pl in p["soon"]:
        btns.append(f'<span class="store soon">{LABELS[pl]}<small>Coming soon</small></span>')
    details = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in p.get("details", []))
    legal = [f'<a href="{d}/">{n}</a>' for d, n in LEGAL if os.path.isdir(os.path.join(ROOT, slug, d))]
    subject = e(p["name"]) + "%20%E2%80%94%20Support"
    credits = credits_for(slug).replace("<h2>Credits</h2>", "<h2>Credits</h2>")
    side = f'<section class="card"><h2>Details</h2><dl>{details}</dl></section>' if details else ""
    desc = e(p["short"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<!-- 80085-detail: generated by tools/build.py -->
<title>{e(title)} — 80085games</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="https://80085.games{img}"><meta property="og:url" content="https://80085.games/{slug}/">
<link rel="canonical" href="https://80085.games/{slug}/"><link rel="icon" href="/img/icon.png">
<style>{CSS}</style></head><body><div class="bg" aria-hidden="true"></div>
<header><a class="brand" href="/">80085<span>games</span></a><nav><a href="/#games">Games</a><a href="/#studio">Studio</a><a href="/#contact">Contact</a></nav></header>
<main>
<a class="back" href="/#games">← All games</a>
<article class="panel">
<div class="art {cls}"><img src="{img}" alt="{e(title)} cover art">{badge}</div>
<div class="body">
<h1>{e(title)}</h1>
<p class="lead">{desc}</p>
<div class="platforms">{''.join(btns)}</div>
<div class="about">
{about_html(p.get('about', ''))}
</div>
</div>
</article>
<div class="cols">
{side}
<section class="card" id="support"><h2>Support</h2><p>Questions, bugs or feedback: <a href="#support" data-m="{EMAIL_B64}" data-s="{subject}" data-show="1">write to us</a></p>{('<p>' + ' · '.join(legal) + '</p>') if legal else ''}</section>
</div>
{('<div class="cols"><section class="card" style="grid-column:1/-1">' + credits + '</section></div>') if credits else ''}
</main>
<footer>© 2026 80085games · Vladimir Matsel</footer>
{MAIL_JS}
</body></html>
"""


def build_pages():
    for p in PROJECTS:
        if p.get("own_page"):
            continue
        d = os.path.join(ROOT, p["slug"])
        os.makedirs(d, exist_ok=True)
        credits_for(p["slug"])  # capture before overwrite
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(p))
        print("page", p["slug"])


def build_home():
    path = os.path.join(ROOT, "index.html")
    s = open(path, encoding="utf-8").read()
    games = [dict(name=p["name"], desc=p["short"], image=f"img/games/{p['image']}", platforms=p["platforms"],
                  soon=p["soon"], links=p["links"], page=p["page"], status=p["status"],
                  wide=bool(p.get("wide")), icon=bool(p.get("icon")), featured=bool(p.get("featured")))
             for p in PROJECTS]
    i0 = s.index("const games=")
    i1 = s.index("\n", i0)
    s = s[:i0] + "const games=" + json.dumps(games, ensure_ascii=False) + ";" + s[i1:]
    s = re.sub(r'id="count" role="status">\d+ projects<', f'id="count" role="status">{len(games)} projects<', s)
    open(path, "w", encoding="utf-8").write(s)
    print("home", len(games), "games")


if __name__ == "__main__":
    build_pages()
    build_home()
