#!/usr/bin/env python3
"""Generates index.html for the diwan profile-photo video.
Edit DUR (seconds per scene) after the voice recording, then run: python3 build.py
"""
import json

TURN = 1.0          # page-turn length (outgoing scene's tail)
W, H = 1920, 1080
CARD_X, CARD_Y = 192, 150   # browser card top-left (card is 1536 wide)
BAR_H = 44

# ---- scenes -------------------------------------------------------------
# shot: img, w, h, at (relative start), fade; rings: rect + at; zoom: origin/scale/at
S = []

# 1. hook (home hero strip) — first frame is the platform cover: fully visible at t=0
S.append(dict(kind="step", dur=6.0, url="diwan.center",
              caption="دوست داری عکست کنار بقیه‌ی نویسنده‌های دیوان باشد؟ فقط چند ثانیه وقت می‌خواهد.",
              shots=[dict(img="home.jpg", w=1536, h=639, at=0,
                          rings=[dict(rect=[1170, 560, 1320, 600], at=1.2)],
                          zoom=dict(origin=[1245, 560], scale=1.6, at=1.6))]))

S.append(dict(kind="step", dur=4.0, url="diwan.center/settings",
              caption="وارد حسابت شو و تنظیمات را باز کن.",
              shots=[dict(img="settings-empty.jpg", w=1536, h=639, at=0,
                          rings=[dict(rect=[1328, 463, 1530, 500], at=1.0)])]))

S.append(dict(kind="step", dur=4.5, url="diwan.center/settings",
              caption="در بخش «تصویر پروفایل»، روی انتخاب عکس بزن.",
              shots=[dict(img="settings-empty.jpg", w=1536, h=639, at=0,
                          rings=[dict(rect=[892, 152, 980, 240], at=1.0)],
                          zoom=dict(origin=[900, 196], scale=1.7, at=0.6))]))

S.append(dict(kind="step", dur=5.0, url="diwan.center/settings",
              caption="یک عکس بردار؛ JPG، PNG یا WebP، تا ۱۰ مگابایت.",
              shots=[dict(img="settings-empty.jpg", w=1536, h=639, at=0,
                          rings=[dict(rect=[678, 181, 882, 204], at=1.0)],
                          zoom=dict(origin=[780, 192], scale=1.9, at=0.6))]))

S.append(dict(kind="step", dur=6.0, url="diwan.center/settings",
              caption="قاب را روی چهره‌ات تنظیم کن و تأیید را بزن.",
              shots=[dict(img="crop.jpg", w=1536, h=695, at=0,
                          rings=[dict(rect=[624, 181, 912, 470], at=0.8),
                                 dict(rect=[862, 517, 969, 555], at=3.2)])]))

S.append(dict(kind="step", dur=8.0, url="diwan.center",
              caption="ذخیره که بشود، عکست کنار نویسنده‌های دیگر نشان داده می‌شود.",
              shots=[dict(img="settings-after.jpg", w=1536, h=639, at=0, url="diwan.center/settings",
                          rings=[dict(rect=[892, 152, 980, 240], at=0.8)]),
                     dict(img="home.jpg", w=1536, h=639, at=3.4, fade=0.7,
                          rings=[dict(rect=[1272, 558, 1320, 602], at=4.8)],
                          zoom=dict(origin=[1290, 580], scale=2.2, at=4.4))]))

S.append(dict(kind="end", dur=7.0,
              caption="اینجا برای همه‌ جا هست."))

NSTEP = sum(1 for s in S if s["kind"] == "step")
PERSIAN = "۰۱۲۳۴۵۶۷۸۹"
def fa(n): return "".join(PERSIAN[int(c)] for c in str(n))

# ---- voice-driven timing -------------------------------------------------
import os
VM = "assets/voice/meta.json"
LEAD, TAIL = 1.0, 0.5
VOICE = []
if os.path.exists(VM):
    meta = json.load(open(VM))
    for i, sc in enumerate(S):
        vd = float(meta[str(i + 1)])
        lead = 0.7 if i == 0 else LEAD
        tail = 1.5 if sc["kind"] == "end" else TAIL
        newd = round(lead + vd + tail, 3)
        f = newd / sc["dur"]
        for sh in sc.get("shots", []):
            sh["at"] = round(sh["at"] * f, 3)
            for r in sh.get("rings", []): r["at"] = round(r["at"] * f, 3)
            if sh.get("zoom"): sh["zoom"]["at"] = round(sh["zoom"]["at"] * f, 3)
        sc["dur"] = newd
        sc["lead"] = lead
        sc["vd"] = vd

