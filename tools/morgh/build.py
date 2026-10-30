import json,sys,re,os
from playwright.sync_api import sync_playwright
DORAN=open('doran.css').read()
FA=str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹')
def fa(n): return str(n).translate(FA)
L=lambda s:f'<span dir="ltr" class="lt">{s}</span>'
SLOT='<div class="slot"></div>'
COVERBG={
 'ig':'background-color:#05070e;background-image:url(../assets/cover_art.jpg);background-size:100% auto;background-position:center top;background-repeat:no-repeat',
 'st':'background-color:#05070e;background-image:url(../assets/cover_art.jpg);background-size:100% auto;background-position:center top;background-repeat:no-repeat',
 'tg':'background-color:#0a0e22;background-image:url(../assets/cover_art.jpg);background-size:auto 100%;background-position:92% center;background-repeat:no-repeat',
 'x':'background-color:#0a0e22;background-image:url(../assets/cover_art.jpg);background-size:auto 100%;background-position:92% center;background-repeat:no-repeat',
}
S=[
 dict(k='cover',kicker='پرسه در جهان کلمه',title='مرغ سحر',sub='همه‌مان تصنیف بهار را شنیده‌ایم؛<br>در اجراهای شجریان و حالا همایون.<br>اما مرغ سحر چیست و از کجا آمده؟',slot=True),
 dict(k='text',title='دو شعر، یک پرنده',body='این تصنیف را بهار حدود ۱۳۰۰ خورشیدی سرود.\nاما دهخدا هم شعری دارد با آغازی مشابه\n(صوراسرافیل، ۱۳۲۷ قمری):',slot=True),
 dict(k='text',title='فقط نمادِ زمانه نبود',body='بین این دو شعر حدود ۱۲ سال فاصله است. شاید فکر کنید در آن فضای پرتنش سیاسی، «مرغ سحر» اسم رمز بوده.\n\nاما ادبیات فارسی، فرهنگ و اساطیر ایران چارچوبی منسجم و درهم‌تنیده است. در گوشه‌گوشه‌ی آثارش می‌شود مرغ سحر، خروس یا شباهنگ را پیدا کرد: از فردوسی و سعدی تا جامی.'),
 dict(k='verse',cap1='نظامی، قرن ششم هجری (حدود ۱۱۴۱ تا ۱۲۰۹ میلادی)',v1=['به غول سیه بانگ برزد خروس','در آمد به غریدن آواز کوس'],cap2='و در جایی دیگر',v2=['برآورد مرغ سحرگه غریو','چو سرسامی از نور و صرعی ز دیو'],src='شرف‌نامه (بخش‌های ۱۶ و ۵۶) · به نقل از گنجور'),
 dict(k='text',title='پرودرش، پیش‌بینِ سپیده‌دم',body='برای این قصه باید عقب‌تر برویم؛ تا اوستا.\n\nدر اوستا خروس «پرودرش» نام دارد: «آن‌که سپیده‌دم را پیش از همه می‌بیند». آخر شب، سروش (فرشته‌ی نیایش و پاسدار شب) او را بیدار می‌کند تا مردم را به برخاستن و نیایش بخواند.',src='منبع: وندیداد، فرگرد ۱۸'),
 dict(k='text',title='دشمنِ خروس',body='بانگ خروس هشدار می‌دهد که «بوشاسپ» (بوشیاسپ)، دیو خواب و سستی، با دست‌های دراز می‌آید تا جهان بیدار را دوباره بخواباند.',src='منبع: وندیداد ۱۸؛ ایرانیکا، مدخل «Cock»'),
 dict(k='close',title='هر واژه قصه‌ای دارد.',body='قصه‌ی خودت را در دیوان بنویس.',final=''),
]
N=len(S); XS=[1,3,4,5]
SIZES={'st':(1080,1920),'ig':(1080,1350),'tg':(1280,720),'x':(1600,900)}
CSS=DORAN+"""
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Regular.woff2) format('woff2');font-weight:400}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Medium.woff2) format('woff2');font-weight:500}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-SemiBold.woff2) format('woff2');font-weight:600}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-Bold.woff2) format('woff2');font-weight:700}
@font-face{font-family:'Vazirmatn';src:url(../fonts/Vazirmatn-ExtraBold.woff2) format('woff2');font-weight:800}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;background:#faf7f2}
body{font-family:Vazirmatn,sans-serif;direction:rtl;color:#1c1a16}
.slide{position:relative;width:var(--W);height:var(--H);overflow:hidden;background:#faf7f2;display:flex}
.slide::before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(201,168,76,.16),transparent 62%);pointer-events:none}
.lt{direction:ltr;unicode-bidi:isolate;display:inline-block;font-family:Vazirmatn,sans-serif}
.panel{position:relative;flex:1;display:flex;flex-direction:column;min-width:0;padding:var(--pad);gap:var(--gap)}
.imgp{position:relative;flex:0 0 var(--imgw);height:100%;background-size:cover;background-position:center}
.kick{display:flex;align-items:center;justify-content:center;gap:16px;color:#836a27;font-weight:600;font-size:var(--fk)}
.kick i{width:var(--rule);height:2px;background:#c9a84c}
h1,h2{font-family:Doran,Vazirmatn,sans-serif;font-weight:800;line-height:1.3;text-align:center;font-size:var(--ft)}
.body{font-size:var(--fb);line-height:1.95;text-align:center;white-space:pre-line}
.main{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:var(--gap2);align-items:center}
.foot{display:flex;align-items:center;justify-content:space-between;color:#836a27;font-weight:600;font-size:var(--ff)}
.foot b{font-family:Doran,Vazirmatn,sans-serif;font-size:calc(var(--ff)*1.45);color:#836a27}
.foot .pg{color:#6b6456;font-weight:500}
.frame{position:absolute;inset:var(--m);border:2px solid #c9a84c;pointer-events:none;z-index:3}
.frame::after{content:"";position:absolute;inset:9px;border:1px solid #c9a84c;opacity:.5}
.dia{position:absolute;width:24px;height:24px;background:#c9a84c;transform:rotate(45deg);z-index:4}
.dia.a{top:calc(var(--m) - 12px);left:calc(var(--m) - 12px)}.dia.b{top:calc(var(--m) - 12px);right:calc(var(--m) - 12px)}
.dia.c{bottom:calc(var(--m) - 12px);left:calc(var(--m) - 12px)}.dia.d{bottom:calc(var(--m) - 12px);right:calc(var(--m) - 12px)}
.verse{position:relative;text-align:center;font-size:var(--fv);line-height:2.05;font-weight:500;padding:0 28px}
.verse.sm{font-size:calc(var(--fv)*.82)}
.vcap{color:#836a27;font-weight:600;font-size:calc(var(--fb)*.85)}
.src{color:#6b6456;font-size:calc(var(--fb)*.72);text-align:center}
.slot{width:72%;height:calc(var(--fb)*1.7);border:2px dashed #c9a84c;border-radius:14px;margin:6px auto;opacity:.9}
.cover .slot{border-color:#e3c46b}
.chips{display:flex;gap:18px;justify-content:center;flex-wrap:wrap}
.chip{border:2px solid #c9a84c;border-radius:14px;padding:10px 26px;text-align:center;background:rgba(201,168,76,.10)}
.chip .w{font-size:calc(var(--fb)*1.25);font-weight:700;color:#1c1a16;direction:ltr}.chip .l{font-size:calc(var(--fb)*.66);color:#6b6456}
.note{font-size:calc(var(--fb)*.72);color:#6b6456;text-align:center}
.eq{font-family:Doran,Vazirmatn;font-size:calc(var(--ft)*1.05);color:#836a27;font-weight:800;text-align:center}
.chain{display:flex;flex-direction:var(--cdir);align-items:center;justify-content:center;gap:var(--cgap)}
.node{border:2px solid #c9a84c;border-radius:16px;padding:14px 22px;text-align:center;background:#fff9ec;min-width:var(--nw)}
.node .w{font-size:calc(var(--fb)*1.15);font-weight:700;direction:ltr}.node .l{font-size:calc(var(--fb)*.68);color:#836a27;font-weight:600}.node .m{font-size:calc(var(--fb)*.66);color:#6b6456}
.arr{color:#c9a84c;font-size:calc(var(--fb)*1.3);line-height:1}
.tree{display:flex;flex-direction:column;align-items:center;gap:var(--cgap);width:100%}
.kids{display:flex;gap:18px;width:100%;justify-content:center}
.kid{flex:1;border:2px solid #c9a84c;border-radius:16px;padding:14px 12px;text-align:center;background:#fff9ec}
.kid .w{font-family:Doran,Vazirmatn;font-size:calc(var(--fb)*1.3);font-weight:800}.kid .e{font-size:calc(var(--fb)*.62);color:#836a27;direction:ltr;font-weight:600;margin:4px 0}.kid .m{font-size:calc(var(--fb)*.66);color:#6b6456}
.root{border:2px solid #836a27;background:#836a27;color:#fff;border-radius:16px;padding:10px 34px;text-align:center}
.root .w{font-size:calc(var(--fb)*1.3);font-weight:800;direction:ltr}.root .m{font-size:calc(var(--fb)*.7)}
.tbl{width:100%;border-collapse:collapse;font-size:var(--ftb)}
.tbl th{background:#c9a84c;color:#0c0a07;padding:var(--tp) 14px;font-weight:700}
.tbl td{padding:var(--tp) 14px;border-bottom:1px solid #ddd8ce;text-align:center}
.tbl td:first-child{font-weight:700;font-family:Doran,Vazirmatn}
.tbl tr.win td{background:#fff1cc;font-weight:800;color:#1c1a16}.tbl td.bd{color:#836a27;font-weight:800;font-size:.72em}.tbl td:nth-child(2){font-family:Vazirmatn,sans-serif}.kk2{color:#836a27;font-weight:600;font-size:var(--fk)}.lead{font-size:calc(var(--fb)*.85);color:#6b6456;text-align:center}
.acard{width:100%;border:2px solid #d7d2c6;border-radius:26px;padding:var(--ap);display:flex;flex-direction:var(--cdir);align-items:center;justify-content:center;gap:var(--ag);background:linear-gradient(165deg,rgba(43,93,147,.09),#fffdf8 65%)}
.aav{display:flex;flex-direction:column;align-items:center;gap:14px}.arch{width:var(--aw);height:calc(var(--aw)*1.25);border-radius:999px 999px 14px 14px;border:3px solid rgba(43,93,147,.4);background-size:cover;background-position:center}
.lvl{border:1.5px solid #2b5d93;color:#2b5d93;border-radius:999px;padding:4px 22px;font-size:calc(var(--fb)*.6);font-weight:500}
.atx{text-align:center}.aname{font-family:Doran,Vazirmatn;font-weight:800;font-size:calc(var(--ft)*1.1)}.aact{color:#6b6456;font-size:calc(var(--fb)*.85);margin-top:6px}
.wk{display:flex;align-items:center;gap:16px;background:#fff;border:1.5px solid #e3ded3;border-radius:16px;padding:12px 16px;max-width:var(--wkw)}
.wt{font-weight:600;font-size:calc(var(--fb)*.62);line-height:1.7;text-align:right}.wc{flex:0 0 var(--cw);height:var(--cw);border-radius:10px;background-size:cover;background-position:center}
.final{white-space:pre-line;font-family:Doran,Vazirmatn;font-weight:800;color:#836a27;font-size:var(--fb2);text-align:center;line-height:1.6}
.link{direction:ltr;font-weight:700;letter-spacing:.06em;color:#836a27;font-size:var(--ff2);text-align:center}
.cover .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,8,0) 35%,rgba(20,16,8,.88) 100%);z-index:1}
.cover{background-size:cover}
.cover .ct{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:var(--cpad);text-align:center;color:#faf7f2;display:flex;flex-direction:column;gap:18px;align-items:center}
.cover h1{color:#faf7f2;font-size:var(--fct)}
.cover .sub{font-size:var(--fb);color:#f1e7c9;line-height:1.8}
.cover .kk{color:#e3c46b;font-weight:600;font-size:var(--fk)}
"""
VARS={
'ig':"--W:1080px;--H:1350px;--m:44px;--pad:104px 100px 96px;--gap:34px;--gap2:30px;--fk:30px;--rule:60px;--ft:70px;--fb:40px;--ff:27px;--ff2:36px;--fv:48px;--ftb:35px;--tp:20px;--fb2:44px;--cdir:column;--cgap:20px;--nw:520px;--imgw:0px;--fct:104px;--cpad:90px 80px 100px",
'tg':"--W:1280px;--H:720px;--m:28px;--pad:56px 64px 46px;--gap:16px;--gap2:18px;--fk:21px;--rule:44px;--ft:42px;--fb:24px;--ff:20px;--ff2:24px;--fv:30px;--ftb:21px;--tp:8px;--fb2:32px;--cdir:row;--cgap:12px;--nw:170px;--imgw:700px;--fct:84px;--cpad:50px 60px 60px",
'x':"--W:1600px;--H:900px;--m:32px;--pad:70px 80px 56px;--gap:20px;--gap2:22px;--fk:24px;--rule:50px;--ft:52px;--fb:29px;--ff:23px;--ff2:28px;--fv:36px;--ftb:25px;--tp:10px;--fb2:38px;--cdir:row;--cgap:14px;--nw:200px;--imgw:860px;--fct:104px;--cpad:60px 80px 70px",
}
VARS['st']=VARS['ig'].replace('--H:1350px','--H:1920px')
def foot(i,plat):
    pos,tot=(XS.index(i)+1,len(XS)) if plat=='x' else (i,N)
    return f'<div class="foot"><span><b>دیوان</b> &nbsp;<span class="lt">diwan.center</span></span><span class="pg">{fa(pos)} / {fa(tot)}</span></div>'
