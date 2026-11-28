import sys
from playwright.sync_api import sync_playwright
DORAN=open('doran.css').read()
FA=str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹')
fa=lambda n:str(n).translate(FA)
KICK='سیمای خیال'
TAG='تصویر ساخته‌شده با هوش مصنوعی'
S=[
 dict(k='img',art='assets/oblomov_in.png',kick=True,title='آبلوموف',sub='از رمان «آبلوموف»، ایوان گنچارف'),
 dict(k='text',title='گنچارف چه نوشته؟',paras=[
  'ایلیا ایلیچ آبلوموف کمی بیش از سی سال دارد؛ میان‌قد و خوش‌سیماست. چشم‌های خاکستری تیره‌اش جایی متمرکز نمی‌شود و چهره‌اش حالت ثابتی ندارد.',
  'به‌خاطر کم‌تحرکی از سنش پیرتر دیده می‌شود: گردنی سفید، دست‌هایی کوچک و چاق و شانه‌هایی نرم.',
  'در خانه روپوشی گشاد از پارچهٔ شرقی می‌پوشد، چنان بزرگ که دو بار دورش می‌پیچد، و دمپایی‌هایی چنان نرم که بی‌نگاه کردن پا در آن‌ها می‌رود.',
 ]),
 dict(k='img',art='assets/oblomov_out.png',title='ایلیا ایلیچ آبلوموف'),
 dict(k='img',art='assets/zakhar.png',title='زاخار'),
 dict(k='img',art='assets/stolz.png',title='اشتولتز'),
 dict(k='img',art='assets/olga.png',title='اولگا'),
]
N=len(S)
SIZES={'ig':(1080,1350),'tg':(1280,720),'x':(1600,900)}
VARS={
'ig':"--W:1080px;--H:1350px;--m:44px;--pad:96px 100px 80px;--ft:68px;--fb:38px;--ff:27px;--ct:90px;--cs:32px;--ck:30px",
'tg':"--W:1280px;--H:720px;--m:28px;--pad:52px 70px 42px;--ft:44px;--fb:25px;--ff:20px;--ct:64px;--cs:26px;--ck:24px",
'x':"--W:1600px;--H:900px;--m:32px;--pad:64px 90px 52px;--ft:54px;--fb:31px;--ff:23px;--ct:80px;--cs:31px;--ck:28px",
}
CSS=DORAN+"""
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Regular.woff2) format('woff2');font-weight:400}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Medium.woff2) format('woff2');font-weight:500}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-SemiBold.woff2) format('woff2');font-weight:600}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Bold.woff2) format('woff2');font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;background:#14100a}
body{font-family:Vazirmatn,sans-serif;direction:rtl;color:#1c1a16}
.slide{position:relative;width:var(--W);height:var(--H);overflow:hidden;background:#faf7f2;display:flex}
.lt{direction:ltr;unicode-bidi:isolate;display:inline-block}
.dark{background:#14100a;color:#faf7f2}
.col{flex-direction:column}
.pic{position:relative;background-size:cover;background-position:center;flex:none}
.ig .pic{width:1080px;height:1080px}
.tg .pic{width:720px;height:720px}.x .pic{width:900px;height:900px}
.tag{position:absolute;left:22px;bottom:22px;background:rgba(20,16,8,.62);color:#f1e7c9;font-size:calc(var(--ck)*.62);padding:6px 16px;border-radius:999px;font-weight:500}
.cap{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:10px;padding:0 50px}
.kk{color:#e3c46b;font-weight:600;font-size:var(--ck)}
.cap h1{font-family:Doran,Vazirmatn,sans-serif;font-weight:800;font-size:var(--ct);line-height:1.35;color:#faf7f2;text-wrap:balance}
.ig .cap h1{font-size:76px;line-height:1.25}
.cs{color:#f1e7c9;font-size:var(--cs);line-height:1.7;text-wrap:balance}
.ig .cap{gap:4px;padding:0 70px}.ig .cs{font-size:30px}.ig .kk{font-size:26px}
.frame{position:absolute;inset:var(--m);border:2px solid #c9a84c;pointer-events:none;z-index:3}
.frame::after{content:"";position:absolute;inset:9px;border:1px solid #c9a84c;opacity:.5}
.dia{position:absolute;width:24px;height:24px;background:#c9a84c;transform:rotate(45deg);z-index:4}
.dia.a{top:calc(var(--m) - 12px);left:calc(var(--m) - 12px)}.dia.b{top:calc(var(--m) - 12px);right:calc(var(--m) - 12px)}
.dia.c{bottom:calc(var(--m) - 12px);left:calc(var(--m) - 12px)}.dia.d{bottom:calc(var(--m) - 12px);right:calc(var(--m) - 12px)}
.tx{position:relative;flex:1;display:flex;flex-direction:column;padding:var(--pad);gap:26px;background:radial-gradient(ellipse at 50% 0%,rgba(201,168,76,.16),transparent 62%),#faf7f2}
.tx .kicker{display:flex;justify-content:center;color:#836a27;font-weight:600;font-size:calc(var(--ff)*1.1)}
h2{font-family:Doran,Vazirmatn,sans-serif;font-weight:800;font-size:var(--ft);text-align:center;line-height:1.3}
.bl{flex:1;display:flex;flex-direction:column;justify-content:center;gap:calc(var(--fb)*.6)}
.bp{font-size:var(--fb);line-height:1.95;text-align:justify;text-wrap:pretty}
.bn{font-size:calc(var(--fb)*.85);color:#836a27;font-weight:600;text-align:center;border-top:1px solid #d7c88f;padding-top:.5em;text-wrap:balance}
.foot{display:flex;justify-content:space-between;color:#836a27;font-weight:600;font-size:var(--ff)}
.foot b{font-family:Doran,Vazirmatn,sans-serif;font-size:calc(var(--ff)*1.45)}.foot .pg{color:#6b6456;font-weight:500}
"""
def html(i,s,p):
    W,H=SIZES[p]
    if s['k']=='img':
        pic=f'<div class="pic" style="background-image:url(../{s["art"]})"><div class="tag">{TAG}</div></div>'
        cap='<div class="cap">'+(f'<div class="kk">{KICK}</div>' if s.get('kick') else '')+f'<h1>{s["title"]}</h1>'+(f'<div class="cs">{s["sub"]}</div>' if s.get('sub') else '')+'</div>'
        # wide layout: image on the right (RTL start), text left
        cls='slide dark '+p+(' col' if p=='ig' else '')
        body=pic+cap
    else:
        frame='<div class="frame"></div><div class="dia a"></div><div class="dia b"></div><div class="dia c"></div><div class="dia d"></div>'
        fb=int({'ig':38,'tg':23,'x':29}[p])
        paras=''.join(f'<div class="bp">{t}</div>' for t in s['paras'])
        body=f'{frame}<div class="tx"><div class="kicker">{KICK}</div><h2>{s["title"]}</h2><div class="bl" style="--fb:{fb}px">{paras}</div><div class="foot"><span><b>دیوان</b> &nbsp;<span class="lt">diwan.center</span></span><span class="pg" dir="ltr">{fa(i)} / {fa(N)}</span></div></div>'
        cls='slide '+p
    return f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="{cls}" style="{VARS[p]}">{body}</div></body></html>'
if __name__=='__main__':
    plats=sys.argv[1:] or ['ig','tg','x']
    with sync_playwright() as pw:
        b=pw.chromium.launch(); 
        for p in plats:
            W,H=SIZES[p]
            for i,s in enumerate(S,1):
                f=f'out/_s{i}_{p}.html'; open(f,'w').write(html(i,s,p))
                pg=b.new_page(viewport={'width':W,'height':H}); pg.goto('file:///'+__import__('os').path.abspath(f).lstrip('/')); pg.wait_for_timeout(500)
                pg.screenshot(path=f'out/{p}{i:02d}.png'); pg.close()
        b.close()