t = 0.0
for s in S:
    s["T"] = t
    t += s["dur"]
TOTAL = round(t, 3)

# ---- html -----------------------------------------------------------------
parts = []
audio = []
tl = []   # js lines
step_no = 0
for i, s in enumerate(S):
    last = i == len(S) - 1
    d = s["dur"] + (0 if last else TURN)
    T = s["T"]
    z = 100 - i
    sid = f"s{i+1}"
    h = [f'<section id="{sid}" class="clip scene" data-start="{T}" data-duration="{d}" style="z-index:{z}">',
         f'<div class="page" id="{sid}-page">']
    # header
    h.append('<div class="hdr"><div class="brand" data-layout-allow-overlap><img src="assets/logo.png" alt=""><span>دیوان</span></div>')
    if s["kind"] == "step":
        step_no += 1
        h.append(f'<div class="stepno">قدم {fa(step_no)} از {fa(NSTEP)}</div>')
    h.append('</div>')

    if s["kind"] == "title":
        h.append('<div class="titlecard"><img class="biglogo" src="assets/logo.png" alt="">'
                 '<h1>عکس پروفایل در دیوان</h1><h2>قدم‌به‌قدم</h2></div>')
    elif s["kind"] == "end":
        h.append('<div class="titlecard"><img class="biglogo" src="assets/logo.png" alt="">'
                 '<h1 class="url">diwan.center</h1></div>')
    else:
        h.append(f'<div class="card" id="{sid}-card"><div class="bar"><i></i><i></i><i></i>'
                 + "".join(f'<span class="url" id="{sid}-u{j}">{sh.get("url", s["url"])}</span>' for j, sh in enumerate(s["shots"])) + '</div><div class="viewport">')
        for j, sh in enumerate(s["shots"]):
            left = (1536 - sh["w"]) // 2
            top = (639 - sh["h"]) // 2
            shid = f"{sid}-sh{j}"
            h.append(f'<div class="shot" id="{shid}" style="left:0;top:0;width:1536px;height:639px">'
                     f'<div class="zoomer" id="{shid}-z" style="left:{left}px;top:{top}px;width:{sh["w"]}px;height:{sh["h"]}px"><img src="assets/shots/{sh["img"]}" width="{sh["w"]}" height="{sh["h"]}" alt="">')
            for k, r in enumerate(sh.get("rings", [])):
                x1, y1, x2, y2 = r["rect"]
                h.append(f'<div class="ring" id="{shid}-r{k}" style="left:{x1}px;top:{y1}px;width:{x2-x1}px;height:{y2-y1}px"></div>')
            h.append('</div></div>')
        h.append('</div></div>')
    h.append(f'<div class="caption" id="{sid}-cap"><span>{s["caption"]}</span></div>')
    h.append(f'<div class="prog"><b id="{sid}-prog"></b></div>')
    h.append('<div class="shade" id="%s-shade"></div>' % sid)
    h.append('</div></section>')
    parts.append("\n".join(h))

    # ---- animation
    tl.append(f'// scene {i+1}')
    if i > 0:
        tl.append(f'tl.fromTo("#{sid}-cap", {{opacity:0,y:26}}, {{opacity:1,y:0,duration:0.6,ease:"power2.out"}}, {T+0.4});')
    pf, pt = i / len(S), (i + 1) / len(S)
    tl.append(f'tl.fromTo("#{sid}-prog", {{width:"{pf*100:.2f}%"}}, {{width:"{pt*100:.2f}%",duration:{s["dur"]},ease:"none"}}, {T});')
    if s["kind"] in ("title", "end"):
        if i == 0:  # first frame is the platform cover: everything visible at t=0
            tl.append(f'tl.fromTo("#{sid} .biglogo", {{scale:0.97}}, {{scale:1,duration:1.2,ease:"power2.out"}}, 0);')
            tl.append(f'tl.set("#{sid}-cap", {{opacity:1,y:0}}, 0);')
        else:
            tl.append(f'tl.fromTo("#{sid} .biglogo", {{opacity:0,y:30,scale:0.94}}, {{opacity:1,y:0,scale:1,duration:0.9,ease:"power3.out"}}, {T+0.1});')
            tl.append(f'tl.fromTo("#{sid} h1", {{opacity:0,y:30}}, {{opacity:1,y:0,duration:0.8,ease:"power3.out"}}, {T+0.5});')
            if s["kind"] == "title":
                tl.append(f'tl.fromTo("#{sid} h2", {{opacity:0,y:24}}, {{opacity:1,y:0,duration:0.8,ease:"power3.out"}}, {T+0.9});')
    else:
        if i == 0:
            tl.append(f'tl.set("#{sid}-card", {{opacity:1,y:0}}, 0);')
            tl.append(f'tl.set("#{sid}-cap", {{opacity:1,y:0}}, 0);')
        else:
            tl.append(f'tl.fromTo("#{sid}-card", {{opacity:0,y:30}}, {{opacity:1,y:0,duration:0.7,ease:"power3.out"}}, {T+0.05});')
        for j, sh in enumerate(s["shots"]):
            shid = f"{sid}-sh{j}"
            at = sh["at"]
            if j == 0:
                pass
            else:
                tl.append(f'tl.set("#{shid}", {{opacity:0}}, 0);')
                tl.append(f'tl.set("#{sid}-u{j}", {{opacity:0}}, 0);')
                tl.append(f'tl.to("#{sid}-u{j}", {{opacity:1,duration:{sh.get("fade",0.5)}}}, {T+at});')
                tl.append(f'tl.to("#{sid}-u{j-1}", {{opacity:0,duration:{sh.get("fade",0.5)}}}, {T+at});')
                tl.append(f'tl.to("#{shid}", {{opacity:1,duration:{sh.get("fade",0.5)},ease:"power1.inOut"}}, {T+at});')
            rings = sh.get("rings", [])
            for k, r in enumerate(rings):
                rid = f"#{shid}-r{k}"
                a = T + r["at"]
                tl.append(f'tl.fromTo("{rid}", {{opacity:0,scale:1.25}}, {{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}}, {a});')
                if k + 1 < len(rings):
                    tl.append(f'tl.to("{rid}", {{opacity:0,duration:0.35}}, {T+rings[k+1]["at"]-0.1});')
                elif j + 1 < len(s["shots"]):
                    tl.append(f'tl.to("{rid}", {{opacity:0,duration:0.3}}, {T+s["shots"][j+1]["at"]-0.2});')
            if sh.get("zoom"):
                zm = sh["zoom"]
                ox, oy = zm["origin"]
                tl.append(f'tl.set("#{shid}-z", {{transformOrigin:"{ox}px {oy}px"}}, 0);')
                tl.append(f'tl.to("#{shid}-z", {{scale:{zm["scale"]},duration:1.3,ease:"power2.inOut"}}, {T+zm["at"]});')
    # voice
    if "vd" in s:
        audio.append((f"voice:L{i+1:02d}", T + s["lead"], s["vd"], 1.0))
    # sfx
    if s["kind"] in ("title", "end"):
        # short chime that ends before the voice starts (SFX must never overlap the voice)
        audio.append(("chime", T + 0.0, min(0.65, s.get("lead", 1.0) - 0.05), 0.7))
    # page turn (outgoing)
    if not last:
        tt = T + s["dur"]
        audio.append(("flip", tt - 0.05, 1.0, 0.8))
        tl.append(f'tl.set("#{sid}-page", {{transformOrigin:"100% 50%",transformPerspective:2400}}, 0);')
        tl.append(f'tl.to("#{sid}-page", {{rotationY:92,duration:{TURN},ease:"power2.in"}}, {tt});')
        tl.append(f'tl.fromTo("#{sid}-shade", {{opacity:0}}, {{opacity:0.55,duration:{TURN},ease:"power2.in"}}, {tt});')