def html(i,s,plat):
    k=s['k']; W,H=SIZES[plat]; wide=plat!='ig'
    frame='<div class="frame"></div><div class="dia a"></div><div class="dia b"></div><div class="dia c"></div><div class="dia d"></div>'
    def kick(): return ''
    if k=='cover':
        return f'<div class="slide cover" style="{COVERBG[plat]}"><div class="shade"></div><div class="ct"><div class="kk">{s["kicker"]}</div><h1>{s["title"]}</h1><div class="sub">{s["sub"]}</div>{SLOT if s.get("slot") else ""}</div></div>'
    inner=''
    if k=='chips':
        inner=f'<h2>{s["title"]}</h2><div class="body">{s["body"]}</div><div class="chips">'+''.join(f'<div class="chip"><div class="w">{w}</div><div class="l">{l}</div></div>' for w,l in s['chips'])+f'</div><div class="note">{s["note"]}</div>'
    elif k=='text':
        inner=f'<h2>{s["title"]}</h2><div class="body">{s["body"]}</div>'+(SLOT if s.get('slot') else '')+(f'<div class="src">{s["src"]}</div>' if s.get('src') else '')
    elif k=='word':
        inner=f'<h2>{s["title"]}</h2><div class="eq">{s["eq"]}</div><div class="body">{s["body"]}</div>'
    elif k=='verse':
        inner=f'<div class="vcap">{s["cap1"]}</div><div class="verse">{"<br>".join(s["v1"])}</div><div class="vcap">{s["cap2"]}</div><div class="verse">{"<br>".join(s["v2"])}</div><div class="src">{s["src"]}</div>'
    elif k=='chain':
        parts=[]
        for n,(w,l,m) in enumerate(s['chain']):
            if n: parts.append('<div class="arr">'+('◀' if wide else '▼')+'</div>')
            parts.append(f'<div class="node"><div class="w">{w}</div><div class="l">{l}</div><div class="m">{m}</div></div>')
        inner=f'<h2>{s["title"]}</h2><div class="chain">{"".join(parts)}</div><div class="note">{s["note"]}</div>'
    elif k=='tree':
        r=s['root']
        inner=f'<h2>{s["title"]}</h2><div class="tree"><div class="root"><div class="w" style="direction:rtl">{r[0]}</div><div class="m">{r[1]}</div></div><div class="arr">▼</div><div class="kids">'+''.join(f'<div class="kid"><div class="w">{a}</div><div class="e">{b}</div><div class="m">{c}</div></div>' for a,b,c in s['kids'])+'</div></div>'
    elif k=='table':
        inner=f'<h2>{s["title"]}</h2><table class="tbl"><tr>'+''.join(f'<th>{h}</th>' for h in s['head'])+'</tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in s['rows'])+'</table>'
    elif k=='aotw':
        inner=(f'<div class="kk2">{s["kicker"]}</div><h2 style="font-size:calc(var(--ft)*1.25)">{s["title"]}</h2><div class="lead">{s["lead"]}</div>'
          f'<div class="acard"><div class="aav"><div class="arch" style="background-image:url(../'+CFG['avatar']+')"></div></div>'
          f'<div class="atx"><div class="aname">{s["name"]}</div><div class="aact">{s["act"]}</div></div>'
          f'<div class="wk"><div class="wt">{s["work"]}</div><div class="wc" style="background-image:url(../'+CFG['cover']+')"></div></div></div>')
    elif k=='lb':
        rows=''.join('<tr'+(' class="win"' if n==0 else '')+'>'+''.join(f'<td>{c}</td>' for c in r)+('<td class="bd">'+s['badge']+'</td>' if n==0 else '<td class="bd"></td>')+'</tr>' for n,r in enumerate(s['rows']))
        inner=f'<h2>{s["title"]}</h2><table class="tbl"><tr>'+''.join(f'<th>{h}</th>' for h in s['head'])+'<th></th></tr>'+rows+f'</table><div class="note">{s["note"]}</div>'
    elif k=='close':
        inner=f'<h2>{s["title"]}</h2><div class="body">{s["body"]}</div>{('<div class="final">'+s["final"]+'</div>') if s["final"] else ''}<div class="link">diwan.center</div>'
    elif k in('imgtext','imgverse'):
        t=f'<h2>{s["title"]}</h2>'
        if s.get('body'): t+=f'<div class="body">{s["body"]}</div>'
        if s.get('verse'): t+=f'<div class="verse sm">{"<br>".join(s["verse"])}</div><div class="src">{s["src"]}</div>'
        if wide:
            return f'<div class="slide"><div class="panel" style="--pad:44px 56px 40px">{kick()}<div class="main">{t}</div>{foot(i,plat)}</div><div class="imgp" style="background-image:url(../{s.get("imgw",s["img"])});background-position:{s.get("tpos","50%")} center;{("flex-basis:%dpx"%s["pw"][plat]) if s.get("pw") else ""}"></div></div>'
        # ig: image top, text bottom
        ih=720
        return (f'<div class="slide" style="flex-direction:column"><div style="height:{ih}px;background-image:url(../{s.get("imgw",s["img"])});background-size:cover;background-position:center {s.get("pos","50%")};border-bottom:3px solid #c9a84c"></div>'
                f'<div class="panel" style="--pad:34px 90px 54px;--gap:14px">{kick()}<div class="main" style="--gap2:14px">{t}</div>{foot(i,plat)}</div></div>')
    return f'<div class="slide">{frame}<div class="panel">{kick()}<div class="main">{inner}</div>{foot(i,plat)}</div></div>'