def _src(nm):
    return "assets/voice/" + nm[6:] + ".wav" if nm.startswith("voice:") else "assets/sfx/" + nm + ".wav"
AUDIO = "\n".join(f'<audio id="a{n}" src="{_src(nm)}" data-start="{round(st,3)}" data-duration="{round(du,3)}" data-volume="{vol}"></audio>' for n, (nm, st, du, vol) in enumerate(audio))

html = f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Vazirmatn"; font-weight: 400; src: url("assets/fonts/Vazirmatn-Regular.woff2") format("woff2"); }}
@font-face {{ font-family: "Vazirmatn"; font-weight: 500; src: url("assets/fonts/Vazirmatn-Medium.woff2") format("woff2"); }}
@font-face {{ font-family: "Vazirmatn"; font-weight: 600; src: url("assets/fonts/Vazirmatn-SemiBold.woff2") format("woff2"); }}
@font-face {{ font-family: "Vazirmatn"; font-weight: 700; src: url("assets/fonts/Vazirmatn-Bold.woff2") format("woff2"); }}
@font-face {{ font-family: "Vazirmatn"; font-weight: 800; src: url("assets/fonts/Vazirmatn-ExtraBold.woff2") format("woff2"); }}
:root {{ --paper:#faf7f2; --ink:#1c1a17; --gold:#c8a44a; --gold-d:#8a6d1f; --muted:#6b665d; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:var(--paper); font-family:"Vazirmatn", sans-serif; }}
#root {{ position:relative; width:100%; height:100%; background:#e9e3d6; }}
.scene {{ position:absolute; inset:0; }}
.page {{ position:absolute; inset:0; background:var(--paper);
  background-image: radial-gradient(rgba(200,164,74,.10) 1.2px, transparent 1.4px); background-size: 26px 26px;
  backface-visibility:hidden; overflow:hidden; }}
.shade {{ position:absolute; inset:0; pointer-events:none; opacity:0;
  background: linear-gradient(270deg, rgba(0,0,0,0) 0%, rgba(60,45,10,.35) 100%); }}
.hdr {{ position:absolute; top:34px; left:70px; right:70px; height:80px; display:flex; align-items:center; justify-content:space-between; }}
.brand {{ display:flex; align-items:center; gap:16px; font-weight:800; font-size:44px; color:var(--ink); }}
.brand img {{ height:68px; }}
.stepno {{ font-weight:600; font-size:30px; color:var(--gold-d); padding:8px 26px; border:2px solid var(--gold); border-radius:999px; background:#fff8e6; }}
.card {{ position:absolute; left:{CARD_X}px; top:{CARD_Y - 20}px; width:1536px; height:{639+BAR_H}px; border-radius:18px;
  background:#fff; box-shadow:0 30px 80px rgba(60,45,10,.22), 0 0 0 1px rgba(60,45,10,.10); overflow:hidden; direction:ltr; }}
.bar {{ height:{BAR_H}px; background:#efe9dc; display:flex; align-items:center; gap:10px; padding:0 18px; border-bottom:1px solid rgba(60,45,10,.12); }}
.bar i {{ width:13px; height:13px; border-radius:50%; background:#d8cfbb; display:block; }}
.bar {{ position:relative; }}
.bar .url {{ position:absolute; left:50%; top:7px; transform:translateX(-50%); background:#faf7f2; border-radius:999px; padding:4px 28px; font-family:"Vazirmatn"; font-size:20px; color:var(--muted); direction:ltr; }}
.viewport {{ position:relative; width:1536px; height:639px; background:var(--paper); overflow:hidden; }}
.shot {{ position:absolute; overflow:hidden; background:var(--paper); }}
.zoomer {{ position:absolute; }}
.zoomer img {{ display:block; }}
.ring {{ position:absolute; border:4px solid var(--gold); border-radius:14px; opacity:0;
  box-shadow:0 0 0 6px rgba(200,164,74,.28), 0 0 34px rgba(200,164,74,.75); }}
.caption {{ position:absolute; left:0; right:0; top:830px; display:flex; justify-content:center; padding:0 150px; direction:rtl; }}
.caption span {{ display:inline-block; text-align:center; font-weight:600; font-size:50px; line-height:1.65; text-wrap:balance; color:var(--ink);
  background:rgba(255,255,255,.88); border:2px solid rgba(200,164,74,.55); border-radius:26px; padding:12px 44px;
  box-shadow:0 10px 30px rgba(60,45,10,.10); }}
.prog {{ position:absolute; left:0; right:0; bottom:0; height:10px; background:rgba(200,164,74,.18); direction:rtl; }}
.prog b {{ display:block; height:100%; background:var(--gold); width:0; }}
.titlecard {{ position:absolute; left:0; right:0; top:150px; display:flex; flex-direction:column; align-items:center; gap:22px; }}
.biglogo {{ height:250px; }}
.titlecard h1 {{ font-weight:800; font-size:92px; color:var(--ink); line-height:1.3; }}
.titlecard h1.url {{ font-family:"Vazirmatn"; direction:ltr; letter-spacing:1px; }}
.titlecard h2 {{ font-weight:600; font-size:56px; color:var(--gold-d); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(parts)}
{AUDIO}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
'''
open("index.html", "w", encoding="utf-8").write(html)
print("total", TOTAL, "scenes", len(S))