def page(i,s,plat):
    # tweak: imgtext on IG uses smaller text sizes
    pv={'ig':'--ap:40px 36px;--ag:22px;--aw:200px;--wkw:100%;--cw:84px','st':'--ap:44px 36px;--ag:26px;--aw:250px;--wkw:100%;--cw:92px','tg':'--ap:22px 40px;--ag:40px;--aw:130px;--wkw:46%;--cw:64px','x':'--ap:26px 50px;--ag:46px;--aw:160px;--wkw:46%;--cw:76px'}[plat]
    extra=':root{'+pv+'}'+('.pg{display:none}' if plat=='st' else '')+'.body{font-size:calc(var(--fb)*1.2)}h2{font-size:calc(var(--ft)*1.12)}'
    if plat=='ig' and s['k']=='cover': extra+='.cover .ct{padding-bottom:54px;gap:10px}.cover h1{font-size:92px}.cover .sub{font-size:34px;line-height:1.7}.cover .slot{height:56px;margin:2px auto 0}.cover .shade{display:block;position:absolute;inset:0;z-index:1;background:linear-gradient(to bottom,rgba(5,7,14,0) 60%,rgba(5,7,14,.88) 70%,#05070e 77%)}'
    if plat=='st' and s['k']=='cover': extra+='.cover h1{font-size:132px}.cover .sub{font-size:46px;line-height:1.7}.cover .ct{padding-bottom:130px;gap:16px}.cover .slot{height:80px}.cover .shade{display:block;position:absolute;inset:0;z-index:1;background:linear-gradient(to bottom,rgba(5,7,14,0) 58%,rgba(5,7,14,.9) 68%,#05070e 74%)}'
    if plat in('tg','x') and s['k']=='cover': extra+='.cover .shade{display:none}.cover .ct{left:0;right:auto;top:0;width:50%;justify-content:center;padding:0 36px 0 36px}'
    if plat=='ig' and s['k'] in('imgtext','imgverse'): extra='.body{font-size:33px;line-height:1.85}h2{font-size:56px}.verse.sm{font-size:37px}.kick{font-size:26px}'
    if plat=='ig' and s['k']=='chain' and len(s['chain'])>3: extra+='.node{padding:8px 20px}.chain{gap:10px}.node .w{font-size:36px}'
    return f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><style>{CSS}:root{{{VARS[plat]}}}{extra}</style></head><body>{html(i,s,plat)}</body></html>'
if __name__=='__main__':
    only=[1] if 'card' in sys.argv else ([int(x) for x in sys.argv[1:]] or range(1,N+1))
    PL=lambda i:[p for p in SIZES if p!='st' and not (p=='x' and i not in XS)]+(['st'] if i==1 else [])
    os.makedirs('out',exist_ok=True)
    over=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for i in only:
            s=S[i-1]
            for plat in PL(i):
                W,H=SIZES[plat]
                open(f'out/_s{i}_{plat}.html','w').write(page(i,s,plat))
                pg=b.new_page(viewport={'width':W,'height':H})
                pg.goto(f'file://{os.getcwd()}/out/_s{i}_{plat}.html'); pg.wait_for_timeout(300)
                bad=pg.evaluate("""()=>{const m=document.querySelector('.main');const p=document.querySelector('.panel');const r=[];if(m&&m.scrollHeight>m.clientHeight+2)r.push('main');if(p&&p.scrollHeight>p.clientHeight+2)r.push('panel');const sl=document.querySelector('.slide');if(sl.scrollHeight>sl.clientHeight+2||sl.scrollWidth>sl.clientWidth+2)r.push('slide');return r}""")
                if bad: over.append((i,plat,bad))
                pg.screenshot(path=f'out/s{i:02d}_{plat}.png',clip={'x':0,'y':0,'width':W,'height':H}); pg.close()
        b.close()
    print('overflow:',over)
